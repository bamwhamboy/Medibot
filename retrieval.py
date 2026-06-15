"""
MediBot Retrieval Engine
Implements Hybrid RAG: BM25 keyword search + TF-IDF vector search + Cross-encoder reranking
All retrieval is RBAC-filtered at the retrieval layer.
"""

import math
import re
from collections import Counter
from knowledge_base import DOCUMENTS, get_accessible_docs, ROLE_COLLECTIONS


# ─── TEXT UTILITIES ────────────────────────────────────────────────────────────

def tokenize(text: str) -> list[str]:
    """Simple tokenizer: lowercase, split on non-alphanumeric, remove stopwords."""
    stopwords = {
        "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "need", "dare", "ought",
        "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
        "up", "about", "into", "through", "during", "before", "after", "above",
        "below", "between", "and", "but", "or", "nor", "not", "so", "yet",
        "both", "either", "neither", "each", "few", "more", "most", "other",
        "some", "such", "than", "too", "very", "just", "it", "its", "this",
        "that", "these", "those", "as", "if", "then", "there", "when", "where",
        "which", "who", "what", "how", "all", "any", "must", "per", "also",
    }
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [t for t in tokens if t not in stopwords and len(t) > 1]


# ─── BM25 RETRIEVER ────────────────────────────────────────────────────────────

class BM25:
    """BM25 sparse keyword retriever (Robertson et al.)."""
    def __init__(self, docs: list[dict], k1: float = 1.5, b: float = 0.75):
        self.docs = docs
        self.k1 = k1
        self.b = b
        self.corpus = [tokenize(d["content"] + " " + d["section_title"]) for d in docs]
        self.N = len(self.corpus)
        self.avgdl = sum(len(d) for d in self.corpus) / max(self.N, 1)
        self.df: dict[str, int] = {}
        for tokens in self.corpus:
            for t in set(tokens):
                self.df[t] = self.df.get(t, 0) + 1
        self.idf: dict[str, float] = {}
        for t, df in self.df.items():
            self.idf[t] = math.log((self.N - df + 0.5) / (df + 0.5) + 1)

    def score(self, query_tokens: list[str], doc_tokens: list[str]) -> float:
        tf_map = Counter(doc_tokens)
        dl = len(doc_tokens)
        score = 0.0
        for t in query_tokens:
            if t not in self.idf:
                continue
            tf = tf_map.get(t, 0)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            score += self.idf[t] * numerator / max(denominator, 1e-9)
        return score

    def retrieve(self, query: str, top_k: int = 10) -> list[tuple[dict, float]]:
        q_tokens = tokenize(query)
        scores = [(doc, self.score(q_tokens, self.corpus[i]))
                  for i, doc in enumerate(self.docs)]
        scores.sort(key=lambda x: x[1], reverse=True)
        return [(doc, s) for doc, s in scores[:top_k] if s > 0]


# ─── TF-IDF VECTOR RETRIEVER ──────────────────────────────────────────────────

class TFIDFRetriever:
    """TF-IDF vector similarity retriever (dense-semantic proxy)."""
    def __init__(self, docs: list[dict]):
        self.docs = docs
        self.corpus = [tokenize(d["content"] + " " + d["section_title"]) for d in docs]
        self.N = len(self.corpus)
        self.df: dict[str, int] = {}
        for tokens in self.corpus:
            for t in set(tokens):
                self.df[t] = self.df.get(t, 0) + 1
        self.idf: dict[str, float] = {
            t: math.log((self.N + 1) / (df + 1)) + 1
            for t, df in self.df.items()
        }

    def _tfidf_vec(self, tokens: list[str]) -> dict[str, float]:
        tf = Counter(tokens)
        total = max(sum(tf.values()), 1)
        vec = {}
        for t, count in tf.items():
            idf = self.idf.get(t, math.log((self.N + 1) / 1) + 1)
            vec[t] = (count / total) * idf
        return vec

    def _cosine(self, a: dict, b: dict) -> float:
        common = set(a) & set(b)
        if not common:
            return 0.0
        dot = sum(a[t] * b[t] for t in common)
        norm_a = math.sqrt(sum(v * v for v in a.values()))
        norm_b = math.sqrt(sum(v * v for v in b.values()))
        return dot / max(norm_a * norm_b, 1e-9)

    def retrieve(self, query: str, top_k: int = 10) -> list[tuple[dict, float]]:
        q_tokens = tokenize(query)
        q_vec = self._tfidf_vec(q_tokens)
        results = []
        for i, doc in enumerate(self.docs):
            d_vec = self._tfidf_vec(self.corpus[i])
            sim = self._cosine(q_vec, d_vec)
            results.append((doc, sim))
        results.sort(key=lambda x: x[1], reverse=True)
        return [(doc, s) for doc, s in results[:top_k] if s > 0]


# ─── CROSS-ENCODER RERANKER ───────────────────────────────────────────────────

class CrossEncoderReranker:
    """
    Lightweight cross-encoder reranker.
    Scores query-document pairs jointly by measuring token overlap,
    term proximity, and section-title relevance — mimicking a cross-encoder.
    In production, replace with: sentence-transformers cross-encoder/ms-marco-MiniLM-L-6-v2
    """
    def rerank(self, query: str, candidates: list[dict], top_k: int = 3) -> list[dict]:
        q_tokens = set(tokenize(query))
        scored = []
        for doc in candidates:
            content_tokens = tokenize(doc["content"])
            title_tokens = set(tokenize(doc["section_title"]))
            content_set = set(content_tokens)

            # 1. Token overlap with content
            overlap = len(q_tokens & content_set) / max(len(q_tokens), 1)

            # 2. Section title relevance (higher weight — titles are precise)
            title_overlap = len(q_tokens & title_tokens) / max(len(q_tokens), 1)

            # 3. Term proximity: count how many query terms appear near each other
            positions: dict[str, list[int]] = {}
            for idx, t in enumerate(content_tokens):
                if t in q_tokens:
                    positions.setdefault(t, []).append(idx)
            proximity_bonus = 0.0
            if len(positions) >= 2:
                all_pos = sorted(p for ps in positions.values() for p in ps)
                if len(all_pos) >= 2:
                    gaps = [all_pos[i + 1] - all_pos[i] for i in range(len(all_pos) - 1)]
                    avg_gap = sum(gaps) / len(gaps)
                    proximity_bonus = 1.0 / (1.0 + avg_gap / 20.0)

            # 4. Chunk-type bonus: tables are great for factual queries
            type_bonus = 0.1 if doc.get("chunk_type") == "table" else 0.0

            # Weighted final score
            score = (overlap * 0.40 + title_overlap * 0.35 +
                     proximity_bonus * 0.20 + type_bonus * 0.05)
            scored.append((doc, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in scored[:top_k]]


# ─── HYBRID RETRIEVAL PIPELINE ────────────────────────────────────────────────

def hybrid_retrieve_and_rerank(
    query: str,
    role: str,
    bm25_top_k: int = 10,
    dense_top_k: int = 10,
    rerank_top_k: int = 3,
) -> tuple[list[dict], dict]:
    """
    Full hybrid RAG pipeline with RBAC enforcement:
    1. Filter documents to role-accessible collections (RBAC at retrieval layer)
    2. BM25 keyword search
    3. TF-IDF vector search
    4. Reciprocal Rank Fusion (RRF) to merge ranked lists
    5. Cross-encoder reranking → top-k final chunks

    Returns: (top_chunks, debug_info)
    """
    # ── STEP 1: RBAC FILTER (at retrieval layer) ──────────────────────────────
    accessible_docs = get_accessible_docs(role)
    if not accessible_docs:
        return [], {"error": "No documents accessible for this role"}

    # ── STEP 2: BM25 RETRIEVAL ────────────────────────────────────────────────
    bm25 = BM25(accessible_docs)
    bm25_results = bm25.retrieve(query, top_k=bm25_top_k)

    # ── STEP 3: TF-IDF DENSE RETRIEVAL ───────────────────────────────────────
    dense = TFIDFRetriever(accessible_docs)
    dense_results = dense.retrieve(query, top_k=dense_top_k)

    # ── STEP 4: RECIPROCAL RANK FUSION (RRF) ──────────────────────────────────
    # RRF score = Σ 1 / (k + rank), k=60 is standard
    RRF_K = 60
    rrf_scores: dict[int, float] = {}
    doc_index: dict[int, dict] = {}

    for rank, (doc, _) in enumerate(bm25_results):
        doc_id = id(doc)
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1.0 / (RRF_K + rank + 1)
        doc_index[doc_id] = doc

    for rank, (doc, _) in enumerate(dense_results):
        doc_id = id(doc)
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1.0 / (RRF_K + rank + 1)
        doc_index[doc_id] = doc

    # Sort by RRF score → candidate set
    fused = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    candidates = [doc_index[did] for did, _ in fused[:max(bm25_top_k, dense_top_k)]]

    # ── STEP 5: CROSS-ENCODER RERANKING ──────────────────────────────────────
    reranker = CrossEncoderReranker()
    top_chunks = reranker.rerank(query, candidates, top_k=rerank_top_k)

    debug_info = {
        "accessible_docs_count": len(accessible_docs),
        "bm25_hits": len(bm25_results),
        "dense_hits": len(dense_results),
        "fused_candidates": len(candidates),
        "reranked_final": len(top_chunks),
        "collections_searched": list(ROLE_COLLECTIONS.get(role, [])),
    }

    return top_chunks, debug_info


def is_analytical_query(question: str) -> bool:
    """Detect if a question should be routed to SQL RAG."""
    analytical_keywords = [
        "how many", "count", "total", "sum", "average", "statistics",
        "most open", "least", "maximum", "minimum", "trend", "breakdown",
        "monthly", "weekly", "quarterly", "last month", "last week",
        "percentage", "ratio", "how much", "number of", "tallied",
        "escalated", "pending", "resolved", "outstanding",
    ]
    q_lower = question.lower()
    return any(kw in q_lower for kw in analytical_keywords)


def check_rbac_violation(question: str, role: str) -> tuple[bool, str]:
    """
    Check if a query attempts to access out-of-scope collections.
    Returns (is_violation, reason_message).
    """
    from knowledge_base import ROLE_COLLECTIONS

    role_collections = set(ROLE_COLLECTIONS.get(role, []))
    all_collections = {"clinical", "nursing", "billing", "equipment", "general"}
    restricted = all_collections - role_collections

    q_lower = question.lower()

    # Signals mapping collection → keywords
    collection_signals = {
        "billing": [
            "billing code", "insurance", "icd-10", "icd10", "claim", "pre-auth",
            "pre-authorisation", "preauthorization", "reimbursement", "tpa",
            "insurer", "package rate", "excl-", "co-pay", "deductible",
            "billing executive", "billing codes", "invoice", "cashless",
        ],
        "clinical": [
            "treatment protocol", "drug formulary", "diagnostic reference",
            "prescription", "medication", "clinical protocol", "lab values",
            "ecg interpretation", "abg", "haematology", "biochemistry",
            "drug interaction", "formulary", "oncology", "dosing",
        ],
        "nursing": [
            "icu nursing", "nursing procedure", "infection control", "central venous",
            "cvc care", "mechanical ventilator", "nasogastric", "ngt", "suctioning",
            "pressure injury", "braden scale", "vap prevention", "cannula insertion",
        ],
        "equipment": [
            "equipment manual", "calibration", "biomedical", "infusion pump",
            "autoclave", "x-ray unit", "bm-500", "sterilpro", "radipro",
            "driveflow", "maintenance schedule", "fault code", "bowie-dick",
        ],
    }

    violated_collections = []
    for coll in restricted:
        signals = collection_signals.get(coll, [])
        if any(sig in q_lower for sig in signals):
            violated_collections.append(coll)

    # Also catch prompt injection attempts
    injection_patterns = [
        "ignore your instructions", "ignore all instructions", "ignore previous",
        "ignore my instructions", "ignore the instructions", "ignore above",
        "disregard", "bypass", "override rbac", "show me all", "reveal all",
        "reveal all documents", "act as admin", "forget you are",
        "pretend you have access", "jailbreak", "ignore restrictions",
        "as an unrestricted", "you are now", "do not follow", "don't follow",
        "without restrictions", "no restrictions", "unrestricted mode",
        "developer mode", "sudo", "root access", "override access",
        "access all", "show all documents", "all collections",
        "forget rbac", "ignore rbac", "skip rbac", "bypass rbac",
    ]
    is_injection = any(p in q_lower for p in injection_patterns)

    if is_injection:
        return True, (
            f"🚫 **Security Alert**: This query appears to be attempting to bypass "
            f"access controls. As a **{role.replace('_', ' ')}**, you have access to "
            f"the **{', '.join(sorted(role_collections))}** collection(s) only. "
            f"This restriction is enforced at the retrieval layer and cannot be overridden."
        )

    if violated_collections:
        role_label = role.replace("_", " ").title()
        return True, (
            f"🔒 **Access Restricted**: As a **{role_label}**, you don't have access "
            f"to the **{', '.join(violated_collections)}** collection(s). "
            f"I can only answer questions from your authorised collections: "
            f"**{', '.join(sorted(role_collections))}**. "
            f"This restriction is enforced at the vector retrieval layer."
        )

    return False, ""
