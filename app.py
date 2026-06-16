"""
MediBot — Streamlit App · MediAssist Health Network
Fixes: single shared password, persistent Groq key, working quick questions & answers
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
#MainMenu,footer,header,.stDeployButton{visibility:hidden;display:none;}
.stApp{
  background:
    radial-gradient(ellipse at 15% 15%,rgba(56,189,248,.07) 0%,transparent 55%),
    radial-gradient(ellipse at 85% 10%,rgba(139,92,246,.06) 0%,transparent 45%),
    linear-gradient(160deg,#080e1a 0%,#0b1220 40%,#080e1a 100%);
  min-height:100vh; color:#e2e8f0;
}
section[data-testid="stSidebar"]{
  background:linear-gradient(175deg,#040912 0%,#060d1a 40%,#050b18 100%) !important;
  border-right:1px solid rgba(56,189,248,.10) !important;
  box-shadow:4px 0 32px rgba(0,0,0,.6) !important;
}
section[data-testid="stSidebar"]>div{padding-top:0 !important;}
section[data-testid="stSidebar"] *{color:#94a3b8 !important;}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] strong,
section[data-testid="stSidebar"] b{color:#f1f5f9 !important;}
section[data-testid="stSidebar"] hr{border-color:rgba(56,189,248,.08) !important;}

/* Sidebar logo */
.sb-logo{background:linear-gradient(135deg,rgba(14,165,233,.08),rgba(99,102,241,.04));
  border-bottom:1px solid rgba(56,189,248,.10);padding:20px 16px 16px;text-align:center;}
.sb-icon{width:48px;height:48px;background:linear-gradient(135deg,#0ea5e9,#6366f1);
  border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:22px;
  margin:0 auto 8px;animation:pulse 2.5s infinite;}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(14,165,233,.4);}60%{box-shadow:0 0 0 10px rgba(14,165,233,0);}100%{box-shadow:0 0 0 0 rgba(14,165,233,0);}}
.sb-title{font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:700;color:#f1f5f9 !important;}
.sb-sub{font-size:9px;color:#1e3a5f !important;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px;}

/* Sidebar user card */
.sb-user-card{margin:12px 12px 0;background:rgba(255,255,255,.03);
  border:1px solid rgba(56,189,248,.10);border-radius:14px;padding:12px;}
.sb-av{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;
  justify-content:center;font-size:13px;font-weight:700;color:white;flex-shrink:0;
  box-shadow:0 3px 10px rgba(0,0,0,.4);}
.sb-uname{font-size:12px;font-weight:600;color:#e2e8f0 !important;}
.sb-udept{font-size:10px;color:#334155 !important;margin-top:1px;}
.online-dot{width:6px;height:6px;border-radius:50%;background:#22c55e;
  box-shadow:0 0 0 2px rgba(34,197,94,.2);display:inline-block;animation:blink 2s infinite;}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.3;}}

/* Role badges */
.role-badge{display:inline-flex;align-items:center;gap:5px;padding:3px 10px;
  border-radius:20px;font-size:10px;font-weight:600;letter-spacing:.4px;
  text-transform:uppercase;margin-top:5px;}
.badge-doctor{background:#052e16;color:#4ade80 !important;border:1px solid #16a34a;}
.badge-nurse{background:#0c1a3a;color:#60a5fa !important;border:1px solid #2563eb;}
.badge-billing_executive{background:#2d1a00;color:#fbbf24 !important;border:1px solid #d97706;}
.badge-technician{background:#1a0a3d;color:#a78bfa !important;border:1px solid #7c3aed;}
.badge-admin{background:#2d0a0a;color:#f87171 !important;border:1px solid #ef4444;}

/* Collection chips */
.coll-chip{display:flex;align-items:center;gap:7px;padding:5px 11px;border-radius:9px;
  font-size:11px;font-weight:500;margin:3px 0;border:1px solid;}
.coll-general{background:rgba(100,116,139,.08);border-color:rgba(100,116,139,.18);color:#94a3b8 !important;}
.coll-clinical{background:rgba(22,163,74,.08);border-color:rgba(22,163,74,.18);color:#4ade80 !important;}
.coll-nursing{background:rgba(37,99,235,.08);border-color:rgba(37,99,235,.18);color:#60a5fa !important;}
.coll-billing{background:rgba(217,119,6,.08);border-color:rgba(217,119,6,.18);color:#fbbf24 !important;}
.coll-equipment{background:rgba(124,58,237,.08);border-color:rgba(124,58,237,.18);color:#a78bfa !important;}
.coll-locked{background:rgba(0,0,0,.15);border-color:rgba(255,255,255,.04);color:#1e293b !important;opacity:.5;}

/* Stats */
.stat-pill{display:flex;align-items:center;gap:6px;padding:4px 0;font-size:11px;color:#334155 !important;}
.stat-pill span{color:#38bdf8 !important;font-weight:600;}

/* Login */
.login-hero{text-align:center;padding:36px 20px 24px;}
.login-icon-ring{width:72px;height:72px;background:linear-gradient(135deg,#0ea5e9,#6366f1);
  border-radius:22px;display:flex;align-items:center;justify-content:center;font-size:34px;
  margin:0 auto 16px;box-shadow:0 8px 28px rgba(14,165,233,.35),0 0 0 10px rgba(14,165,233,.07);
  animation:float 3s ease-in-out infinite;}
@keyframes float{0%,100%{transform:translateY(0);}50%{transform:translateY(-7px);}}
.login-title{font-family:'Space Grotesk',sans-serif;font-size:32px;font-weight:800;
  background:linear-gradient(135deg,#38bdf8,#818cf8,#34d399);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:-1px;}
.login-sub{font-size:13px;color:#475569;margin-top:7px;line-height:1.5;}
.login-features{display:flex;justify-content:center;gap:9px;flex-wrap:wrap;margin-top:12px;}
.login-feat-chip{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);
  border-radius:20px;padding:4px 12px;font-size:11px;font-weight:500;color:#475569;}
.key-panel{background:rgba(217,119,6,.07);border:1px solid rgba(217,119,6,.22);
  border-radius:12px;padding:12px 16px;margin-bottom:14px;}
.key-panel-title{font-size:12px;font-weight:600;color:#fbbf24;}
.key-panel-sub{font-size:11px;color:#78350f;margin-top:3px;}
.key-panel-sub a{color:#f59e0b;}
.pwd-banner{background:rgba(34,197,94,.06);border:1px solid rgba(34,197,94,.18);
  border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:12px;color:#4ade80;
  display:flex;align-items:center;gap:8px;}
.user-card{background:rgba(255,255,255,.03);border:1.5px solid rgba(255,255,255,.07);
  border-radius:14px;padding:15px;margin:6px 0;position:relative;overflow:hidden;}
.user-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.uc-doctor::before{background:linear-gradient(90deg,#22c55e,#16a34a);}
.uc-nurse::before{background:linear-gradient(90deg,#3b82f6,#2563eb);}
.uc-billing::before{background:linear-gradient(90deg,#f59e0b,#d97706);}
.uc-technician::before{background:linear-gradient(90deg,#8b5cf6,#7c3aed);}
.uc-admin::before{background:linear-gradient(90deg,#ef4444,#dc2626);}
.uc-icon{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;
  justify-content:center;font-size:20px;margin-bottom:7px;}
.uc-doctor-bg{background:rgba(22,163,74,.14);}.uc-nurse-bg{background:rgba(37,99,235,.14);}
.uc-billing-bg{background:rgba(217,119,6,.14);}.uc-technician-bg{background:rgba(124,58,237,.14);}
.uc-admin-bg{background:rgba(220,38,38,.14);}
.uc-name{font-size:13px;font-weight:700;color:#e2e8f0;}
.uc-dept{font-size:10px;color:#475569;margin-top:1px;}
.uc-creds{font-size:10.5px;font-family:'Courier New',monospace;color:#334155;margin-top:7px;
  padding:4px 8px;background:rgba(255,255,255,.03);border-radius:6px;
  border:1px solid rgba(255,255,255,.05);}
.uc-access{font-size:10px;color:#1e3a5f;margin-top:3px;}

/* Messages */
.msg-row-user{display:flex;justify-content:flex-end;margin:14px 0;animation:slideR .3s ease;}
.msg-row-bot{display:flex;justify-content:flex-start;align-items:flex-start;gap:9px;margin:14px 0;animation:slideL .3s ease;}
.msg-row-blocked{display:flex;justify-content:flex-start;align-items:flex-start;gap:9px;margin:14px 0;}
@keyframes slideR{from{opacity:0;transform:translateX(18px);}to{opacity:1;transform:translateX(0);}}
@keyframes slideL{from{opacity:0;transform:translateX(-18px);}to{opacity:1;transform:translateX(0);}}
.bubble-user{background:linear-gradient(135deg,#2563eb,#1d4ed8);color:white;
  padding:11px 16px;border-radius:18px 18px 4px 18px;max-width:70%;font-size:13.5px;
  line-height:1.65;box-shadow:0 4px 18px rgba(37,99,235,.4);word-wrap:break-word;}
.bot-avatar{width:34px;height:34px;background:linear-gradient(135deg,#0c4a6e,#0ea5e9);
  border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:17px;
  flex-shrink:0;margin-top:2px;box-shadow:0 2px 10px rgba(14,165,233,.25);}
.bubble-bot{background:rgba(255,255,255,.04);color:#cbd5e1;padding:14px 18px;
  border-radius:4px 18px 18px 18px;max-width:80%;font-size:13.5px;line-height:1.78;
  border:1px solid rgba(56,189,248,.10);word-wrap:break-word;backdrop-filter:blur(6px);}
.bubble-bot strong{color:#38bdf8;}
.blocked-avatar{width:34px;height:34px;background:linear-gradient(135deg,#450a0a,#7f1d1d);
  border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;
  flex-shrink:0;margin-top:2px;box-shadow:0 2px 10px rgba(239,68,68,.25);}
.bubble-blocked{background:rgba(239,68,68,.06);color:#fca5a5;padding:12px 16px;
  border-radius:4px 18px 18px 18px;max-width:80%;font-size:13.5px;line-height:1.68;
  border:1px solid rgba(239,68,68,.18);}
.bubble-blocked strong{color:#f87171;}
.sources-row{margin-top:11px;padding-top:9px;border-top:1px solid rgba(56,189,248,.08);}
.src-chip{display:inline-flex;align-items:center;gap:4px;background:rgba(14,165,233,.07);
  color:#38bdf8;border:1px solid rgba(14,165,233,.15);border-radius:7px;
  padding:3px 9px;font-size:10.5px;font-weight:500;margin:2px 3px;}
.ret-badge{display:inline-flex;align-items:center;gap:4px;padding:2px 9px;border-radius:20px;
  font-size:10.5px;font-weight:600;margin-top:7px;}
.ret-hybrid{background:rgba(37,99,235,.10);color:#60a5fa;border:1px solid rgba(37,99,235,.2);}
.ret-sql{background:rgba(124,58,237,.10);color:#a78bfa;border:1px solid rgba(124,58,237,.2);}
.sql-box{margin-top:9px;background:#020817;border-radius:9px;padding:10px 13px;
  font-size:11.5px;font-family:'Courier New',monospace;color:#38bdf8;
  border:1px solid rgba(14,165,233,.12);overflow-x:auto;line-height:1.6;}
.welcome-banner{background:rgba(14,165,233,.05);border:1px solid rgba(14,165,233,.13);
  border-radius:14px;padding:14px 18px;display:flex;align-items:center;gap:13px;margin-bottom:8px;}
.welcome-icon{font-size:28px;flex-shrink:0;}
.welcome-text{font-size:13px;color:#7dd3fc;line-height:1.58;}
.welcome-text strong{color:#38bdf8;}

/* Input */
.stTextInput>div>div>input{
  border-radius:13px !important;border:1.5px solid rgba(255,255,255,.08) !important;
  padding:11px 15px !important;font-size:13.5px !important;font-family:'Inter',sans-serif !important;
  background:rgba(255,255,255,.04) !important;color:#e2e8f0 !important;transition:all .2s !important;}
.stTextInput>div>div>input::placeholder{color:#334155 !important;}
.stTextInput>div>div>input:focus{border-color:rgba(14,165,233,.45) !important;
  box-shadow:0 0 0 4px rgba(14,165,233,.08) !important;background:rgba(255,255,255,.06) !important;}
.stButton>button{border-radius:11px !important;font-family:'Inter',sans-serif !important;font-weight:600 !important;transition:all .2s !important;}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#0ea5e9,#2563eb) !important;
  color:white !important;border:none !important;box-shadow:0 4px 14px rgba(14,165,233,.35) !important;}
.stButton>button[kind="primary"]:hover{background:linear-gradient(135deg,#0284c7,#1d4ed8) !important;
  transform:translateY(-1px) !important;box-shadow:0 6px 18px rgba(14,165,233,.45) !important;}
.stButton>button[kind="secondary"]{background:rgba(255,255,255,.04) !important;
  border:1px solid rgba(255,255,255,.08) !important;color:#94a3b8 !important;}
.stButton>button[kind="secondary"]:hover{background:rgba(14,165,233,.08) !important;
  border-color:rgba(14,165,233,.25) !important;color:#38bdf8 !important;}
.stSelectbox>div>div{border-radius:9px !important;border:1px solid rgba(56,189,248,.15) !important;
  background:rgba(255,255,255,.04) !important;}
.stAlert{border-radius:11px !important;}
div[data-testid="stInfo"]{background:rgba(14,165,233,.08) !important;border-color:rgba(14,165,233,.2) !important;color:#7dd3fc !important;}
div[data-testid="stSuccess"]{background:rgba(22,163,74,.08) !important;border-color:rgba(22,163,74,.2) !important;color:#86efac !important;}
div[data-testid="stWarning"]{background:rgba(234,179,8,.08) !important;border-color:rgba(234,179,8,.2) !important;color:#fde047 !important;}
div[data-testid="stError"]{background:rgba(239,68,68,.08) !important;border-color:rgba(239,68,68,.2) !important;color:#fca5a5 !important;}
.streamlit-expanderHeader{background:rgba(255,255,255,.03) !important;border-radius:9px !important;
  border:1px solid rgba(255,255,255,.07) !important;color:#64748b !important;}
.stToggle>label{font-size:12px !important;color:#64748b !important;}
.sb-signout button{background:rgba(239,68,68,.06) !important;
  border:1px solid rgba(239,68,68,.18) !important;color:#f87171 !important;border-radius:9px !important;}
.sb-signout button:hover{background:rgba(239,68,68,.14) !important;border-color:rgba(239,68,68,.4) !important;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:#1e293b;border-radius:4px;}
::-webkit-scrollbar-thumb:hover{background:#334155;}
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ─────────────────────────────────────────────────────────────────
GROQ_API_URL   = "https://api.groq.com/openai/v1/chat/completions"
MODEL          = "llama-3.3-70b-versatile"
SHARED_PASSWORD = "medibot123"   # ← single password for all accounts

USERS = {
    "dr.mehta":     {"role":"doctor",            "display":"Dr. Arjun Mehta",   "dept":"Clinical Department",      "initials":"AM","color":"#059669"},
    "nurse.priya":  {"role":"nurse",             "display":"Nurse Priya Singh", "dept":"Critical Care Unit",       "initials":"PS","color":"#2563eb"},
    "billing.ravi": {"role":"billing_executive", "display":"Ravi Kumar",        "dept":"Billing & Insurance",      "initials":"RK","color":"#d97706"},
    "tech.anand":   {"role":"technician",        "display":"Anand Pillai",      "dept":"Biomedical Engineering",   "initials":"AP","color":"#7c3aed"},
    "admin.sys":    {"role":"admin",             "display":"Admin System",       "dept":"Executive / IT",           "initials":"AS","color":"#dc2626"},
}

ROLE_META = {
    "doctor":            {"icon":"👨‍⚕️","label":"Doctor",        "color":"#059669","bg_class":"uc-doctor-bg",    "card_class":"uc-doctor",    "badge":"badge-doctor"},
    "nurse":             {"icon":"👩‍⚕️","label":"Nurse",         "color":"#2563eb","bg_class":"uc-nurse-bg",     "card_class":"uc-nurse",     "badge":"badge-nurse"},
    "billing_executive": {"icon":"📋",  "label":"Billing Exec", "color":"#d97706","bg_class":"uc-billing-bg",   "card_class":"uc-billing",   "badge":"badge-billing_executive"},
    "technician":        {"icon":"🔧",  "label":"Technician",   "color":"#7c3aed","bg_class":"uc-technician-bg","card_class":"uc-technician","badge":"badge-technician"},
    "admin":             {"icon":"🛡️", "label":"Admin",         "color":"#dc2626","bg_class":"uc-admin-bg",     "card_class":"uc-admin",     "badge":"badge-admin"},
}

COLLECTION_META = {
    "general":  {"icon":"📚","label":"General",  "chip":"coll-general"},
    "clinical": {"icon":"🩺","label":"Clinical", "chip":"coll-clinical"},
    "nursing":  {"icon":"💉","label":"Nursing",  "chip":"coll-nursing"},
    "billing":  {"icon":"📊","label":"Billing",  "chip":"coll-billing"},
    "equipment":{"icon":"⚙️","label":"Equipment","chip":"coll-equipment"},
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
        "user_color":"#2563eb", "messages":[], "show_debug":False,
        "api_key":"", "selected_model":MODEL,
        "run_question":"",   # question to process this frame
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
        cur  = conn.cursor()
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
          <div class="login-sub" style="color:#475569;">
            MediAssist Health Network · Internal AI Assistant<br>
            <span style="font-size:11px;color:#334155;">Powered by Groq ⚡ LLaMA-3.3-70B</span>
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
                Free at <a href="https://console.groq.com/keys" target="_blank"
                style="color:#f59e0b;font-weight:600;">console.groq.com/keys</a>
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
                st.rerun()          # re-render immediately so key panel collapses
        else:
            st.success(f"⚡ Groq key ready  ·  Model: {MODEL}", icon="✅")

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # ── Shared password banner ──
        st.markdown(f"""
        <div class="pwd-banner">
          🔐 &nbsp;Password for <strong>all accounts</strong>: &nbsp;
          <code style="background:#0f172a;color:#38bdf8;padding:2px 9px;
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
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px;font-weight:600;color:#334155;letter-spacing:.8px;text-transform:uppercase;margin-bottom:8px;">👤 Demo Accounts</div>', unsafe_allow_html=True)
        users_list = list(USERS.items())
        col_a, col_b = st.columns(2)
        for i,(uname,info) in enumerate(users_list):
            role  = info["role"]
            meta  = ROLE_META[role]
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
        <div style="text-align:center;margin-top:16px;font-size:10.5px;color:#1e293b;">
          🔒 RBAC enforced at retrieval layer · 54 chunks · 30 claims · 21 tickets in DB
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════
def render_sidebar():
    role   = st.session_state.role
    meta   = ROLE_META[role]
    colls  = ROLE_COLLECTIONS.get(role,[])
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
            <div class="sb-av" style="background:linear-gradient(135deg,{st.session_state.user_color},{st.session_state.user_color}99);">
              {st.session_state.initials}
            </div>
            <div>
              <div class="sb-uname">{st.session_state.display_name}</div>
              <div class="sb-udept">{st.session_state.dept}</div>
            </div>
          </div>
          <span class="role-badge {meta['badge']}">{meta['icon']} {meta['label']}</span>
          <div style="display:flex;align-items:center;gap:5px;margin-top:7px;font-size:10px;color:#1e3a5f !important;">
            <span class="online-dot"></span> Online
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:9.5px;font-weight:600;color:#1e3a5f !important;letter-spacing:1.1px;text-transform:uppercase;padding:3px 2px;">📂 Your Collections</div>', unsafe_allow_html=True)
        for c in colls:
            cm = COLLECTION_META[c]
            st.markdown(f'<div class="coll-chip {cm["chip"]}">{cm["icon"]} {cm["label"]}</div>', unsafe_allow_html=True)

        if locked:
            st.markdown('<div style="font-size:9.5px;font-weight:600;color:#1e293b !important;letter-spacing:1.1px;text-transform:uppercase;padding:7px 2px 3px;">🔒 Restricted</div>', unsafe_allow_html=True)
            for c in locked:
                cm = COLLECTION_META[c]
                st.markdown(f'<div class="coll-chip coll-locked">🚫 {cm["label"]}</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:rgba(255,255,255,.02);border:1px solid rgba(56,189,248,.07);border-radius:10px;padding:10px 12px;">
          <div class="stat-pill">📄 <span>{n_chunks}</span> chunks accessible</div>
          <div class="stat-pill">🔍 BM25 + TF-IDF + RRF + Rerank</div>
          <div class="stat-pill">⚡ Groq · <span>LLaMA-3.3-70B</span></div>
          {"<div class='stat-pill'>🗄️ <span>SQL RAG enabled</span></div>" if role in ("billing_executive","admin") else ""}
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        model_map = {
            "llama-3.3-70b-versatile": "⚡ LLaMA 3.3 70B (Best)",
            "llama-3.1-8b-instant":    "🚀 LLaMA 3.1 8B (Fastest)",
            "mixtral-8x7b-32768":      "🌀 Mixtral 8x7B (32k ctx)",
            "gemma2-9b-it":            "💎 Gemma2 9B (Light)",
        }
        chosen = st.selectbox("🤖 Model", list(model_map.values()), index=0)
        st.session_state.selected_model = [k for k,v in model_map.items() if v==chosen][0]

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        st.session_state.show_debug = st.toggle("🔬 Debug mode", value=st.session_state.show_debug)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

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
    rtype  = data.get("retrieval_type","hybrid_rag")
    blabel = "🔍 Hybrid RAG" if rtype=="hybrid_rag" else "🗄️ SQL RAG"
    bclass = "ret-hybrid"    if rtype=="hybrid_rag" else "ret-sql"

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
                    f'color:#64748b;cursor:pointer;font-weight:500;">🗄️ View SQL query</summary>'
                    f'<div class="sql-box">{q}</div></details>')

    st.markdown(f"""
    <div class="msg-row-bot">
      <div class="bot-avatar">🏥</div>
      <div class="bubble-bot">
        {answer_html}
        {src_html}
        <div style="margin-top:8px;"><span class="ret-badge {bclass}">{blabel}</span></div>
        {sql_html}
      </div>
    </div>""", unsafe_allow_html=True)

    if st.session_state.show_debug and data.get("debug"):
        with st.expander("🔬 Retrieval debug"):
            st.json(data["debug"])

def render_blocked_msg(content:str):
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content.replace("\n","<br>"))
    st.markdown(f"""
    <div class="msg-row-blocked">
      <div class="blocked-avatar">🔒</div>
      <div class="bubble-blocked">{html}</div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# CHAT
# ═══════════════════════════════════════════════════════════════════════
def render_chat():
    role  = st.session_state.role
    meta  = ROLE_META[role]
    colls = ROLE_COLLECTIONS.get(role,[])

    # ── IMPORTANT: process run_question FIRST, before any rendering ──────────
    # This is the fix for blank answers — we process and THEN render everything.
    if st.session_state.get("run_question","").strip():
        q = st.session_state.run_question.strip()
        st.session_state.run_question = ""
        with st.spinner("⚡ Searching your authorised collections…"):
            _process(q, role)
        # Fall through — render normally with the new message now in state

    is_fresh = not st.session_state.messages

    # ── Header ──────────────────────────────────────────────────────────────
    COLL_BG = {"general":"#1e293b","clinical":"#052e16","nursing":"#0c1a3a","billing":"#2d1a00","equipment":"#1a0a3d"}
    COLL_FG = {"general":"#94a3b8","clinical":"#4ade80","nursing":"#60a5fa","billing":"#fbbf24","equipment":"#a78bfa"}
    h1, h2 = st.columns([5,1])
    with h1:
        tags = " ".join(
            f'<span style="font-size:11px;background:{COLL_BG[c]};color:{COLL_FG[c]};'
            f'padding:2px 8px;border-radius:7px;margin-right:3px;">{COLLECTION_META[c]["icon"]} {c.title()}</span>'
            for c in colls
        )
        st.markdown(f"""
        <div style="padding:10px 0 14px;border-bottom:1px solid rgba(56,189,248,.08);margin-bottom:14px;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:34px;height:34px;background:linear-gradient(135deg,#0f3460,#1d4ed8);
              border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:17px;
              box-shadow:0 2px 8px rgba(29,78,216,.3);">🏥</div>
            <div>
              <div style="font-family:'Space Grotesk',sans-serif;font-size:16px;font-weight:700;color:#f1f5f9;line-height:1.2;">
                MediBot <span class="online-dot" style="margin-left:3px;"></span>
                <span style="font-size:10.5px;font-weight:400;color:#22c55e;vertical-align:middle;">Online</span>
              </div>
              <div style="font-size:11px;color:#475569;margin-top:2px;">
                {meta['icon']} {st.session_state.display_name} &nbsp;·&nbsp; {tags}
              </div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
    with h2:
        if st.button("🗑️ Clear", help="Clear chat"):
            st.session_state.messages = []
            st.rerun()

    # ── Welcome banner ───────────────────────────────────────────────────────
    if is_fresh:
        coll_str = "  ".join(f"{COLLECTION_META[c]['icon']} **{c.title()}**" for c in colls)
        sql_note = (" You also have **SQL RAG** — ask analytical questions about claims & equipment data."
                    if role in ("billing_executive","admin") else "")
        st.markdown(f"""
        <div class="welcome-banner">
          <div class="welcome-icon">{meta['icon']}</div>
          <div class="welcome-text">
            Welcome, <strong>{st.session_state.display_name}</strong>!
            Your authorised collections: {coll_str}.{sql_note}<br>
            <span style="font-size:11.5px;color:#2563eb;">Click a quick question below or type your own.</span>
          </div>
        </div>""", unsafe_allow_html=True)

    # ── Quick questions (always show, not just on fresh) ─────────────────────
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

    # ── Message history ───────────────────────────────────────────────────────
    for msg in st.session_state.messages:
        if   msg["role"]=="user":      render_user_msg(msg["content"])
        elif msg["role"]=="assistant": render_bot_msg(msg["data"])
        elif msg["role"]=="blocked":   render_blocked_msg(msg["content"])

    # ── Input bar ─────────────────────────────────────────────────────────────
    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
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
