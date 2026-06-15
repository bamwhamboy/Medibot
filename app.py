"""
MediBot — Streamlit Application  ·  MediAssist Health Network
Hybrid RAG + RBAC + SQL RAG  ·  Groq LLaMA-3.3-70B
Eye-catching UI with glassmorphism, animations & medical branding
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

# ─── FULL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }

/* ── App background — deep dark mesh ── */
.stApp {
    background:
        radial-gradient(ellipse at 15% 15%, rgba(56,189,248,0.07) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 10%, rgba(139,92,246,0.06) 0%, transparent 45%),
        radial-gradient(ellipse at 50% 95%, rgba(16,185,129,0.05) 0%, transparent 50%),
        linear-gradient(160deg, #080e1a 0%, #0b1220 40%, #080e1a 100%);
    min-height: 100vh;
    color: #e2e8f0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #040912 0%, #060d1a 40%, #050b18 100%) !important;
    border-right: 1px solid rgba(56,189,248,0.10) !important;
    box-shadow: 4px 0 32px rgba(0,0,0,0.6) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
section[data-testid="stSidebar"] * { color: #94a3b8 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] strong,
section[data-testid="stSidebar"] b { color: #f1f5f9 !important; }
section[data-testid="stSidebar"] hr { border-color: rgba(56,189,248,0.08) !important; }

/* ── Sidebar logo ── */
.sb-logo {
    background: linear-gradient(135deg, rgba(56,189,248,0.08), rgba(139,92,246,0.06));
    border-bottom: 1px solid rgba(56,189,248,0.10);
    padding: 20px 16px 16px;
    text-align: center;
}
.sb-logo-pulse {
    width: 54px; height: 54px;
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
    margin: 0 auto 10px;
    animation: pulse-ring 2.5s infinite;
}
@keyframes pulse-ring {
    0%   { box-shadow: 0 0 0 0 rgba(14,165,233,0.45); }
    60%  { box-shadow: 0 0 0 12px rgba(14,165,233,0); }
    100% { box-shadow: 0 0 0 0 rgba(14,165,233,0); }
}
.sb-logo-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px; font-weight: 700;
    color: #f1f5f9 !important; letter-spacing: -0.3px;
}
.sb-logo-sub { font-size: 9.5px; color: #334e68 !important; letter-spacing: 2px; text-transform: uppercase; margin-top: 3px; }

/* ── Sidebar user card ── */
.sb-user-card {
    margin: 12px 12px 0;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(56,189,248,0.10);
    border-radius: 14px; padding: 14px;
}
.sb-avatar {
    width: 42px; height: 42px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; font-weight: 800; color: white; flex-shrink: 0;
    box-shadow: 0 4px 14px rgba(0,0,0,0.4);
}
.sb-uname { font-size: 13px; font-weight: 600; color: #f1f5f9 !important; }
.sb-udept { font-size: 11px; color: #475569 !important; margin-top: 1px; }

/* ── Role badges ── */
.role-badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 4px 11px; border-radius: 20px;
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.4px; text-transform: uppercase; margin-top: 6px;
}
.badge-doctor           { background:#052e16; color:#4ade80!important; border:1px solid #16a34a; }
.badge-nurse            { background:#0c1a3a; color:#60a5fa!important; border:1px solid #2563eb; }
.badge-billing_executive{ background:#2d1a00; color:#fbbf24!important; border:1px solid #d97706; }
.badge-technician       { background:#1a0a3d; color:#a78bfa!important; border:1px solid #7c3aed; }
.badge-admin            { background:#2d0a0a; color:#f87171!important; border:1px solid #ef4444; }

/* ── Collection chips ── */
.coll-chip {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 12px; border-radius: 10px;
    font-size: 12px; font-weight: 500;
    margin: 4px 0; border: 1px solid; transition: all 0.2s;
}
.coll-general  { background:rgba(100,116,139,.10); border-color:rgba(100,116,139,.20); color:#94a3b8!important; }
.coll-clinical { background:rgba(22,163,74,.08);   border-color:rgba(22,163,74,.18);   color:#4ade80!important; }
.coll-nursing  { background:rgba(37,99,235,.08);   border-color:rgba(37,99,235,.18);   color:#60a5fa!important; }
.coll-billing  { background:rgba(217,119,6,.08);   border-color:rgba(217,119,6,.18);   color:#fbbf24!important; }
.coll-equipment{ background:rgba(124,58,237,.08);  border-color:rgba(124,58,237,.18);  color:#a78bfa!important; }
.coll-locked   { background:rgba(0,0,0,.20); border-color:rgba(255,255,255,.04); color:#1e293b!important; opacity:0.55; }

/* ── Stat pills ── */
.stat-pill { display:flex; align-items:center; gap:7px; padding:5px 0; font-size:11.5px; color:#475569!important; }
.stat-pill-val { color:#38bdf8!important; font-weight:600; }

/* ── Login page ── */
.login-hero { text-align:center; padding:44px 24px 28px; }
.login-icon-ring {
    width: 80px; height: 80px;
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    border-radius: 24px;
    display: flex; align-items: center; justify-content: center;
    font-size: 38px; margin: 0 auto 20px;
    box-shadow: 0 8px 32px rgba(14,165,233,0.35), 0 0 0 10px rgba(14,165,233,0.07);
    animation: float 3s ease-in-out infinite;
}
@keyframes float { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-7px);} }

.login-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 36px; font-weight: 800;
    background: linear-gradient(135deg, #38bdf8, #818cf8, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: -1px; line-height: 1.1;
}
.login-sub { font-size: 14px; color: #475569; margin-top: 8px; line-height: 1.5; }
.login-features { display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-top:14px; }
.login-feat-chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px; padding: 5px 13px;
    font-size: 11px; font-weight: 500; color: #64748b;
}

/* ── API key panel ── */
.key-panel {
    background: rgba(217,119,6,0.07);
    border: 1px solid rgba(217,119,6,0.25);
    border-radius: 14px; padding: 14px 18px; margin-bottom: 20px;
}
.key-panel-title { font-size: 13px; font-weight: 600; color: #fbbf24; margin-bottom: 5px; }
.key-panel-sub   { font-size: 11.5px; color: #92400e; }
.key-panel-sub a { color: #f59e0b; }

/* ── User login cards ── */
.user-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 18px; margin: 8px 0;
    cursor: pointer; position: relative; overflow: hidden;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
}
.user-card:hover { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.13); transform: translateY(-2px); }
.user-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; }
.uc-doctor::before     { background:linear-gradient(90deg,#22c55e,#16a34a); }
.uc-nurse::before      { background:linear-gradient(90deg,#3b82f6,#2563eb); }
.uc-billing::before    { background:linear-gradient(90deg,#f59e0b,#d97706); }
.uc-technician::before { background:linear-gradient(90deg,#8b5cf6,#7c3aed); }
.uc-admin::before      { background:linear-gradient(90deg,#ef4444,#dc2626); }
.uc-icon { width:44px; height:44px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; margin-bottom:10px; }
.uc-doctor-bg     { background:rgba(22,163,74,0.15); }
.uc-nurse-bg      { background:rgba(37,99,235,0.15); }
.uc-billing-bg    { background:rgba(217,119,6,0.15); }
.uc-technician-bg { background:rgba(124,58,237,0.15); }
.uc-admin-bg      { background:rgba(220,38,38,0.15); }
.uc-name  { font-size:14px; font-weight:700; color:#e2e8f0; }
.uc-dept  { font-size:11px; color:#475569; margin-top:2px; }
.uc-creds { font-size:11px; font-family:'Courier New',monospace; color:#334155; margin-top:8px; padding:5px 8px; background:rgba(255,255,255,0.03); border-radius:6px; border:1px solid rgba(255,255,255,0.06); }
.uc-access{ font-size:10px; color:#334155; margin-top:4px; }

/* ── Chat header ── */
.online-dot {
    width:8px; height:8px; border-radius:50%;
    background:#22c55e; box-shadow:0 0 0 3px rgba(34,197,94,0.2);
    display:inline-block; margin-right:4px;
    animation: blink-dot 2s infinite;
}
@keyframes blink-dot { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

/* ── Messages ── */
.msg-row-user    { display:flex; justify-content:flex-end; margin:16px 0; animation:slideInRight .3s ease; }
.msg-row-bot     { display:flex; justify-content:flex-start; align-items:flex-start; gap:10px; margin:16px 0; animation:slideInLeft .3s ease; }
.msg-row-blocked { display:flex; justify-content:flex-start; align-items:flex-start; gap:10px; margin:16px 0; }
@keyframes slideInRight { from{opacity:0;transform:translateX(20px);}  to{opacity:1;transform:translateX(0);} }
@keyframes slideInLeft  { from{opacity:0;transform:translateX(-20px);} to{opacity:1;transform:translateX(0);} }

/* User bubble — keep blue gradient, it's intentional sender colour */
.bubble-user {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    padding: 13px 18px;
    border-radius: 20px 20px 4px 20px;
    max-width: 70%; font-size: 14px; line-height: 1.65;
    box-shadow: 0 4px 20px rgba(37,99,235,0.4);
    word-wrap: break-word;
}

/* Bot avatar */
.bot-avatar {
    width: 38px; height: 38px; border-radius: 12px;
    background: linear-gradient(135deg, #0c4a6e, #0ea5e9);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0; margin-top: 2px;
    box-shadow: 0 3px 12px rgba(14,165,233,0.3);
}

/* Bot bubble */
.bubble-bot {
    background: rgba(255,255,255,0.04);
    color: #cbd5e1;
    padding: 16px 20px;
    border-radius: 4px 20px 20px 20px;
    max-width: 78%; font-size: 14px; line-height: 1.80;
    border: 1px solid rgba(56,189,248,0.10);
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    word-wrap: break-word;
    backdrop-filter: blur(8px);
}
.bubble-bot strong { color: #38bdf8; }

/* Blocked bubble */
.blocked-avatar {
    width: 38px; height: 38px; border-radius: 12px;
    background: linear-gradient(135deg, #450a0a, #7f1d1d);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0; margin-top: 2px;
    box-shadow: 0 3px 12px rgba(239,68,68,0.3);
}
.bubble-blocked {
    background: rgba(239,68,68,0.06);
    color: #fca5a5;
    padding: 14px 18px;
    border-radius: 4px 20px 20px 20px;
    max-width: 78%; font-size: 14px; line-height: 1.7;
    border: 1px solid rgba(239,68,68,0.20);
    box-shadow: 0 4px 20px rgba(239,68,68,0.08);
}

/* ── Source citations ── */
.sources-row { margin-top:12px; padding-top:10px; border-top:1px solid rgba(56,189,248,0.08); }
.src-chip {
    display:inline-flex; align-items:center; gap:5px;
    background:rgba(14,165,233,0.08);
    color:#38bdf8; border:1px solid rgba(14,165,233,0.18);
    border-radius:8px; padding:4px 10px;
    font-size:11px; font-weight:500; margin:2px 3px;
}

/* ── Retrieval badges ── */
.ret-badge { display:inline-flex; align-items:center; gap:5px; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; margin-top:8px; }
.ret-hybrid { background:rgba(37,99,235,0.12); color:#60a5fa; border:1px solid rgba(37,99,235,0.25); }
.ret-sql    { background:rgba(124,58,237,0.12); color:#a78bfa; border:1px solid rgba(124,58,237,0.25); }

/* ── SQL box ── */
.sql-box {
    margin-top:10px; background:#020817; border-radius:10px;
    padding:12px 14px; font-size:12px; font-family:'Courier New',monospace;
    color:#38bdf8; border:1px solid rgba(14,165,233,0.15);
    overflow-x:auto; line-height:1.6;
}

/* ── Quick questions ── */
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #94a3b8 !important;
    font-size: 12px !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(14,165,233,0.08) !important;
    border-color: rgba(14,165,233,0.25) !important;
    color: #38bdf8 !important;
}

/* ── Input bar ── */
.stTextInput > div > div > input {
    border-radius: 14px !important;
    border: 1.5px solid rgba(255,255,255,0.08) !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    background: rgba(255,255,255,0.04) !important;
    color: #e2e8f0 !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div > input::placeholder { color: #334155 !important; }
.stTextInput > div > div > input:focus {
    border-color: rgba(14,165,233,0.45) !important;
    box-shadow: 0 0 0 4px rgba(14,165,233,0.08) !important;
    background: rgba(255,255,255,0.06) !important;
}

/* ── Primary button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(14,165,233,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0284c7, #1d4ed8) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(14,165,233,0.45) !important;
}
.stButton > button { border-radius: 12px !important; font-family: 'Inter', sans-serif !important; font-weight: 500 !important; transition: all 0.2s !important; }

/* ── Sidebar sign-out ── */
.sb-signout button {
    background: rgba(239,68,68,0.06) !important;
    border: 1px solid rgba(239,68,68,0.18) !important;
    color: #f87171 !important;
    border-radius: 10px !important;
}
.sb-signout button:hover {
    background: rgba(239,68,68,0.14) !important;
    border-color: rgba(239,68,68,0.4) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1px solid rgba(56,189,248,0.15) !important;
    background: rgba(255,255,255,0.04) !important;
    color: #94a3b8 !important;
}

/* ── Alerts ── */
.stAlert { border-radius: 12px !important; }
div[data-testid="stInfo"]    { background: rgba(14,165,233,0.08) !important; border-color: rgba(14,165,233,0.2) !important; color: #7dd3fc !important; }
div[data-testid="stSuccess"] { background: rgba(22,163,74,0.08) !important; border-color: rgba(22,163,74,0.2) !important; color: #86efac !important; }
div[data-testid="stWarning"] { background: rgba(234,179,8,0.08) !important; border-color: rgba(234,179,8,0.2) !important; color: #fde047 !important; }
div[data-testid="stError"]   { background: rgba(239,68,68,0.08) !important; border-color: rgba(239,68,68,0.2) !important; color: #fca5a5 !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: #64748b !important;
}

/* ── Toggle ── */
.stToggle > label { font-size: 12px !important; color: #64748b !important; }

/* ── Welcome banner ── */
.welcome-banner {
    background: rgba(14,165,233,0.06);
    border: 1px solid rgba(14,165,233,0.15);
    border-radius: 16px; padding: 16px 20px;
    display: flex; align-items: center; gap: 14px; margin-bottom: 8px;
}
.welcome-icon { font-size: 32px; flex-shrink: 0; }
.welcome-text { font-size: 13.5px; color: #7dd3fc; line-height: 1.6; }
.welcome-text strong { color: #38bdf8; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #334155; }
</style>
""", unsafe_allow_html=True)

# ─── GROQ CONFIG ──────────────────────────────────────────────────────────────
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

# ─── APP DATA ─────────────────────────────────────────────────────────────────
USERS = {
    "dr.mehta":     {"password":"doctor123",  "role":"doctor",            "display":"Dr. Arjun Mehta",   "dept":"Clinical Department",      "initials":"AM", "color":"#059669"},
    "nurse.priya":  {"password":"nurse123",   "role":"nurse",             "display":"Nurse Priya Singh", "dept":"Critical Care Unit",        "initials":"PS", "color":"#2563eb"},
    "billing.ravi": {"password":"billing123", "role":"billing_executive", "display":"Ravi Kumar",        "dept":"Billing & Insurance",       "initials":"RK", "color":"#d97706"},
    "tech.anand":   {"password":"tech123",    "role":"technician",        "display":"Anand Pillai",      "dept":"Biomedical Engineering",    "initials":"AP", "color":"#7c3aed"},
    "admin.sys":    {"password":"admin123",   "role":"admin",             "display":"Admin System",      "dept":"Executive / IT Operations", "initials":"AS", "color":"#dc2626"},
}

ROLE_META = {
    "doctor":            {"icon":"👨‍⚕️", "label":"Doctor",           "color":"#059669", "bg_class":"uc-doctor-bg",     "card_class":"uc-doctor",     "badge":"badge-doctor"},
    "nurse":             {"icon":"👩‍⚕️", "label":"Nurse",            "color":"#2563eb", "bg_class":"uc-nurse-bg",      "card_class":"uc-nurse",      "badge":"badge-nurse"},
    "billing_executive": {"icon":"📋",   "label":"Billing Exec",     "color":"#d97706", "bg_class":"uc-billing-bg",    "card_class":"uc-billing",    "badge":"badge-billing_executive"},
    "technician":        {"icon":"🔧",   "label":"Technician",       "color":"#7c3aed", "bg_class":"uc-technician-bg", "card_class":"uc-technician", "badge":"badge-technician"},
    "admin":             {"icon":"🛡️",  "label":"Administrator",    "color":"#dc2626", "bg_class":"uc-admin-bg",      "card_class":"uc-admin",      "badge":"badge-admin"},
}

COLLECTION_META = {
    "general":  {"icon":"📚", "label":"General",   "chip":"coll-general"},
    "clinical": {"icon":"🩺", "label":"Clinical",  "chip":"coll-clinical"},
    "nursing":  {"icon":"💉", "label":"Nursing",   "chip":"coll-nursing"},
    "billing":  {"icon":"📊", "label":"Billing",   "chip":"coll-billing"},
    "equipment":{"icon":"⚙️", "label":"Equipment", "chip":"coll-equipment"},
}

QUICK_QUESTIONS = {
    "doctor": [
        "⚡ NSTEMI treatment protocol & Aspirin dose?",
        "🌡️ Paracetamol dose for 12 kg child?",
        "🫁 Manage COPD acute exacerbation?",
        "❤️ Normal troponin I range & significance?",
        "💊 Azithromycin drug interactions?",
    ],
    "nurse": [
        "🩺 CVC dressing change procedure?",
        "💉 IV cannula size for child under 5kg?",
        "🦠 PPE for aerosol-generating procedures?",
        "🍽️ Gastric residual volume >400 mL action?",
        "🛏️ Pressure injury prevention bundle?",
    ],
    "billing_executive": [
        "⏱️ Emergency cashless pre-auth deadline?",
        "🏷️ NSTEMI ICD-10 code & package rate?",
        "📋 Respond to EXCL-01 rejection?",
        "📊 How many claims are escalated?",
        "📈 Billing KPI targets?",
    ],
    "technician": [
        "🔴 DriveFlow IP-200 fault code F-12?",
        "🧫 Autoclave Bowie-Dick test procedure?",
        "📡 BM-500 calibration schedule?",
        "📋 Which categories have open tickets?",
        "☢️ RadiPro MX-150 radiation safety?",
    ],
    "admin": [
        "📊 How many claims are escalated?",
        "🔧 Open tickets by equipment category?",
        "💊 NSTEMI treatment protocol?",
        "📅 Staff leave entitlements?",
        "⚠️ Fault codes requiring equipment removal?",
    ],
}

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
def init_state():
    for k, v in {
        "logged_in": False, "username": None, "role": None,
        "display_name": None, "dept": None, "initials": None,
        "user_color": "#2563eb", "messages": [],
        "show_debug": False, "api_key": "",
        "selected_model": MODEL,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
# Auto-load API key from Streamlit Cloud secrets if available
if not st.session_state.api_key:
    try:
        secret_key = st.secrets.get("GROQ_API_KEY", "")
        if secret_key:
            st.session_state.api_key = secret_key
    except Exception:
        pass
if not os.path.exists(DB_PATH):
    create_database()

# ─── LLM CALL (GROQ) ──────────────────────────────────────────────────────────
def call_llm(system: str, user: str, max_tokens: int = 1200) -> str:
    # Check session state → env var → Streamlit Cloud secrets (in that order)
    key = (st.session_state.get("api_key")
           or os.environ.get("GROQ_API_KEY", "")
           or st.secrets.get("GROQ_API_KEY", "") if hasattr(st, "secrets") else "")
    if not key:
        return "⚠️ No Groq API key. Enter it in the sidebar."
    model = st.session_state.get("selected_model", MODEL)
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": model, "max_tokens": max_tokens, "temperature": 0.2,
        "messages": [{"role":"system","content":system},{"role":"user","content":user}],
    }
    try:
        r = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.HTTPError:
        try:
            msg = r.json().get("error", {}).get("message", "HTTP error")
        except Exception:
            msg = r.text[:200]
        return f"⚠️ Groq API Error {r.status_code}: {msg}"
    except Exception as e:
        return f"⚠️ Request failed: {str(e)}"

# ─── SQL RAG ──────────────────────────────────────────────────────────────────
def run_sql_rag(question: str) -> dict:
    schema = get_db_schema()
    raw_sql = call_llm(
        "You are a SQLite expert. Return ONLY the SQL query, no explanation, no markdown.",
        f"{schema}\n\nQuestion: {question}\n\nSQL:",
        max_tokens=400,
    )
    sql_query = extract_sql(raw_sql)
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        conn.close()
        if not rows:
            results_str = "Query returned no results."
        else:
            lines = [" | ".join(cols), "─" * max(40, len(" | ".join(cols)))]
            for row in rows:
                lines.append(" | ".join(str(v) if v is not None else "—" for v in row))
            results_str = "\n".join(lines)
    except sqlite3.Error as e:
        return {"answer": f"⚠️ DB error: {e}\nSQL: `{sql_query}`",
                "sql_query": sql_query, "raw_results": None}

    answer = call_llm(
        "You are MediBot for MediAssist Health Network. Answer clearly from SQL results. Use bullet points for lists.",
        f'Question: "{question}"\n\nSQL:\n{sql_query}\n\nResults:\n{results_str}\n\nAnswer:',
        max_tokens=700,
    )
    return {"answer": answer, "sql_query": sql_query, "raw_results": results_str}

# ─── HYBRID RAG ───────────────────────────────────────────────────────────────
def run_hybrid_rag(question: str, role: str) -> dict:
    chunks, debug = hybrid_retrieve_and_rerank(question, role, rerank_top_k=4)
    if not chunks:
        return {"answer": "I couldn't find relevant information in your authorised collections. Try rephrasing.", "sources": [], "debug": debug}
    context = "\n\n---\n\n".join(
        f"[Source {i}: {c['source_document']} — {c['section_title']}]\n{c['content']}"
        for i, c in enumerate(chunks, 1)
    )
    meta = ROLE_META.get(role, {})
    system = f"""You are MediBot, the internal AI assistant for MediAssist Health Network.
User: {st.session_state.get('display_name','Staff')} | Role: {meta.get('label', role)} | Authorised: {', '.join(ROLE_COLLECTIONS.get(role,[]))}

Answer using ONLY the provided document context. Be precise, professional, cite exact codes/dosages/values.
Use bullet points for procedures. Do NOT hallucinate. Do NOT reveal information outside the user's authorised collections.

CONTEXT:
{context}"""
    answer = call_llm(system, question, max_tokens=1200)
    sources = [{"source_document":c["source_document"],"section_title":c["section_title"],"collection":c["collection"]} for c in chunks]
    return {"answer": answer, "sources": sources, "debug": debug}

def run_rag(question: str, role: str) -> dict:
    if role in ("billing_executive","admin") and is_analytical_query(question):
        r = run_sql_rag(question)
        return {"answer":r["answer"],"retrieval_type":"sql_rag","sources":[],
                "sql_query":r.get("sql_query"),"raw_results":r.get("raw_results"),"debug":{}}
    r = run_hybrid_rag(question, role)
    return {"answer":r["answer"],"retrieval_type":"hybrid_rag",
            "sources":r.get("sources",[]),"debug":r.get("debug",{})}

# ═══════════════════════════════════════════════════════════════════════════════
# ─── LOGIN SCREEN ─────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
def render_login():
    _, mid, _ = st.columns([0.8, 2.4, 0.8])
    with mid:
        # Hero
        st.markdown("""
        <div class="login-hero">
            <div class="login-icon-ring">🏥</div>
            <div class="login-title">MediBot</div>
            <div class="login-sub">
                MediAssist Health Network · Internal AI Assistant<br>
                <span style="color:#94a3b8;font-size:12px;">Powered by Groq ⚡ LLaMA-3.3-70B</span>
            </div>
            <div class="login-features">
                <span class="login-feat-chip">🔍 Hybrid RAG</span>
                <span class="login-feat-chip">🔒 Role-Based Access</span>
                <span class="login-feat-chip">🗄️ SQL Analytics</span>
                <span class="login-feat-chip">📄 Source Citations</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # API Key panel
        st.markdown("""
        <div class="key-panel">
            <div class="key-panel-title">🔑 Groq API Key Required</div>
            <div class="key-panel-sub">
                Get your free key at
                <a href="https://console.groq.com/keys" target="_blank"
                   style="color:#d97706;font-weight:600;">console.groq.com/keys</a>
                — 14,400 free requests/day
            </div>
        </div>
        """, unsafe_allow_html=True)

        key_val = st.text_input("Groq API Key", type="password",
            value=st.session_state.api_key, placeholder="gsk_...",
            label_visibility="collapsed")
        if key_val:
            st.session_state.api_key = key_val
            st.success(f"⚡ Groq connected · {MODEL}", icon="✅")
        else:
            st.warning("Paste your Groq API key above, then choose an account below", icon="⬆️")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 👤 Select Your Account")
        st.markdown("<br>", unsafe_allow_html=True)

        # User cards grid
        users_list = list(USERS.items())
        col_a, col_b = st.columns(2)
        for i, (uname, info) in enumerate(users_list):
            role = info["role"]
            meta = ROLE_META[role]
            colls = ROLE_COLLECTIONS.get(role, [])
            target_col = col_a if i % 2 == 0 else col_b
            with target_col:
                st.markdown(f"""
                <div class="user-card {meta['card_class']}">
                    <div class="uc-icon {meta['bg_class']}">{meta['icon']}</div>
                    <div class="uc-name">{info['display']}</div>
                    <div class="uc-dept">{info['dept']}</div>
                    <span class="role-badge {meta['badge']}">{meta['label']}</span>
                    <div class="uc-creds">{uname} · {info['password']}</div>
                    <div class="uc-access">Collections: {" · ".join(colls)}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Sign in as {info['display'].split()[0]} {info['display'].split()[1] if len(info['display'].split())>1 else ''} →",
                             key=f"login_{uname}", use_container_width=True):
                    if not st.session_state.api_key:
                        st.error("Enter your Groq API key first.")
                    else:
                        st.session_state.update({
                            "logged_in": True, "username": uname,
                            "role": info["role"], "display_name": info["display"],
                            "dept": info["dept"], "initials": info["initials"],
                            "user_color": info["color"], "messages": [],
                        })
                        st.rerun()

        st.markdown("""
        <div style="text-align:center;margin-top:24px;padding-bottom:16px;
             font-size:11px;color:#334155;">
            🔒 RBAC enforced at retrieval layer &nbsp;·&nbsp; All 11 PDFs indexed &nbsp;·&nbsp;
            30 claims · 21 maintenance tickets in DB
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
def render_sidebar():
    role = st.session_state.role
    meta = ROLE_META[role]
    colls = ROLE_COLLECTIONS.get(role, [])
    locked = sorted(set(COLLECTION_META.keys()) - set(colls))
    chunk_count = sum(1 for d in DOCUMENTS if d["collection"] in colls)

    with st.sidebar:
        # Logo banner
        st.markdown(f"""
        <div class="sb-logo">
            <div class="sb-logo-pulse">🏥</div>
            <div class="sb-logo-title">MediBot</div>
            <div class="sb-logo-sub">MediAssist Health Network</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # User card
        st.markdown(f"""
        <div class="sb-user-card">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                <div class="sb-avatar" style="background:linear-gradient(135deg,{st.session_state.user_color},{st.session_state.user_color}99);">
                    {st.session_state.initials}
                </div>
                <div>
                    <div class="sb-uname">{st.session_state.display_name}</div>
                    <div class="sb-udept">{st.session_state.dept}</div>
                </div>
            </div>
            <span class="role-badge {meta['badge']}">{meta['icon']} {meta['label']}</span>
            <div style="display:flex;align-items:center;margin-top:8px;gap:5px;font-size:11px;color:#3a6080 !important;">
                <span class="online-dot"></span> Online
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px;font-weight:600;color:#4a6080 !important;letter-spacing:1px;text-transform:uppercase;padding:4px 2px;">📂 Authorised Collections</div>', unsafe_allow_html=True)

        for c in colls:
            cm = COLLECTION_META[c]
            st.markdown(f'<div class="coll-chip {cm["chip"]}">{cm["icon"]} {cm["label"]}</div>', unsafe_allow_html=True)

        if locked:
            st.markdown('<div style="font-size:11px;font-weight:600;color:#374151 !important;letter-spacing:1px;text-transform:uppercase;padding:8px 2px 4px;">🔒 Restricted</div>', unsafe_allow_html=True)
            for c in locked:
                cm = COLLECTION_META[c]
                st.markdown(f'<div class="coll-chip coll-locked">🚫 {cm["label"]}</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:rgba(255,255,255,.03);border:1px solid rgba(99,179,237,0.1);
             border-radius:12px;padding:12px 14px;">
            <div class="stat-pill">📄 <span class="stat-pill-val">{chunk_count}</span> chunks accessible</div>
            <div class="stat-pill">🔍 BM25 + TF-IDF + RRF + Rerank</div>
            <div class="stat-pill">⚡ Groq · <span class="stat-pill-val">LLaMA-3.3-70B</span></div>
            {"<div class='stat-pill'>🗄️ <span class='stat-pill-val'>SQL RAG enabled</span></div>" if role in ("billing_executive","admin") else ""}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Model selector
        model_map = {
            "llama-3.3-70b-versatile": "⚡ LLaMA 3.3 70B (Best)",
            "llama-3.1-8b-instant":    "🚀 LLaMA 3.1 8B (Fastest)",
            "mixtral-8x7b-32768":      "🌀 Mixtral 8x7B (32k ctx)",
            "gemma2-9b-it":            "💎 Gemma2 9B (Light)",
        }
        chosen = st.selectbox(
            "🤖 Model",
            options=list(model_map.values()),
            index=0,
        )
        st.session_state.selected_model = [k for k,v in model_map.items() if v == chosen][0]

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.session_state.show_debug = st.toggle("🔬 Debug mode", value=st.session_state.show_debug)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="sb-signout">', unsafe_allow_html=True)
            if st.button("↩ Sign Out", use_container_width=True):
                st.session_state.update({
                    "logged_in": False, "username": None, "role": None,
                    "display_name": None, "dept": None, "initials": None,
                    "messages": [],
                })
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── MESSAGE RENDERERS ────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
def render_user_msg(content: str):
    content_safe = content.replace("<","&lt;").replace(">","&gt;")
    st.markdown(f"""
    <div class="msg-row-user">
        <div class="bubble-user">{content_safe}</div>
    </div>""", unsafe_allow_html=True)

def render_bot_msg(data: dict):
    answer = data.get("answer","")
    # Light markdown conversion for the answer
    answer_html = (answer
        .replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        .replace("\n\n","</p><p style='margin-top:8px;'>")
        .replace("\n","<br>")
    )
    answer_html = f"<p>{answer_html}</p>"
    # Bold **text**
    import re as _re
    answer_html = _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', answer_html)
    # Bullet conversion
    answer_html = answer_html.replace("<br>• ","</p><li>").replace("<br>- ","</p><li>")

    rtype  = data.get("retrieval_type","hybrid_rag")
    blabel = "🔍 Hybrid RAG" if rtype=="hybrid_rag" else "🗄️ SQL RAG"
    bclass = "ret-hybrid"    if rtype=="hybrid_rag" else "ret-sql"

    # Sources
    src_html = ""
    if data.get("sources"):
        chips = "".join(
            f'<span class="src-chip">📄 {s["source_document"]} <span style="color:#93c5fd;margin:0 2px;">·</span> '
            f'{s["section_title"][:44]}{"…" if len(s["section_title"])>44 else ""}</span>'
            for s in data["sources"]
        )
        src_html = f'<div class="sources-row">{chips}</div>'

    # SQL query
    sql_html = ""
    if data.get("sql_query"):
        sql_safe = data["sql_query"].replace("<","&lt;").replace(">","&gt;")
        sql_html = f'<details style="margin-top:10px;"><summary style="font-size:12px;color:#64748b;cursor:pointer;font-weight:500;">🗄️ View SQL query</summary><div class="sql-box">{sql_safe}</div></details>'

    st.markdown(f"""
    <div class="msg-row-bot">
        <div class="bot-avatar">🏥</div>
        <div class="bubble-bot">
            {answer_html}
            {src_html}
            <div style="margin-top:8px;">
                <span class="ret-badge {bclass}">{blabel}</span>
            </div>
            {sql_html}
        </div>
    </div>""", unsafe_allow_html=True)

    if st.session_state.show_debug and data.get("debug"):
        with st.expander("🔬 Retrieval pipeline debug"):
            st.json(data["debug"])

def render_blocked_msg(content: str):
    content_html = content.replace("\n","<br>")
    import re as _re
    content_html = _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content_html)
    st.markdown(f"""
    <div class="msg-row-blocked">
        <div class="blocked-avatar">🔒</div>
        <div class="bubble-blocked">{content_html}</div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── CHAT SCREEN ──────────────────────────────────────════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════
def render_chat():
    role     = st.session_state.role
    meta     = ROLE_META[role]
    colls    = ROLE_COLLECTIONS.get(role, [])
    is_fresh = not st.session_state.messages

    # ── Chat header ──
    COLL_BG = {'general': '#1e293b', 'clinical': '#052e16', 'nursing': '#0c1a3a', 'billing': '#2d1a00', 'equipment': '#1a0a3d'}
    COLL_FG = {'general': '#94a3b8', 'clinical': '#4ade80', 'nursing': '#60a5fa', 'billing': '#fbbf24', 'equipment': '#a78bfa'}
    hc1, hc2 = st.columns([5, 1])
    with hc1:
        coll_tags = " ".join(
            f'<span style="font-size:11px;background:{COLL_BG[c]};color:{COLL_FG[c]};'
            f'padding:2px 8px;border-radius:8px;margin-right:4px;">{COLLECTION_META[c]["icon"]} {c.title()}</span>'
            for c in colls
        )
        st.markdown(f"""
        <div style="padding:10px 0 14px;border-bottom:1px solid rgba(56,189,248,0.08);margin-bottom:16px;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                <div style="width:36px;height:36px;background:linear-gradient(135deg,#0f3460,#1d4ed8);
                     border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;
                     box-shadow:0 2px 8px rgba(29,78,216,.3);">🏥</div>
                <div>
                    <div style="font-family:'Space Grotesk',sans-serif;font-size:17px;font-weight:700;color:#f1f5f9;line-height:1.2;">
                        MediBot <span class="online-dot" style="margin-left:4px;"></span>
                        <span style="font-size:11px;font-weight:400;color:#10b981;vertical-align:middle;">Online</span>
                    </div>
                    <div style="font-size:11.5px;color:#475569;margin-top:2px;">
                        {meta['icon']} {st.session_state.display_name} &nbsp;·&nbsp;
                        {coll_tags}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with hc2:
        if st.button("🗑️ Clear", help="Clear conversation"):
            st.session_state.messages = []
            st.rerun()

    # ── Welcome banner ──
    if is_fresh:
        coll_icons = "  ".join(f"{COLLECTION_META[c]['icon']} **{c.title()}**" for c in colls)
        sql_note = " You also have **SQL RAG** — ask analytical questions about claims and equipment data." if role in ("billing_executive","admin") else ""
        st.markdown(f"""
        <div class="welcome-banner">
            <div class="welcome-icon">{meta['icon']}</div>
            <div class="welcome-text">
                Welcome, <strong>{st.session_state.display_name}</strong>! I can answer questions from your authorised collections:
                {coll_icons}.{sql_note}<br>
                <span style="font-size:12px;color:#3b82f6;">Use the quick questions below or type your own.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Quick questions ──
    qs = QUICK_QUESTIONS.get(role, [])
    if qs and is_fresh:
        st.markdown('<div style="font-size:12px;font-weight:600;color:#334155;letter-spacing:0.5px;margin:12px 0 6px;">💡 Quick Questions</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, q in enumerate(qs):
            with cols[i % 3]:
                if st.button(q, key=f"qq_{i}", use_container_width=True):
                    st.session_state.messages.append({"role":"user","content":q})
                    st.rerun()

    if not is_fresh:
        st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)

    # ── Message history ──
    for msg in st.session_state.messages:
        if   msg["role"] == "user":      render_user_msg(msg["content"])
        elif msg["role"] == "assistant": render_bot_msg(msg["data"])
        elif msg["role"] == "blocked":   render_blocked_msg(msg["content"])

    # ── Input bar ──
    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
    st.markdown('<div>', unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        fc1, fc2 = st.columns([7, 1])
        with fc1:
            user_input = st.text_input(
                "msg", label_visibility="collapsed",
                placeholder=f"Ask MediBot anything from your authorised collections… ({', '.join(colls)})",
            )
        with fc2:
            submitted = st.form_submit_button("Send ➤", use_container_width=True, type="primary")

    st.markdown('</div>', unsafe_allow_html=True)

    if submitted and user_input.strip():
        question = user_input.strip()
        st.session_state.messages.append({"role":"user","content":question})

        # RBAC guard
        is_viol, viol_msg = check_rbac_violation(question, role)
        if is_viol:
            st.session_state.messages.append({"role":"blocked","content":viol_msg})
            st.rerun()

        if not (st.session_state.get("api_key") or os.environ.get("GROQ_API_KEY","")):
            st.session_state.messages.append({"role":"blocked","content":"⚠️ No Groq API key found. Please sign out and enter your key."})
            st.rerun()

        with st.spinner("⚡ Searching your authorised collections via Groq…"):
            try:
                result = run_rag(question, role)
                st.session_state.messages.append({"role":"assistant","data":result})
            except Exception as e:
                st.session_state.messages.append({"role":"blocked","content":f"⚠️ Error: {str(e)}"})

        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# ─── MAIN ─────────────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    if not st.session_state.logged_in:
        render_login()
    else:
        render_sidebar()
        render_chat()

if __name__ == "__main__":
    main()
