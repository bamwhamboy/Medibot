"""
MediBot SQL RAG Module
Creates and queries the mediassist.db SQLite database.
Implements a 3-step SQL RAG chain:
  1. Translate NL question → SQL (LLM)
  2. Clean & extract SQL from LLM output
  3. Execute SQL → pass results to LLM for NL answer
"""

import sqlite3
import re
import os
# Note: LLM calls are handled in app.py via Groq API (no anthropic SDK needed)

DB_PATH = os.path.join(os.path.dirname(__file__), "mediassist.db")


# ─── DATABASE CREATION ────────────────────────────────────────────────────────

def create_database():
    """Create and populate the mediassist.db with realistic sample data."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ── Claims table ──────────────────────────────────────────────────────────
    cur.execute("""
    CREATE TABLE IF NOT EXISTS claims (
        claim_id        TEXT PRIMARY KEY,
        patient_id      TEXT NOT NULL,
        department      TEXT NOT NULL,
        icd_code        TEXT,
        diagnosis       TEXT,
        insurer         TEXT,
        claim_amount    REAL,
        approved_amount REAL,
        status          TEXT,      -- Approved, Pending, Rejected, Escalated, Under Review
        submission_date TEXT,
        settlement_date TEXT,
        rejection_code  TEXT,
        campus          TEXT
    )
    """)

    # ── Maintenance tickets table ─────────────────────────────────────────────
    cur.execute("""
    CREATE TABLE IF NOT EXISTS maintenance_tickets (
        ticket_id       TEXT PRIMARY KEY,
        asset_tag       TEXT NOT NULL,
        equipment_name  TEXT NOT NULL,
        category        TEXT,      -- Monitor, Infusion Pump, Autoclave, X-Ray Unit
        issue_type      TEXT,      -- Fault, Preventive, Calibration, Breakdown
        fault_code      TEXT,
        status          TEXT,      -- Open, In Progress, Resolved, Escalated
        priority        TEXT,      -- High, Medium, Low
        raised_date     TEXT,
        resolved_date   TEXT,
        campus          TEXT,
        assigned_to     TEXT
    )
    """)

    # ── Sample claims data ────────────────────────────────────────────────────
    claims_data = [
        # Approved
        ("CLM-2024-0001","P-10023","Cardiology","I21.4","NSTEMI","HDFC Ergo",120000,110000,"Approved","2024-01-05","2024-01-26",None,"Hyderabad Central"),
        ("CLM-2024-0002","P-10045","Orthopaedics","M17.0","Knee Osteoarthritis","Star Health",175000,165000,"Approved","2024-01-08","2024-01-30",None,"Pune Speciality"),
        ("CLM-2024-0003","P-10067","General Medicine","J18.9","Pneumonia","ICICI Lombard",45000,42000,"Approved","2024-01-10","2024-02-01",None,"Hyderabad Central"),
        ("CLM-2024-0004","P-10089","Nephrology","N18.3","CKD Stage 3","Niva Bupa",25200,24000,"Approved","2024-01-12","2024-02-03",None,"Mysuru Clinic Hub"),
        ("CLM-2024-0005","P-10101","Obstetrics","O82","LSCS","New India Assurance",52000,49000,"Approved","2024-01-15","2024-02-05",None,"Pune Speciality"),
        ("CLM-2024-0006","P-10112","Cardiology","I21.0","STEMI Anterior","Bajaj Allianz",185000,175000,"Approved","2024-01-18","2024-02-08",None,"Secunderabad"),
        ("CLM-2024-0007","P-10134","Gastroenterology","K35.2","Appendicitis","Care Health",65000,60000,"Approved","2024-01-20","2024-02-12",None,"Hyderabad Central"),
        ("CLM-2024-0008","P-10156","Neurology","I63.9","Cerebral Infarction","United India",98000,90000,"Approved","2024-01-22","2024-02-14",None,"Bengaluru Onco Centre"),
        ("CLM-2024-0009","P-10178","Ophthalmology","H25.9","Cataract","Star Health",26000,24000,"Approved","2024-02-01","2024-02-22",None,"Hyderabad Central"),
        ("CLM-2024-0010","P-10190","Cardiology","I50.0","Congestive Heart Failure","HDFC Ergo",95000,88000,"Approved","2024-02-03","2024-02-25",None,"Secunderabad"),
        ("CLM-2024-0011","P-10202","Endocrinology","E11.2","DM2 Renal Comp","Niva Bupa",55000,50000,"Approved","2024-02-05","2024-02-27",None,"Hyderabad Central"),
        ("CLM-2024-0012","P-10214","Orthopaedics","S72.0","Femoral Fracture","ICICI Lombard",210000,195000,"Approved","2024-02-08","2024-03-01",None,"Pune Speciality"),
        # Pending
        ("CLM-2024-0013","P-10226","Cardiology","I21.4","NSTEMI","Star Health",120000,None,"Pending","2024-02-10",None,None,"Secunderabad"),
        ("CLM-2024-0014","P-10238","Neurology","G40.9","Epilepsy","Bajaj Allianz",32000,None,"Pending","2024-02-12",None,None,"Hyderabad Central"),
        ("CLM-2024-0015","P-10250","General Surgery","K80.2","Cholelithiasis","Care Health",58000,None,"Pending","2024-02-14",None,None,"Hyderabad Central"),
        ("CLM-2024-0016","P-10262","General Medicine","A90","Dengue","HDFC Ergo",35000,None,"Pending","2024-02-16",None,None,"Mysuru Clinic Hub"),
        ("CLM-2024-0017","P-10274","Cardiology","I48.0","Atrial Fibrillation","United India",38000,None,"Pending","2024-02-18",None,None,"Secunderabad"),
        # Rejected
        ("CLM-2024-0018","P-10286","Dermatology","L57.0","Cosmetic Procedure","Niva Bupa",28000,0,"Rejected","2024-01-25",None,"EXCL-05","Hyderabad Central"),
        ("CLM-2024-0019","P-10298","General Medicine","J18.9","Pneumonia","Star Health",45000,0,"Rejected","2024-01-28",None,"EXCL-02","Pune Speciality"),
        ("CLM-2024-0020","P-10310","Orthopaedics","M17.0","Knee OA","ICICI Lombard",175000,0,"Rejected","2024-02-02",None,"EXCL-01","Pune Speciality"),
        ("CLM-2024-0021","P-10322","General Medicine","R50.9","Fever","Bajaj Allianz",15000,0,"Rejected","2024-02-05",None,"EXCL-07","Hyderabad Central"),
        # Escalated
        ("CLM-2024-0022","P-10334","Cardiology","I21.4","NSTEMI","HDFC Ergo",120000,None,"Escalated","2024-01-30",None,None,"Secunderabad"),
        ("CLM-2024-0023","P-10346","Neurology","I63.9","Stroke","United India",98000,None,"Escalated","2024-02-04",None,None,"Bengaluru Onco Centre"),
        ("CLM-2024-0024","P-10358","Nephrology","N17.9","AKI","New India Assurance",68000,None,"Escalated","2024-02-07",None,None,"Hyderabad Central"),
        # Under Review
        ("CLM-2024-0025","P-10370","Oncology","C34.1","Lung Malignancy","Star Health",250000,None,"Under Review","2024-02-09",None,None,"Bengaluru Onco Centre"),
        ("CLM-2024-0026","P-10382","Oncology","C50.9","Breast Malignancy","HDFC Ergo",280000,None,"Under Review","2024-02-11",None,None,"Bengaluru Onco Centre"),
        ("CLM-2024-0027","P-10394","Cardiology","I21.0","STEMI","Care Health",185000,None,"Under Review","2024-02-13",None,None,"Hyderabad Central"),
        ("CLM-2024-0028","P-10406","Gastroenterology","C18.9","Colon Malignancy","Niva Bupa",220000,None,"Under Review","2024-02-15",None,None,"Bengaluru Onco Centre"),
        # More approved (March)
        ("CLM-2024-0029","P-10418","General Medicine","J44.1","COPD Exacerbation","ICICI Lombard",42000,39000,"Approved","2024-03-01","2024-03-22",None,"Hyderabad Central"),
        ("CLM-2024-0030","P-10430","Cardiology","I21.4","NSTEMI","Bajaj Allianz",120000,115000,"Approved","2024-03-03","2024-03-25",None,"Secunderabad"),
    ]
    cur.executemany("""
    INSERT OR IGNORE INTO claims VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, claims_data)

    # ── Sample maintenance tickets data ───────────────────────────────────────
    tickets_data = [
        # Monitors
        ("TKT-2024-001","EQ-HYD-1042","BM-500 Monitor","Monitor","Fault","E-12","Resolved","High","2024-01-05","2024-01-06","Hyderabad Central","Ramesh Kumar"),
        ("TKT-2024-002","EQ-HYD-1087","BM-500 Monitor","Monitor","Preventive",None,"Resolved","Low","2024-01-10","2024-01-10","Hyderabad Central","Suresh Nair"),
        ("TKT-2024-003","EQ-SEC-0234","BM-500 Monitor","Monitor","Calibration",None,"Resolved","Medium","2024-01-15","2024-01-16","Secunderabad","Ramesh Kumar"),
        ("TKT-2024-004","EQ-HYD-1103","BM-500 Monitor","Monitor","Fault","E-07","In Progress","Medium","2024-02-01",None,"Hyderabad Central","Suresh Nair"),
        ("TKT-2024-005","EQ-PUN-0456","BM-500 Monitor","Monitor","Fault","E-02","Open","Low","2024-02-10",None,"Pune Speciality","Anand Pillai"),
        ("TKT-2024-006","EQ-BLR-0178","BM-500 Monitor","Monitor","Breakdown","E-12","Escalated","High","2024-02-18",None,"Bengaluru Onco Centre","Ramesh Kumar"),
        # Infusion Pumps
        ("TKT-2024-007","EQ-HYD-2031","DriveFlow IP-200","Infusion Pump","Fault","F-12","Resolved","High","2024-01-08","2024-01-09","Hyderabad Central","Anand Pillai"),
        ("TKT-2024-008","EQ-HYD-2045","DriveFlow IP-200","Infusion Pump","Preventive",None,"Resolved","Low","2024-01-12","2024-01-12","Hyderabad Central","Suresh Nair"),
        ("TKT-2024-009","EQ-SEC-1122","DriveFlow IP-200","Infusion Pump","Fault","F-03","Resolved","Medium","2024-01-20","2024-01-21","Secunderabad","Ramesh Kumar"),
        ("TKT-2024-010","EQ-HYD-2067","DriveFlow IP-200","Infusion Pump","Fault","F-01","In Progress","Medium","2024-02-05",None,"Hyderabad Central","Anand Pillai"),
        ("TKT-2024-011","EQ-PUN-1234","DriveFlow IP-200","Infusion Pump","Breakdown","F-12","Open","High","2024-02-14",None,"Pune Speciality","Suresh Nair"),
        ("TKT-2024-012","EQ-MYS-0089","DriveFlow IP-200","Infusion Pump","Calibration",None,"Open","Low","2024-02-20",None,"Mysuru Clinic Hub","Anand Pillai"),
        # Autoclaves
        ("TKT-2024-013","EQ-HYD-3001","SterilPro 3000","Autoclave","Fault","E-01","Resolved","High","2024-01-07","2024-01-08","Hyderabad Central","Ramesh Kumar"),
        ("TKT-2024-014","EQ-PUN-3002","SterilPro 3000","Autoclave","Preventive",None,"Resolved","Low","2024-01-25","2024-01-25","Pune Speciality","Anand Pillai"),
        ("TKT-2024-015","EQ-SEC-3003","SterilPro 3000","Autoclave","Fault","E-07","Open","High","2024-02-08",None,"Secunderabad","Suresh Nair"),
        ("TKT-2024-016","EQ-BLR-3004","SterilPro 3000","Autoclave","Breakdown","E-11","Escalated","High","2024-02-17",None,"Bengaluru Onco Centre","Ramesh Kumar"),
        # X-Ray Units
        ("TKT-2024-017","EQ-HYD-4001","RadiPro MX-150","X-Ray Unit","Fault","F-09","Resolved","High","2024-01-14","2024-01-15","Hyderabad Central","Anand Pillai"),
        ("TKT-2024-018","EQ-SEC-4002","RadiPro MX-150","X-Ray Unit","Calibration",None,"Resolved","Medium","2024-01-28","2024-01-29","Secunderabad","Suresh Nair"),
        ("TKT-2024-019","EQ-PUN-4003","RadiPro MX-150","X-Ray Unit","Fault","F-02","In Progress","Medium","2024-02-03",None,"Pune Speciality","Ramesh Kumar"),
        ("TKT-2024-020","EQ-BLR-4004","RadiPro MX-150","X-Ray Unit","Breakdown","F-09","Open","High","2024-02-22",None,"Bengaluru Onco Centre","Anand Pillai"),
        ("TKT-2024-021","EQ-HYD-4005","RadiPro MX-150","X-Ray Unit","Preventive",None,"Open","Low","2024-02-25",None,"Hyderabad Central","Suresh Nair"),
    ]
    cur.executemany("""
    INSERT OR IGNORE INTO maintenance_tickets VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, tickets_data)

    conn.commit()
    conn.close()
    return DB_PATH


def get_db_schema() -> str:
    """Return the database schema as a string for LLM context."""
    return """
Database: mediassist.db (SQLite)

TABLE: claims
  claim_id        TEXT PRIMARY KEY
  patient_id      TEXT
  department      TEXT          -- e.g. 'Cardiology', 'Orthopaedics', 'General Medicine'
  icd_code        TEXT          -- e.g. 'I21.4', 'J18.9'
  diagnosis       TEXT
  insurer         TEXT          -- e.g. 'HDFC Ergo', 'Star Health', 'ICICI Lombard'
  claim_amount    REAL          -- original claimed amount (INR)
  approved_amount REAL          -- approved payout (NULL if not yet settled)
  status          TEXT          -- 'Approved', 'Pending', 'Rejected', 'Escalated', 'Under Review'
  submission_date TEXT          -- YYYY-MM-DD
  settlement_date TEXT          -- YYYY-MM-DD (NULL if not settled)
  rejection_code  TEXT          -- e.g. 'EXCL-01', NULL if not rejected
  campus          TEXT          -- hospital campus name

TABLE: maintenance_tickets
  ticket_id       TEXT PRIMARY KEY
  asset_tag       TEXT          -- e.g. 'EQ-HYD-1042'
  equipment_name  TEXT          -- e.g. 'BM-500 Monitor', 'DriveFlow IP-200'
  category        TEXT          -- 'Monitor', 'Infusion Pump', 'Autoclave', 'X-Ray Unit'
  issue_type      TEXT          -- 'Fault', 'Preventive', 'Calibration', 'Breakdown'
  fault_code      TEXT          -- e.g. 'E-12', 'F-09', NULL for preventive tasks
  status          TEXT          -- 'Open', 'In Progress', 'Resolved', 'Escalated'
  priority        TEXT          -- 'High', 'Medium', 'Low'
  raised_date     TEXT          -- YYYY-MM-DD
  resolved_date   TEXT          -- YYYY-MM-DD (NULL if not resolved)
  campus          TEXT
  assigned_to     TEXT          -- technician name
"""


def extract_sql(llm_output: str) -> str:
    """
    Step 2: Extract just the SQL statement from LLM output.
    Handles markdown fences, explanation text, etc.
    """
    # Remove markdown code fences
    fenced = re.search(r"```(?:sql)?\s*([\s\S]+?)```", llm_output, re.IGNORECASE)
    if fenced:
        return fenced.group(1).strip()

    # Look for SELECT/WITH statement
    sql_match = re.search(
        r"((?:SELECT|WITH|INSERT|UPDATE|DELETE)[\s\S]+?);?\s*$",
        llm_output,
        re.IGNORECASE | re.MULTILINE,
    )
    if sql_match:
        sql = sql_match.group(1).strip()
        if not sql.endswith(";"):
            sql += ";"
        return sql

    # Fallback: return stripped output
    return llm_output.strip()
