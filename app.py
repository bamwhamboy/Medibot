"""
MediBot — Streamlit App · MediAssist Health Network
Light, clinical-clean UI redesign · single shared password, persistent Groq key
"""
import os, re, sqlite3, requests
import streamlit as st

from knowledge_base import ROLE_COLLECTIONS, DOCUMENTS
from retrieval import hybrid_retrieve_and_rerank, is_analytical_query, check_rbac_violation
from sql_rag import create_database, DB_PATH, get_db_schema, extract_sql

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediBot · MediAssist AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none;}

/* ── TOKENS ──
   Ink      #1A1F2B   primary text
   Slate    #64748B   secondary text
   Teal     #0F6E5C   primary accent (trust / clinical)
   Coral    #E8623D   alert / blocked
   Canvas   #FAFAF8   app background
   Card     #FFFFFF   surfaces
   Line     #E7E4DC   hairline borders
*/

.stApp{
  background:#FAFAF8;
  min-height:100vh; color:#1A1F2B;
}

section[data-testid="stSidebar"]{
  background:#FFFFFF !important;
  border-right:1px solid #E7E4DC !important;
  box-shadow:none !important;
}
section[data-testid="stSidebar"]>div{padding-top:0 !important;}
section[data-testid="stSidebar"] *{color:#475569 !important;}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] strong,
section[data-testid="stSidebar"] b{color:#1A1F2B !important;}
section[data-testid="stSidebar"] hr{border-color:#E7E4DC !important;}

/* Sidebar logo */
.sb-logo{background:#FFFFFF;border-bottom:1px solid #E7E4DC;padding:22px 18px 18px;text-align:center;}
.sb-icon{width:46px;height:46px;background:#0F6E5C;
  border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:21px;
  margin:0 auto 10px;box-shadow:0 4px 14px rgba(15,110,92,.22);}
.sb-title{font-family:'Fraunces',serif;font-size:21px;font-weight:700;color:#1A1F2B !important;letter-spacing:-.3px;}
.sb-sub{font-size:10.5px;color:#94A3B8 !important;letter-spacing:1.6px;text-transform:uppercase;margin-top:3px;font-weight:600;}

/* Sidebar user card */
.sb-user-card{margin:14px 14px 0;background:#FAFAF8;
  border:1px solid #E7E4DC;border-radius:14px;padding:13px;}
.sb-av{width:36px;height:36px;border-radius:9px;display:flex;align-items:center;
  justify-content:center;font-size:14px;font-weight:700;color:white;flex-shrink:0;}
.sb-uname{font-size:14px;font-weight:600;color:#1A1F2B !important;}
.sb-udept{font-size:12px;color:#94A3B8 !important;margin-top:1px;}
.online-dot{width:6px;height:6px;border-radius:50%;background:#0F9D6C;
  box-shadow:0 0 0 2px rgba(15,157,108,.18);display:inline-block;}

/* Role badges (ID-card tab style) */
.role-badge{display:inline-flex;align-items:center;gap:5px;padding:4px 12px;
  border-radius:6px;font-size:11.5px;font-weight:700;letter-spacing:.5px;
  text-transform:uppercase;margin-top:6px;border-left:3px solid;}
.badge-doctor{background:#EAF7F2;color:#0F6E5C !important;border-color:#0F6E5C;}
.badge-nurse{background:#EAF1FB;color:#2563EB !important;border-color:#2563EB;}
.badge-billing_executive{background:#FDF3E7;color:#B7791F !important;border-color:#B7791F;}
.badge-technician{background:#F3EEFB;color:#7C3AED !important;border-color:#7C3AED;}
.badge-admin{background:#FCEEEA;color:#C2410C !important;border-color:#C2410C;}

/* Collection chips */
.coll-chip{display:flex;align-items:center;gap:7px;padding:7px 13px;border-radius:8px;
  font-size:13px;font-weight:600;margin:4px 0;border:1px solid;}
.coll-general{background:#F8FAFC;border-color:#E2E8F0;color:#64748B !important;}
.coll-clinical{background:#EAF7F2;border-color:#CDEEE1;color:#0F6E5C !important;}
.coll-nursing{background:#EAF1FB;border-color:#CFE0FA;color:#2563EB !important;}
.coll-billing{background:#FDF3E7;border-color:#F5DFB8;color:#B7791F !important;}
.coll-equipment{background:#F3EEFB;border-color:#E1D4FA;color:#7C3AED !important;}
.coll-locked{background:#F8FAFC;border-color:#EDEDED;color:#C2C7CF !important;}

/* Stats */
.stat-pill{display:flex;align-items:center;gap:6px;padding:5px 0;font-size:13px;color:#64748B !important;}
.stat-pill span{color:#0F6E5C !important;font-weight:700;}

/* Login */
.login-hero{text-align:center;padding:44px 20px 26px;}
.login-icon-ring{width:68px;height:68px;background:#0F6E5C;
  border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:30px;
  margin:0 auto 18px;box-shadow:0 10px 28px rgba(15,110,92,.22);}
.login-title{font-family:'Fraunces',serif;font-size:42px;font-weight:700;color:#1A1F2B;letter-spacing:-1.2px;}
.login-sub{font-size:15px;color:#64748B;margin-top:9px;line-height:1.6;}
.login-features{display:flex;justify-content:center;gap:9px;flex-wrap:wrap;margin-top:16px;}
.login-feat-chip{background:#FFFFFF;border:1px solid #E7E4DC;
  border-radius:20px;padding:6px 14px;font-size:13px;font-weight:600;color:#475569;}
.key-panel{background:#FDF3E7;border:1px solid #F5DFB8;
  border-radius:12px;padding:13px 17px;margin-bottom:16px;}
.key-panel-title{font-size:14px;font-weight:700;color:#B7791F;}
.key-panel-sub{font-size:13px;color:#92621A;margin-top:3px;}
.key-panel-sub a{color:#B7791F;font-weight:600;}
.pwd-banner{background:#EAF7F2;border:1px solid #CDEEE1;
  border-radius:10px;padding:11px 15px;margin-bottom:16px;font-size:14px;color:#0F6E5C;
  display:flex;align-items:center;gap:8px;}
.user-card{background:#FFFFFF;border:1px solid #E7E4DC;
  border-radius:14px;padding:16px;margin:6px 0;position:relative;overflow:hidden;
  transition:box-shadow .15s ease, transform .15s ease;}
.user-card:hover{box-shadow:0 8px 20px rgba(26,31,43,.07);transform:translateY(-1px);}
.user-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;}
.uc-doctor::before{background:#0F6E5C;}
.uc-nurse::before{background:#2563EB;}
.uc-billing::before{background:#B7791F;}
.uc-technician::before{background:#7C3AED;}
.uc-admin::before{background:#C2410C;}
.uc-icon{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;
  justify-content:center;font-size:19px;margin-bottom:8px;}
.uc-doctor-bg{background:#EAF7F2;}.uc-nurse-bg{background:#EAF1FB;}
.uc-billing-bg{background:#FDF3E7;}.uc-technician-bg{background:#F3EEFB;}
.uc-admin-bg{background:#FCEEEA;}
.uc-name{font-size:15px;font-weight:700;color:#1A1F2B;}
.uc-dept{font-size:12px;color:#94A3B8;margin-top:1px;}
.uc-creds{font-size:12.5px;font-family:'JetBrains Mono',monospace;color:#475569;margin-top:9px;
  padding:5px 9px;background:#FAFAF8;border-radius:6px;
  border:1px solid #EDEDED;}
.uc-access{font-size:12px;color:#94A3B8;margin-top:5px;}

/* Messages */
.msg-row-user{display:flex;justify-content:flex-end;margin:14px 0;}
.msg-row-bot{display:flex;justify-content:flex-start;align-items:flex-start;gap:10px;margin:14px 0;}
.msg-row-blocked{display:flex;justify-content:flex-start;align-items:flex-start;gap:10px;margin:14px 0;}

.bubble-user{background:#1A1F2B;color:#FAFAF8;
  padding:12px 17px;border-radius:16px 16px 4px 16px;max-width:70%;font-size:15px;
  line-height:1.65;word-wrap:break-word;}
.bot-avatar{width:34px;height:34px;background:#0F6E5C;
  border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;
  flex-shrink:0;margin-top:2px;}
.bubble-bot{background:#FFFFFF;color:#1A1F2B;padding:15px 19px;
  border-radius:4px 16px 16px 16px;max-width:80%;font-size:15px;line-height:1.78;
  border:1px solid #E7E4DC;word-wrap:break-word;}
.bubble-bot strong{color:#0F6E5C;}
.blocked-avatar{width:34px;height:34px;background:#E8623D;
  border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:15px;
  flex-shrink:0;margin-top:2px;}
.bubble-blocked{background:#FCEEEA;color:#9A3412;padding:13px 17px;
  border-radius:4px 16px 16px 16px;max-width:80%;font-size:15px;line-height:1.68;
  border:1px solid #F6D2C2;}
.bubble-blocked strong{color:#C2410C;}
.sources-row{margin-top:12px;padding-top:10px;border-top:1px solid #EDEDED;}
.src-chip{display:inline-flex;align-items:center;gap:4px;background:#EAF7F2;
  color:#0F6E5C;border:1px solid #CDEEE1;border-radius:7px;
  padding:5px 11px;font-size:12px;font-weight:600;margin:2px 3px;}
.ret-badge{display:inline-flex;align-items:center;gap:4px;padding:4px 11px;border-radius:20px;
  font-size:12px;font-weight:700;margin-top:8px;}
.ret-hybrid{background:#EAF1FB;color:#2563EB;border:1px solid #CFE0FA;}
.ret-sql{background:#F3EEFB;color:#7C3AED;border:1px solid #E1D4FA;}
.sql-box{margin-top:10px;background:#1A1F2B;border-radius:9px;padding:11px 14px;
  font-size:13px;font-family:'JetBrains Mono',monospace;color:#5EEAD4;
  border:1px solid #2A3142;overflow-x:auto;line-height:1.6;}
.welcome-banner{background:#FFFFFF;border:1px solid #E7E4DC;
  border-radius:14px;padding:15px 19px;display:flex;align-items:center;gap:14px;margin-bottom:10px;}
.welcome-icon{font-size:26px;flex-shrink:0;}
.welcome-text{font-size:14.5px;color:#475569;line-height:1.6;}
.welcome-text strong{color:#0F6E5C;}

/* Input */
.stTextInput>div>div>input{
  border-radius:12px !important;border:1.5px solid #E7E4DC !important;
  padding:12px 16px !important;font-size:15px !important;font-family:'Inter',sans-serif !important;
  background:#FFFFFF !important;color:#1A1F2B !important;transition:all .15s !important;}
.stTextInput>div>div>input::placeholder{color:#B0B7C3 !important;}
.stTextInput>div>div>input:focus{border-color:#0F6E5C !important;
  box-shadow:0 0 0 3px rgba(15,110,92,.10) !important;}
.stButton>button{border-radius:10px !important;font-family:'Inter',sans-serif !important;font-weight:600 !important;transition:all .15s !important;}
.stButton>button[kind="primary"]{background:#0F6E5C !important;
  color:white !important;border:none !important;box-shadow:0 3px 10px rgba(15,110,92,.25) !important;}
.stButton>button[kind="primary"]:hover{background:#0C5847 !important;
  transform:translateY(-1px) !important;box-shadow:0 5px 14px rgba(15,110,92,.32) !important;}
.stButton>button[kind="secondary"]{background:#FFFFFF !important;
  border:1px solid #E7E4DC !important;color:#475569 !important;}
.stButton>button[kind="secondary"]:hover{background:#EAF7F2 !important;
  border-color:#CDEEE1 !important;color:#0F6E5C !important;}
.stSelectbox>div>div{border-radius:9px !important;border:1px solid #E7E4DC !important;
  background:#FFFFFF !important;}
.stAlert{border-radius:11px !important;}
div[data-testid="stInfo"]{background:#EAF1FB !important;border-color:#CFE0FA !important;color:#1D4ED8 !important;}
div[data-testid="stSuccess"]{background:#EAF7F2 !important;border-color:#CDEEE1 !important;color:#0F6E5C !important;}
div[data-testid="stWarning"]{background:#FDF3E7 !important;border-color:#F5DFB8 !important;color:#92621A !important;}
div[data-testid="stError"]{background:#FCEEEA !important;border-color:#F6D2C2 !important;color:#C2410C !important;}
.streamlit-expanderHeader{background:#FFFFFF !important;border-radius:9px !important;
  border:1px solid #E7E4DC !important;color:#475569 !important;}
.stToggle>label{font-size:12px !important;color:#64748B !important;}
.sb-signout button{background:#FCEEEA !important;
  border:1px solid #F6D2C2 !important;color:#C2410C !important;border-radius:9px !important;}
.sb-signout button:hover{background:#F6D2C2 !important;border-color:#E8623D !important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:#E7E4DC;border-radius:4px;}
::-webkit-scrollbar-thumb:hover{background:#CBD5E1;}
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ─────────────────────────────────────────────────────────────────
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"
SHARED_PASSWORD = "medibot123"  # ← single password for all accounts

USERS = {
    "dr.mehta":     {"role":"doctor",            "display":"Dr. Arjun Mehta",   "dept":"Clinical Department",     "initials":"AM","color":"#0F6E5C"},
    "nurse.priya":  {"role":"nurse",              "display":"Nurse Priya Singh", "dept":"Critical Care Unit",      "initials":"PS","color":"#2563EB"},
    "billing.ravi": {"role":"billing_executive",  "display":"Ravi Kumar",        "dept":"Billing & Insurance",     "initials":"RK","color":"#B7791F"},
    "tech.anand":   {"role":"technician",         "display":"Anand Pillai",      "dept":"Biomedical Engineering",  "initials":"AP","color":"#7C3AED"},
    "admin.sys":    {"role":"admin",              "display":"Admin System",      "dept":"Executive / IT",          "initials":"AS","color":"#C2410C"},
}

ROLE_META = {
    "doctor":            {"icon":"👨‍⚕️","label":"Doctor",       "color":"#0F6E5C","bg_class":"uc-doctor-bg",     "card_class":"uc-doctor",     "badge":"badge-doctor"},
    "nurse":              {"icon":"👩‍⚕️","label":"Nurse",        "color":"#2563EB","bg_class":"uc-nurse-bg",      "card_class":"uc-nurse",      "badge":"badge-nurse"},
    "billing_executive":  {"icon":"📋","label":"Billing Exec", "color":"#B7791F","bg_class":"uc-billing-bg",    "card_class":"uc-billing",    "badge":"badge-billing_executive"},
    "technician":         {"icon":"🔧","label":"Technician",   "color":"#7C3AED","bg_class":"uc-technician-bg", "card_class":"uc-technician", "badge":"badge-technician"},
    "admin":              {"icon":"🛡️","label":"Admin",        "color":"#C2410C","bg_class":"uc-admin-bg",      "card_class":"uc-admin",      "badge":"badge-admin"},
}

COLLECTION_META = {
    "general":   {"icon":"📚","label":"General",   "chip":"coll-general"},
    "clinical":  {"icon":"🩺","label":"Clinical",  "chip":"coll-clinical"},
    "nursing":   {"icon":"💉","label":"Nursing",   "chip":"coll-nursing"},
    "billing":   {"icon":"📊","label":"Billing",   "chip":"coll-billing"},
    "equipment": {"icon":"⚙️","label":"Equipment","chip":"coll-equipment"},
}

QUICK_QUESTIONS = {
    "doctor": [
        "What is the NSTEMI treatment protocol?",
        "Paracetamol dose for a 12 kg child?",
        "How to manage COPD exacerbation?",
        "Normal troponin I reference range?",
        "Azithromycin drug interactions?",
    ],
    "nurse": [
        "CVC dressing change procedure?",
        "IV cannula size for child under 5 kg?",
        "PPE for aerosol-generating procedures?",
        "Gastric residual volume above 400 mL — what to do?",
        "Pressure injury prevention bundle?",
    ],
    "billing_executive": [
        "Emergency cashless pre-auth deadline?",
        "NSTEMI ICD-10 code and package rate?",
        "How to respond to EXCL-01 rejection?",
        "How many claims are currently escalated?",
        "Billing executive KPI targets?",
    ],
    "technician": [
        "DriveFlow IP-200 fault code F-12 action?",
        "Autoclave Bowie-Dick test procedure?",
        "BM-500 monitor calibration schedule?",
        "Which fault codes require equipment removal?",
        "RadiPro MX-150 radiation safety rules?",
    ],
    "admin": [
        "How many claims are escalated right now?",
        "Open maintenance tickets by equipment category?",
        "NSTEMI treatment protocol?",
        "Staff leave entitlements — clinical vs non-clinical?",
        "Which fault codes require immediate equipment removal?",
    ],
}

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
def _init():
    defaults = {
        "logged_in":False, "username":None, "role":None,
        "display_name":None, "dept":None, "initials":None,
        "user_color":"#2563EB", "messages":[], "show_debug":False,
        "api_key":"", "selected_model":MODEL,
        "run_question":"",  # question to process this frame
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
_init()

# ─── Auto-load API key (env → Streamlit secrets) ──────────────────────────────
if not st.session_state.api_key:
    _k = os.environ.get("GROQ_API_KEY","").strip()
    if not _k:
        try: _k = st.secrets.get("GROQ_API_KEY","").strip()
        except: pass
    if _k:
        st.session_state.api_key = _k

# ─── DB ────────────────────────────────────────────────────────────────────────
if not os.path.exists(DB_PATH):
    create_database()

# ─── LLM CALL ─────────────────────────────────────────────────────────────────
def call_llm(system:str, user:str, max_tokens:int=1200) -> str:
    key = st.session_state.api_key.strip()
    if not key:
        return "⚠️ No Groq API key. Enter it on the login screen."
    model = st.session_state.get("selected_model", MODEL)
    try:
        r = requests.post(
            GROQ_API_URL,
            headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},
            json={"model":model,"max_tokens":max_tokens,"temperature":0.2,
                  "messages":[{"role":"system","content":system},{"role":"user","content":user}]},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except requests.HTTPError:
        try: msg = r.json().get("error",{}).get("message","HTTP error")
        except: msg = r.text[:200]
        return f"⚠️ Groq Error {r.status_code}: {msg}"
    except Exception as e:
        return f"⚠️ Request failed: {e}"

# ─── SQL RAG ──────────────────────────────────────────────────────────────────
def run_sql_rag(question:str) -> dict:
    sql = extract_sql(call_llm(
        "You are a SQLite expert. Return ONLY the SQL query — no explanation, no markdown fences.",
        f"{get_db_schema()}\n\nQuestion: {question}\n\nSQL:",
        max_tokens=400,
    ))
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        conn.close()
        if not rows:
            results_str = "Query returned no results."
        else:
            lines = [" | ".join(cols), "─"*max(40,len(" | ".join(cols)))]
            for row in rows:
                lines.append(" | ".join(str(v) if v is not None else "—" for v in row))
            results_str = "\n".join(lines)
    except sqlite3.Error as e:
        return {"answer":f"⚠️ DB error: {e}\nSQL tried: `{sql}`","sql_query":sql,"raw_results":None}

    answer = call_llm(
        "You are MediBot for MediAssist. Answer clearly from SQL results. Use bullets for lists.",
        f'Question: "{question}"\n\nSQL:\n{sql}\n\nResults:\n{results_str}\n\nAnswer:',
        max_tokens=700,
    )
    return {"answer":answer,"sql_query":sql,"raw_results":results_str}

# ─── HYBRID RAG ───────────────────────────────────────────────────────────────
def run_hybrid_rag(question:str, role:str) -> dict:
    chunks, debug = hybrid_retrieve_and_rerank(question, role, rerank_top_k=4)
    if not chunks:
        return {"answer":"I couldn't find relevant information in your authorised collections. Please try rephrasing.",
                 "sources":[],"debug":debug}

    context = "\n\n---\n\n".join(
        f"[Source {i}: {c['source_document']} — {c['section_title']}]\n{c['content']}"
        for i,c in enumerate(chunks,1)
    )
    meta = ROLE_META.get(role,{})
    answer = call_llm(
        f"""You are MediBot, internal AI assistant for MediAssist Health Network.
User: {st.session_state.display_name} | Role: {meta.get('label',role)} | Collections: {', '.join(ROLE_COLLECTIONS.get(role,[]))}
Answer ONLY from the document context below. Be precise and professional.
Include exact codes, dosages, and values. Use bullet points for procedures.
Do NOT hallucinate. Do NOT reveal information from restricted collections.

DOCUMENT CONTEXT:
{context}""",
        question, max_tokens=1200,
    )
    return {
        "answer": answer,
        "sources": [{"source_document":c["source_document"],
                     "section_title":c["section_title"],
                     "collection":c["collection"]} for c in chunks],
        "debug": debug,
    }

def run_rag(question:str, role:str) -> dict:
    if role in ("billing_executive","admin") and is_analytical_query(question):
        r = run_sql_rag(question)
        return {"answer":r["answer"],"retrieval_type":"sql_rag","sources":[],
                "sql_query":r.get("sql_query"),"raw_results":r.get("raw_results"),"debug":{}}
    r = run_hybrid_rag(question, role)
    return {"answer":r["answer"],"retrieval_type":"hybrid_rag",
            "sources":r.get("sources",[]),"debug":r.get("debug",{})}

# ─── PROCESS QUESTION (no spinner — caller wraps) ─────────────────────────────
def _process(question:str, role:str):
    st.session_state.messages.append({"role":"user","content":question})
    viol, msg = check_rbac_violation(question, role)
    if viol:
        st.session_state.messages.append({"role":"blocked","content":msg})
        return
    if not st.session_state.api_key.strip():
        st.session_state.messages.append({"role":"blocked",
            "content":"⚠️ No Groq API key found. Please sign out and enter your key."})
        return
    try:
        st.session_state.messages.append({"role":"assistant","data":run_rag(question,role)})
    except Exception as e:
        st.session_state.messages.append({"role":"blocked","content":f"⚠️ Error: {e}"})

# ═══════════════════════════════════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════════════════════════════════
def render_login():
    _, mid, _ = st.columns([0.8,2.4,0.8])
    with mid:
        st.markdown("""
        <div class="login-hero">
            <div class="login-icon-ring">🏥</div>
            <div class="login-title">MediBot</div>
            <div class="login-sub">
                MediAssist Health Network · Internal AI Assistant<br>
                <span style="font-size:11.5px;color:#94A3B8;">Powered by Groq ⚡ LLaMA-3.3-70B</span>
            </div>
            <div class="login-features">
                <span class="login-feat-chip">🔍 Hybrid RAG</span>
                <span class="login-feat-chip">🔒 Role-Based Access</span>
                <span class="login-feat-chip">🗄️ SQL Analytics</span>
                <span class="login-feat-chip">📄 Source Citations</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── API Key (hidden if already loaded from env/secrets) ──
        if not st.session_state.api_key:
            st.markdown("""
            <div class="key-panel">
                <div class="key-panel-title">🔑 Step 1 — Enter your Groq API Key</div>
                <div class="key-panel-sub">
                    Free at <a href="https://console.groq.com/keys" target="_blank">console.groq.com/keys</a>
                    — 14,400 free requests/day
                </div>
            </div>
            """, unsafe_allow_html=True)
            typed_key = st.text_input(
                "Groq API Key", type="password",
                placeholder="gsk_...", label_visibility="collapsed",
                key="key_field",
            )
            if typed_key.strip():
                st.session_state.api_key = typed_key.strip()
                st.rerun()
        else:
            st.success(f"⚡ Groq key ready · Model: {MODEL}", icon="✅")

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # ── Shared password banner ──
        st.markdown(f"""
        <div class="pwd-banner">
            🔐&nbsp; Password for <strong>all accounts</strong>:&nbsp;
            <code style="background:#1A1F2B;color:#5EEAD4;padding:2px 9px;
            border-radius:6px;font-size:13px;letter-spacing:1px;">{SHARED_PASSWORD}</code>
        </div>
        """, unsafe_allow_html=True)

        # ── Username & password form ──
        with st.form("login_form"):
            uname_in = st.text_input("Username", placeholder="e.g. dr.mehta")
            pwd_in   = st.text_input("Password", type="password", placeholder="medibot123")
            login_btn = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

        if login_btn:
            uname_in = uname_in.strip().lower()
            if uname_in not in USERS:
                st.error("❌ Username not found. Try: dr.mehta, nurse.priya, billing.ravi, tech.anand, admin.sys")
            elif pwd_in != SHARED_PASSWORD:
                st.error("❌ Wrong password. Password for all accounts is: medibot123")
            elif not st.session_state.api_key:
                st.error("⚠️ Please enter your Groq API key above first.")
            else:
                info = USERS[uname_in]
                st.session_state.update({
                    "logged_in":True, "username":uname_in,
                    "role":info["role"], "display_name":info["display"],
                    "dept":info["dept"], "initials":info["initials"],
                    "user_color":info["color"], "messages":[], "run_question":"",
                })
                st.rerun()

        # ── Account reference table ──
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px;font-weight:700;color:#94A3B8;letter-spacing:.9px;text-transform:uppercase;margin-bottom:9px;">👤 Demo Accounts</div>', unsafe_allow_html=True)

        users_list = list(USERS.items())
        col_a, col_b = st.columns(2)
        for i,(uname,info) in enumerate(users_list):
            role = info["role"]
            meta = ROLE_META[role]
            colls = ROLE_COLLECTIONS.get(role,[])
            with (col_a if i%2==0 else col_b):
                st.markdown(f"""
                <div class="user-card {meta['card_class']}">
                    <div class="uc-icon {meta['bg_class']}">{meta['icon']}</div>
                    <div class="uc-name">{info['display']}</div>
                    <div class="uc-dept">{info['dept']}</div>
                    <span class="role-badge {meta['badge']}">{meta['label']}</span>
                    <div class="uc-creds">👤 {uname}</div>
                    <div class="uc-access">🔓 {" · ".join(colls)}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center;margin-top:20px;font-size:11px;color:#B0B7C3;">
            🔒 RBAC enforced at retrieval layer &nbsp;·&nbsp; 54 chunks &nbsp;·&nbsp; 30 claims &nbsp;·&nbsp; 21 tickets in DB
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════
def render_sidebar():
    role = st.session_state.role
    meta = ROLE_META[role]
    colls = ROLE_COLLECTIONS.get(role,[])
    locked = sorted(set(COLLECTION_META)-set(colls))
    n_chunks = sum(1 for d in DOCUMENTS if d["collection"] in colls)

    with st.sidebar:
        st.markdown(f"""
        <div class="sb-logo">
            <div class="sb-icon">🏥</div>
            <div class="sb-title">MediBot</div>
            <div class="sb-sub">MediAssist Health Network</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sb-user-card">
            <div style="display:flex;align-items:center;gap:9px;margin-bottom:9px;">
                <div class="sb-av" style="background:{st.session_state.user_color};">
                    {st.session_state.initials}
                </div>
                <div>
                    <div class="sb-uname">{st.session_state.display_name}</div>
                    <div class="sb-udept">{st.session_state.dept}</div>
                </div>
            </div>
            <span class="role-badge {meta['badge']}">{meta['icon']} {meta['label']}</span>
            <div style="display:flex;align-items:center;gap:5px;margin-top:8px;font-size:10.5px;color:#94A3B8 !important;">
                <span class="online-dot"></span> Online
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:10px;font-weight:700;color:#94A3B8 !important;letter-spacing:1.1px;text-transform:uppercase;padding:3px 2px;">📂 Your Collections</div>', unsafe_allow_html=True)
        for c in colls:
            cm = COLLECTION_META[c]
            st.markdown(f'<div class="coll-chip {cm["chip"]}">{cm["icon"]} {cm["label"]}</div>', unsafe_allow_html=True)

        if locked:
            st.markdown('<div style="font-size:10px;font-weight:700;color:#C2C7CF !important;letter-spacing:1.1px;text-transform:uppercase;padding:9px 2px 4px;">🔒 Restricted</div>', unsafe_allow_html=True)
            for c in locked:
                cm = COLLECTION_META[c]
                st.markdown(f'<div class="coll-chip coll-locked">🚫 {cm["label"]}</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#FAFAF8;border:1px solid #E7E4DC;border-radius:10px;padding:11px 13px;">
            <div class="stat-pill">📄 <span>{n_chunks}</span> chunks accessible</div>
            <div class="stat-pill">🔍 BM25 + TF-IDF + RRF + Rerank</div>
            <div class="stat-pill">⚡ Groq · <span>LLaMA-3.3-70B</span></div>
            {"<div class='stat-pill'>🗄️ <span>SQL RAG enabled</span></div>" if role in ("billing_executive","admin") else ""}
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        model_map = {
            "llama-3.3-70b-versatile": "⚡ LLaMA 3.3 70B (Best)",
            "llama-3.1-8b-instant": "🚀 LLaMA 3.1 8B (Fastest)",
            "mixtral-8x7b-32768": "🌀 Mixtral 8x7B (32k ctx)",
            "gemma2-9b-it": "💎 Gemma2 9B (Light)",
        }
        chosen = st.selectbox("🤖 Model", list(model_map.values()), index=0)
        st.session_state.selected_model = [k for k,v in model_map.items() if v==chosen][0]

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        st.session_state.show_debug = st.toggle("🔬 Debug mode", value=st.session_state.show_debug)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="sb-signout">', unsafe_allow_html=True)
            if st.button("↩ Sign Out", use_container_width=True):
                st.session_state.update({
                    "logged_in":False,"username":None,"role":None,
                    "display_name":None,"dept":None,"initials":None,"messages":[],
                })
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# MESSAGE RENDERERS
# ═══════════════════════════════════════════════════════════════════════
def _fmt(text:str) -> str:
    """Minimal markdown→html for bot bubbles."""
    h = text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    h = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', h)
    h = h.replace("\n","<br>")
    return h

def render_user_msg(content:str):
    st.markdown(f'<div class="msg-row-user"><div class="bubble-user">{_fmt(content)}</div></div>',
                unsafe_allow_html=True)

def render_bot_msg(data:dict):
    answer_html = _fmt(data.get("answer",""))
    rtype = data.get("retrieval_type","hybrid_rag")
    blabel = "🔍 Hybrid RAG" if rtype=="hybrid_rag" else "🗄️ SQL RAG"
    bclass = "ret-hybrid" if rtype=="hybrid_rag" else "ret-sql"

    src_html = ""
    if data.get("sources"):
        chips = "".join(
            f'<span class="src-chip">📄 {s["source_document"]} · '
            f'{s["section_title"][:42]}{"…" if len(s["section_title"])>42 else ""}</span>'
            for s in data["sources"]
        )
        src_html = f'<div class="sources-row">{chips}</div>'

    sql_html = ""
    if data.get("sql_query"):
        q = data["sql_query"].replace("<","&lt;").replace(">","&gt;")
        sql_html = (f'<details style="margin-top:10px;"><summary style="font-size:11.5px;'
                    f'color:#94A3B8;cursor:pointer;font-weight:600;">🗄️ View SQL query</summary>'
                    f'<div class="sql-box">{q}</div></details>')

    # NOTE: built as a single unindented line on purpose — Streamlit's markdown
    # parser can mis-split indented multi-line HTML blocks and leak a stray
    # closing tag as literal text in its own block. Keeping this flat avoids that.
    html = ('<div class="msg-row-bot">'
            '<div class="bot-avatar">🏥</div>'
            '<div class="bubble-bot">'
            f'{answer_html}'
            f'{src_html}'
            f'<div style="margin-top:9px;"><span class="ret-badge {bclass}">{blabel}</span></div>'
            f'{sql_html}'
            '</div>'
            '</div>')
    st.markdown(html, unsafe_allow_html=True)

    if st.session_state.show_debug and data.get("debug"):
        with st.expander("🔬 Retrieval debug"):
            st.json(data["debug"])

def render_blocked_msg(content:str):
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content.replace("\n","<br>"))
    block = ('<div class="msg-row-blocked">'
             '<div class="blocked-avatar">🔒</div>'
             f'<div class="bubble-blocked">{html}</div>'
             '</div>')
    st.markdown(block, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# CHAT
# ═══════════════════════════════════════════════════════════════════════
def render_chat():
    role = st.session_state.role
    meta = ROLE_META[role]
    colls = ROLE_COLLECTIONS.get(role,[])

    # ── IMPORTANT: process run_question FIRST, before any rendering ──────────
    if st.session_state.get("run_question","").strip():
        q = st.session_state.run_question.strip()
        st.session_state.run_question = ""
        with st.spinner("⚡ Searching your authorised collections…"):
            _process(q, role)

    is_fresh = not st.session_state.messages

    # ── Header ──────────────────────────────────────────────────────────────
    COLL_BG = {"general":"#F8FAFC","clinical":"#EAF7F2","nursing":"#EAF1FB","billing":"#FDF3E7","equipment":"#F3EEFB"}
    COLL_FG = {"general":"#64748B","clinical":"#0F6E5C","nursing":"#2563EB","billing":"#B7791F","equipment":"#7C3AED"}

    h1, h2, h3 = st.columns([5,0.9,0.9])
    with h1:
        tags = " ".join(
            f'<span style="font-size:12.5px;background:{COLL_BG[c]};color:{COLL_FG[c]};'
            f'padding:3px 10px;border-radius:7px;margin-right:4px;font-weight:600;">{COLLECTION_META[c]["icon"]} {c.title()}</span>'
            for c in colls
        )
        st.markdown(f"""
        <div style="padding:12px 0 16px;border-bottom:1px solid #E7E4DC;margin-bottom:16px;">
            <div style="display:flex;align-items:center;gap:11px;">
                <div style="width:36px;height:36px;background:#0F6E5C;
                border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;">🏥</div>
                <div>
                    <div style="font-family:'Fraunces',serif;font-size:20px;font-weight:700;color:#1A1F2B;line-height:1.2;letter-spacing:-.3px;">
                        MediBot <span class="online-dot" style="margin-left:3px;"></span>
                        <span style="font-size:12px;font-weight:600;color:#0F9D6C;vertical-align:middle;">Online</span>
                    </div>
                    <div style="font-size:13px;color:#94A3B8;margin-top:3px;">
                        {meta['icon']} {st.session_state.display_name} &nbsp;·&nbsp; {tags}
                    </div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
    with h2:
        if st.button("← Back", help="Back to login screen"):
            st.session_state.update({
                "logged_in":False,"username":None,"role":None,
                "display_name":None,"dept":None,"initials":None,"messages":[],
            })
            st.rerun()
    with h3:
        if st.button("🗑️ Clear", help="Clear chat"):
            st.session_state.messages = []
            st.rerun()

    # ── Welcome banner ───────────────────────────────────────────────────────
    if is_fresh:
        coll_str = " ".join(f"{COLLECTION_META[c]['icon']} **{c.title()}**" for c in colls)
        sql_note = (" You also have **SQL RAG** — ask analytical questions about claims & equipment data."
                    if role in ("billing_executive","admin") else "")
        st.markdown(f"""
        <div class="welcome-banner">
            <div class="welcome-icon">{meta['icon']}</div>
            <div class="welcome-text">
                Welcome, <strong>{st.session_state.display_name}</strong>!
                Your authorised collections: {coll_str}.{sql_note}<br>
                <span style="font-size:11.5px;color:#0F6E5C;">Click a quick question below or type your own.</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Quick questions ─────────────────────────────────────────────────────
    qs = QUICK_QUESTIONS.get(role,[])
    if qs:
        with st.expander("💡 Quick Questions — click any to ask", expanded=is_fresh):
            c1,c2,c3 = st.columns(3)
            cols_cycle = [c1,c2,c3]
            for i,q in enumerate(qs):
                with cols_cycle[i%3]:
                    if st.button(q, key=f"qq_{i}", use_container_width=True):
                        st.session_state.run_question = q
                        st.rerun()
        st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)

    # ── Input bar (placed above history since newest messages render on top) ──
    with st.form("chat_form", clear_on_submit=True):
        fi, fb = st.columns([7,1])
        with fi:
            user_input = st.text_input(
                "msg", label_visibility="collapsed",
                placeholder=f"Ask MediBot anything from: {', '.join(colls)}…",
            )
        with fb:
            sent = st.form_submit_button("Send ➤", use_container_width=True, type="primary")

    if sent and user_input.strip():
        st.session_state.run_question = user_input.strip()
        st.rerun()

    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)

    # ── Message history (newest first, pairs kept together) ──────────────────
    # Messages are stored chronologically as they happen: user, then
    # assistant/blocked. Group into pairs first, then reverse pair order so
    # the latest question+answer appears at the top, while within a pair the
    # question still appears above its answer.
    msgs = st.session_state.messages
    pairs = []
    i = 0
    while i < len(msgs):
        if msgs[i]["role"] == "user":
            pair = [msgs[i]]
            if i + 1 < len(msgs) and msgs[i+1]["role"] in ("assistant", "blocked"):
                pair.append(msgs[i+1])
                i += 2
            else:
                i += 1
            pairs.append(pair)
        else:
            pairs.append([msgs[i]])
            i += 1

    for pair in reversed(pairs):
        for msg in pair:
            if msg["role"]=="user": render_user_msg(msg["content"])
            elif msg["role"]=="assistant": render_bot_msg(msg["data"])
            elif msg["role"]=="blocked": render_blocked_msg(msg["content"])

# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════
def main():
    if not st.session_state.logged_in:
        render_login()
    else:
        render_sidebar()
        render_chat()

if __name__ == "__main__":
    main()
