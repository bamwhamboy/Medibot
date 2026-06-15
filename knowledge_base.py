"""
MediBot Knowledge Base
All document content extracted from PDFs, structured with metadata for RBAC filtering.
"""

DOCUMENTS = [
    # ─── BILLING COLLECTION ───────────────────────────────────────────────────
    {
        "source_document": "billing_codes.pdf",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Introduction & ICD-10 Coding Principles",
        "chunk_type": "text",
        "content": """Insurance Billing Code Reference — MediAssist Health Network (BILL-CODE-010 v8.0)
This reference maps diagnosis and procedure codes used in MediAssist claim submissions to insurer package rates.
ICD-10 codes describe the diagnosis (why the patient was treated). Procedure codes describe the intervention (what was done).
Specificity matters: an unspecified code invites a query or rejection. Always code to the highest level of detail supported by the clinical record.
Package rates are indicative MediAssist negotiated rates. Final settlement depends on the patient's policy, sum insured, co-pay and sub-limits.""",
    },
    {
        "source_document": "billing_codes.pdf",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Top ICD-10 Diagnosis Codes — Cardiac & Respiratory",
        "chunk_type": "table",
        "content": """Top ICD-10 Diagnosis Codes used at MediAssist:
I21.0 — STEMI anterior wall: LOS 5–7 days, Package ₹1,85,000, Pre-auth required
I21.4 — NSTEMI: LOS 3–5 days, Package ₹1,20,000, Pre-auth required
I50.0 — Congestive heart failure: LOS 4–6 days, Package ₹95,000, Pre-auth required
I48.0 — Atrial fibrillation: LOS 2–3 days, Package ₹38,000, No pre-auth
J18.9 — Pneumonia unspecified: LOS 4–6 days, Package ₹45,000, No pre-auth
J44.1 — COPD with acute exacerbation: LOS 4–5 days, Package ₹42,000, No pre-auth
J45.9 — Asthma unspecified: LOS 1–2 days, Package ₹18,000, No pre-auth
A90 — Dengue fever: LOS 3–5 days, Package ₹35,000, No pre-auth
A09 — Acute gastroenteritis: LOS 2–3 days, Package ₹22,000, No pre-auth
I63.9 — Cerebral infarction (stroke): LOS 6–8 days, Package ₹98,000, Pre-auth required
G40.9 — Epilepsy unspecified: LOS 2–3 days, Package ₹32,000, No pre-auth""",
    },
    {
        "source_document": "billing_codes.pdf",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Top ICD-10 Diagnosis Codes — Surgery, Orthopaedics & Other",
        "chunk_type": "table",
        "content": """More ICD-10 Diagnosis Codes:
E11.9 — Type 2 diabetes w/o complications: Day care, Package ₹8,500, No pre-auth
E11.2 — Type 2 diabetes with renal complications: LOS 3–4 days, Package ₹55,000, Pre-auth required
N18.3 — Chronic kidney disease stage 3 (dialysis): Day care, Package ₹4,200/session, Pre-auth required
N17.9 — Acute kidney injury: LOS 4–6 days, Package ₹68,000, Pre-auth required
K35.2 — Acute appendicitis with peritonitis: LOS 3–4 days, Package ₹65,000, Pre-auth required
K80.2 — Gallstones (cholelithiasis): LOS 2–3 days, Package ₹58,000, Pre-auth required
K40.9 — Inguinal hernia: LOS 1–2 days, Package ₹48,000, Pre-auth required
O80 — Normal spontaneous delivery: LOS 2 days, Package ₹28,000, No pre-auth
O82 — Delivery by caesarean section (LSCS): LOS 3–4 days, Package ₹52,000, Pre-auth required
S72.0 — Femoral neck fracture: LOS 7–10 days, Package ₹2,10,000, Pre-auth required
M17.0 — Primary osteoarthritis of knee: LOS 5–7 days, Package ₹1,75,000, Pre-auth required
D64.9 — Anaemia unspecified: Day care, Package ₹9,000, No pre-auth
R50.9 — Fever unspecified: LOS 1–2 days, Package ₹15,000, No pre-auth
I10 — Essential hypertension: Day care, Package ₹7,500, No pre-auth""",
    },
    {
        "source_document": "billing_codes.pdf",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Common Procedure Codes",
        "chunk_type": "table",
        "content": """Common Procedure Codes at MediAssist:
PROC-CARD-01 — Coronary angiography: Package ₹25,000, Day care
PROC-CARD-02 — PTCA with stent (single): Package ₹1,65,000, Inpatient
PROC-CARD-03 — Permanent pacemaker implant: Package ₹2,40,000, Inpatient
PROC-GSUR-01 — Appendicectomy (laparoscopic): Package ₹62,000, Inpatient
PROC-GSUR-02 — Laparoscopic cholecystectomy: Package ₹58,000, Inpatient
PROC-GSUR-03 — Hernia repair (mesh): Package ₹48,000, Inpatient
PROC-NEPH-01 — Haemodialysis per session: Package ₹4,200, Day care
PROC-ORTH-01 — Total knee replacement (unilateral): Package ₹1,75,000, Inpatient
PROC-ORTH-02 — Hip hemiarthroplasty: Package ₹2,10,000, Inpatient
PROC-OBGY-01 — LSCS (lower segment caesarean): Package ₹52,000, Inpatient
PROC-OPTH-01 — Cataract surgery (phaco + IOL): Package ₹26,000, Day care
PROC-GAST-01 — Upper GI endoscopy: Package ₹9,500, Day care
PROC-RAD-01 — MRI brain (plain): Package ₹8,000, Day care
PROC-RAD-02 — CT abdomen (contrast): Package ₹7,500, Day care
PROC-NEUR-01 — Thrombolysis for acute stroke: Package ₹85,000, Inpatient""",
    },
    {
        "source_document": "billing_codes.pdf",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Empanelled Insurer Panel",
        "chunk_type": "table",
        "content": """Empanelled Insurer Panel — confirm TPA before submitting:
Star Health: portal.starhealth.in, In-house TPA, 1800-425-2255
HDFC Ergo: claims.hdfcergo.com, In-house TPA, 1800-2700-700
ICICI Lombard: ilclaims.icicilombard.com, In-house TPA, 1800-2666
New India Assurance: claims.newindia.co.in, MedSave TPA, 1800-220-000
United India: claims.uiic.co.in, Medi Assist TPA, 1800-425-3333
Bajaj Allianz: claims.bajajallianz.com, In-house TPA, 1800-209-5858
Niva Bupa: claims.nivabupa.com, In-house TPA, 1860-500-8888
Care Health: claims.careinsurance.com, In-house TPA, 1800-102-4499""",
    },
    {
        "source_document": "billing_codes.pdf",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Exclusions Reference & Rejection Codes",
        "chunk_type": "table",
        "content": """Common Claim Exclusion / Rejection Codes:
EXCL-01 — Non-disclosure of pre-existing condition: Appealable with prior records
EXCL-02 — Treatment within policy waiting period: Usually upheld; verify dates
EXCL-03 — Treatment by non-empanelled provider: Reimbursement route only
EXCL-04 — Day-care procedure claimed as inpatient: Re-file under correct package
EXCL-05 — Cosmetic/aesthetic procedure: Excluded; usually final
EXCL-06 — Self-inflicted injury: Excluded per policy
EXCL-07 — Investigation-only admission (no treatment): Often disallowed
EXCL-08 — Documentation beyond claim deadline: Appeal with justification
Best practice: When a patient has multiple conditions, sequence the primary diagnosis first. Mis-sequencing is a frequent cause of package-rate disputes.""",
    },
    {
        "source_document": "billing_codes.pdf",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Room Rent, Sub-limits & Co-pay Reference",
        "chunk_type": "table",
        "content": """Room Rent & Sub-limit Reference:
General ward — Sum insured < ₹3 lakh
Twin sharing — Sum insured ₹3–5 lakh; proportionate deduction if upgraded
Single private — Sum insured ₹5–10 lakh; proportionate deduction if upgraded
Deluxe/suite — Sum insured > ₹10 lakh or rider; often excluded

Common Co-pay & Sub-limits:
Senior-citizen co-pay: 10–20% of admissible claim
Zone-based co-pay (metro vs non-metro): As per policy schedule
Cataract sub-limit: ₹25,000–₹40,000 per eye
Maternity sub-limit: ₹35,000 (normal) / ₹50,000 (LSCS) where covered
Ambulance charges: ₹2,000–₹5,000 per hospitalisation

Pre-authorisation Document Checklist:
- Completed insurer pre-authorisation form
- Admission note with provisional diagnosis and ICD-10 code
- Treating doctor's treatment plan and estimated length of stay
- Cost estimate mapped to the package rate
- Patient policy/e-card, photo ID and policy number
- For accidents: MLC number and FIR copy where applicable""",
    },
    # Claim Submission Guide
    {
        "source_document": "claim_submission_guide.md",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Cashless Claim Process — Pre-auth Timeline & Steps",
        "chunk_type": "text",
        "content": """Cashless Claim Process (BILL-OPS-011 v6.0):
Cashless is the default pathway for planned and emergency admissions where the patient holds a policy with an empanelled insurer.
Pre-authorisation timelines:
- Planned admission: at least 48 hours before admission
- Emergency admission: within 6 hours of admission
Missing the 6-hour emergency window is the single most common reason for avoidable cashless denials.

Documents required for pre-authorisation:
1. Insurer-specific pre-authorisation form
2. Admission note with provisional diagnosis and ICD-10 code from billing_codes.pdf
3. Treating doctor's treatment plan and estimated length of stay (LOS)
4. Cost estimate mapped to the relevant package rate
5. Patient KYC: policy card/e-card, government photo ID, policy number
6. For accident cases: MLC number and FIR copy

Step-by-step process:
1. Verify patient eligibility (policy active, sum insured available, waiting period cleared, room-rent category)
2. Counsel patient on room eligibility — exceeding eligible room rent triggers proportionate deduction
3. Create claim in MBP → Claims → New Cashless and attach documents
4. Submit via insurer portal AND log portal reference number in MBP
5. Record timestamp of submission — SLA clock starts here
6. Track status hourly until approval, query, or denial
7. On approval: record approved amount and pre-auth number in MBP; inform the ward
8. On query: respond within 2 hours with requested clinical documents""",
    },
    {
        "source_document": "claim_submission_guide.md",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Insurer Approval Turnaround SLAs",
        "chunk_type": "table",
        "content": """Typical Insurer Approval Turnaround (initial pre-auth):
Star Health: 2–4 hours (fastest; auto-adjudication for standard packages)
HDFC Ergo: 3–6 hours (frequent clinical queries on cardiac packages)
ICICI Lombard: 3–6 hours (TPA-routed; confirm TPA before submitting)
New India Assurance: 4–8 hours (PSU insurer; slower on weekends)
United India: 4–8 hours (manual review common)
Bajaj Allianz: 3–5 hours
Niva Bupa: 2–5 hours
Care Health: 3–6 hours
If no response within SLA window, escalate per the escalation matrix.""",
    },
    {
        "source_document": "claim_submission_guide.md",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Reimbursement Claim Process",
        "chunk_type": "text",
        "content": """Reimbursement Claim Process:
Used when the patient pays the hospital directly and claims from the insurer afterwards — typically when the insurer is not empanelled, patient chose not to use cashless, or cashless was declined for administrative reasons.

Documents required:
1. Original itemised hospital bills with payment receipts
2. Discharge summary signed by the treating consultant
3. Prescription copies and pharmacy invoices
4. Investigation reports (lab, radiology) supporting the diagnosis
5. Completed reimbursement claim form with patient NEFT/bank details
6. Cancelled cheque or passbook copy for payout
7. KYC documents and policy copy

Process:
1. Counsel patient at discharge that the claim is reimbursement, not cashless
2. Issue complete original document set and retain certified copies in MBP
3. Help patient fill the claim form; verify ICD-10 and procedure codes match the bills
4. Note the insurer's submission deadline — typically 30 days post-discharge (some allow 15, some 90)
5. Hand over document checklist and send written reminder of deadline""",
    },
    {
        "source_document": "claim_submission_guide.md",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Pre-Authorisation Enhancement",
        "chunk_type": "text",
        "content": """Pre-Authorisation Enhancement:
Raise an enhancement when the initially approved amount will not cover actual treatment cost.

When to raise:
- Projected final bill exceeds approved pre-auth amount by more than 10%
- A new procedure or implant (stent, prosthesis) is added mid-admission
- LOS extends beyond the approved package days

Documents required:
1. Enhancement request form referencing the original pre-auth number
2. Clinical justification note from treating doctor
3. Revised cost estimate and updated treatment plan
4. Any new investigation reports

Process:
1. Raise enhancement BEFORE the original approved amount is exhausted — never after discharge
2. Submit via insurer portal linked to original pre-auth, marked "Enhancement"
3. Track as a child claim under the parent pre-auth in MBP
4. If enhancement delayed beyond 6 hours and patient due for discharge, escalate to insurer nodal officer""",
    },
    {
        "source_document": "claim_submission_guide.md",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Claim Rejection Response & Appeal",
        "chunk_type": "text",
        "content": """Claim Rejection Response:
A rejection is not the end of the claim. Most rejections on administrative or documentation grounds are reversible on appeal.

Common rejection codes with responses:
EXCL-01 — Non-disclosure of pre-existing condition: Submit prior medical records/declaration
EXCL-02 — Treatment within waiting period: Verify policy dates; appeal if mis-calculated
EXCL-03 — Non-empanelled treating doctor/provider: Provide registration proof; or move to reimbursement
EXCL-04 — Day-care procedure claimed as inpatient: Re-submit under correct day-care package
EXCL-05 — Cosmetic/excluded procedure: Usually final; confirm exclusion in policy
EXCL-07 — Investigation-only admission: Provide clinical necessity note
EXCL-08 — Documentation beyond deadline: Appeal with justification for delay

Reconsideration/appeal must be filed within insurer's window — usually 90 days from rejection.
If appeal denied, escalate to insurer grievance cell, then Insurance Ombudsman.""",
    },
    {
        "source_document": "claim_submission_guide.md",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Escalation Matrix",
        "chunk_type": "table",
        "content": """Escalation Matrix (always escalate in writing and log each step in MBP):
Cashless pre-auth delayed: TPA helpline → Insurer nodal officer → MediAssist billing manager
Claim rejected (clinical grounds): Medical reviewer call → Written appeal with CMO sign-off → Insurance ombudsman
Payment delayed >30 days post-discharge: Accounts team → CFO office → Legal cell
Enhancement not approved before discharge: TPA helpline → Insurer nodal officer → MediAssist billing manager

Escalation discipline:
- Wait the stated window before moving to next level — premature escalation resets goodwill
- Every escalation email must quote claim ID, pre-auth number, patient ID, and SLA breached
- CC the campus billing manager on any escalation beyond first contact
- Never let more than 24 hours pass without escalation when a response is overdue""",
    },
    {
        "source_document": "claim_submission_guide.md",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Fraud Prevention & Controls",
        "chunk_type": "text",
        "content": """Fraud Prevention — Claim fraud is zero-tolerance:
Warning signs:
- Mismatch between diagnosis, procedure, and investigation reports
- Inflated or duplicated line items on the bill
- Documents that appear altered, back-dated, or inconsistent in handwriting/fonts
- Pressure from any party to "adjust" codes to a higher package rate (up-coding)
- Repeated claims for the same patient across facilities within a short period

Controls:
- Mandatory dual-check for any claim above ₹2,00,000 — second billing executive must independently verify
- Every claim must carry a complete audit trail in MBP with timestamps
- Claim files retained for minimum 7 years
- Never share insurer portal credentials

Reporting: Suspected fraud must be reported to Billing Manager and Internal Audit within 24 hours via MBP → Compliance → Report Concern or compliance@mediassist.in. Reports may be made confidentially. Retaliation against good-faith reporters is itself a disciplinary offence.""",
    },
    {
        "source_document": "claim_submission_guide.md",
        "collection": "billing",
        "access_roles": ["billing_executive", "admin"],
        "section_title": "Billing KPIs & Quick Reference Card",
        "chunk_type": "table",
        "content": """Billing Executive KPIs (monthly targets):
Pre-auth raised within SLA: >95% (drives same-day approvals)
Query response time: <2 hours (prevents avoidable rejections)
First-pass approval rate: >85% (reflects coding & documentation quality)
Claim rejection rate: <10% (quality and compliance indicator)
Average days to payment: <21 days (cash-flow health)
Reopened/appealed claims won: >60% (effectiveness of escalation)

Quick Reference Card (deadlines & SLAs):
Emergency cashless pre-auth: Within 6 hours of admission
Planned cashless pre-auth: 48 hours before admission
Response to insurer query: Within 2 hours
Reimbursement submission: Within 30 days of discharge
Rejection reconsideration: Within 90 days of rejection
Dual-check threshold: Claims >₹2,00,000
Fraud report: Within 24 hours of suspicion
Escalation cadence: No gap >24 hours when overdue""",
    },

    # ─── CLINICAL COLLECTION ─────────────────────────────────────────────────
    {
        "source_document": "treatment_protocols.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "Type 2 Diabetes Mellitus — Treatment Protocol",
        "chunk_type": "text",
        "content": """Type 2 Diabetes Mellitus — Standard Treatment Protocol (CLIN-PROT-005 v7.0)
ICD-10: E11

Diagnostic criteria:
- Fasting plasma glucose (FPG) ≥126 mg/dL, OR
- 2-hour plasma glucose ≥200 mg/dL on 75g OGTT, OR
- HbA1c ≥6.5% on a standardised assay

Pharmacological management:
First-line: Metformin 500 mg BD with meals — titrate to 1000 mg BD over 4 weeks
Second-line: Add Glipizide 5 mg OD — if HbA1c >7.5% after 3 months on Metformin
Third-line: Consider SGLT2 inhibitor / GLP-1 agonist — specialist-guided; review renal status

Monitoring:
- HbA1c every 3 months until stable, then 6-monthly
- Fasting blood glucose weekly for first month after any dose change
- Renal function (eGFR) and urine ACR annually; annual fundus and foot screening

Referral criteria:
- HbA1c >10% despite dual therapy → endocrinology referral
- eGFR <45 mL/min/1.73m² → nephrology referral and Metformin dose review""",
    },
    {
        "source_document": "treatment_protocols.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "Hypertension Stage 2 — Treatment Protocol",
        "chunk_type": "text",
        "content": """Hypertension — Stage 2 Treatment Protocol (ICD-10: I10)

Diagnostic criteria: Systolic BP ≥140 mmHg or diastolic BP ≥90 mmHg confirmed on two separate readings at least one week apart.

Pharmacological management:
First-line: Amlodipine 5 mg OD — titrate to 10 mg if target not met in 4 weeks; caution: ankle oedema
Second-line: Add Telmisartan 40 mg OD — avoid in pregnancy; monitor K⁺ and creatinine
Add-on: Hydrochlorothiazide 12.5–25 mg OD — monitor electrolytes; caution in gout

Monitoring:
- BP check at every visit; home BP diary encouraged
- Serum creatinine and potassium at baseline and 4 weeks after ACE-i/ARB initiation

Lifestyle modification targets:
- Dietary sodium: less than 2 g/day
- BMI: target below 25 kg/m²
- Alcohol: restrict to no more than 2 units/day
- Aerobic exercise: at least 30 minutes, 5 days a week""",
    },
    {
        "source_document": "treatment_protocols.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "Community-Acquired Pneumonia — Treatment Protocol",
        "chunk_type": "text",
        "content": """Community-Acquired Pneumonia — Treatment Protocol (ICD-10: J18.9)

Severity scoring — CURB-65:
One point each for: Confusion, Urea >7 mmol/L, Respiratory rate ≥30/min, BP <90/60 mmHg, Age ≥65 years.
Score 0–1: outpatient management
Score 2: hospital admission (general ward)
Score ≥3: consider ICU/HDU care

Antimicrobial therapy:
Outpatient: Amoxicillin 500 mg TDS for 5 days
Outpatient (atypical): Add Azithromycin 500 mg OD for 3 days
Inpatient: IV Piperacillin-Tazobactam 4.5g Q8H — switch to oral when afebrile >48h and CRP falling

Monitoring:
- SpO₂ monitoring every 4 hours during admission; target 94–98%
- Repeat chest X-ray at 6 weeks post-discharge to confirm resolution""",
    },
    {
        "source_document": "treatment_protocols.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "NSTEMI — Acute Myocardial Infarction Treatment Protocol",
        "chunk_type": "text",
        "content": """Acute Myocardial Infarction — NSTEMI Treatment Protocol (ICD-10: I21.4)

Immediate management (first 60 minutes):
- Aspirin 300 mg loading dose stat (chewed)
- Clopidogrel 300 mg loading dose (or Ticagrelor per cardiology)
- IV Heparin 60 units/kg bolus (maximum 4000 units), then infusion per protocol
- 12-lead ECG within 10 minutes of arrival
- High-sensitivity troponin at 0 and 3 hours

Risk stratification:
Calculate TIMI risk score. A score ≥3 indicates high risk and warrants early invasive strategy (coronary angiography within 24 hours).

Ongoing medications:
Atorvastatin 80 mg nocte — check LFTs at baseline
Metoprolol 25 mg BD — contraindicated in cardiogenic shock/acute LVF
Ramipril 2.5 mg OD from day 2 — only if BP stable; monitor renal function

Escalation: Cardiology on-call must be notified for all NSTEMI presentations within 15 minutes of diagnosis.
Billing: ICD-10 I21.4, Package ₹1,20,000, Pre-auth required, LOS 3–5 days""",
    },
    {
        "source_document": "treatment_protocols.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "Paediatric Fever Management Protocol",
        "chunk_type": "text",
        "content": """Paediatric Fever Management (ICD-10: R50.9)

Temperature-based approach:
<38°C: Observation; encourage fluids
38–38.9°C: Oral Paracetamol; reassess
≥39°C: Paracetamol + tepid sponging
≥40°C or febrile seizure: IV Paracetamol + urgent medical evaluation

Weight-based dosing:
<5 kg: Paracetamol oral 60 mg Q6H, IV 7.5 mg/kg Q6H, Ibuprofen NOT recommended
5–10 kg: Paracetamol oral 120 mg Q6H, IV 15 mg/kg Q6H, Ibuprofen oral 50 mg Q8H
10–20 kg: Paracetamol oral 250 mg Q6H, IV 15 mg/kg Q6H, Ibuprofen oral 100 mg Q8H
>20 kg: Paracetamol oral 500 mg Q6H, IV 15 mg/kg Q6H, Ibuprofen oral 200 mg Q8H

Danger signs — escalate urgently if any:
SpO₂ <94%, heart rate >180 in a child <1 year, altered consciousness, non-blanching rash, neck stiffness""",
    },
    {
        "source_document": "treatment_protocols.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "Dengue Fever — Management Protocol",
        "chunk_type": "text",
        "content": """Dengue Fever Management (ICD-10: A90 dengue, A91 dengue haemorrhagic fever)
Dengue is endemic across MediAssist's catchment, peaking in post-monsoon months. Management is supportive.

Classification:
Dengue without warning signs: Fever + 2 of (nausea, rash, aches, leucopenia) → Outpatient with daily review
Dengue with warning signs: Abdominal pain, persistent vomiting, mucosal bleed, lethargy, ↑HCT with ↓platelets → Admit for IV fluids
Severe dengue: Shock, fluid accumulation with respiratory distress, severe bleeding, organ impairment → ICU management

Management:
- Paracetamol for fever; AVOID NSAIDs and Aspirin (bleeding risk)
- Isotonic fluids (0.9% saline / Ringer's lactate) titrated to haematocrit and urine output
- Monitor platelet count and haematocrit every 12–24 hours
- Platelet transfusion only for significant bleeding or platelets <10×10⁹/L

Red flags: Narrowing pulse pressure (<20 mmHg) signals impending shock — immediate IV fluid resuscitation.""",
    },
    {
        "source_document": "treatment_protocols.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "COPD Acute Exacerbation — Treatment Protocol",
        "chunk_type": "text",
        "content": """Acute Exacerbation of COPD Treatment Protocol (ICD-10: J44.1)

Diagnostic features: Acute worsening of breathlessness, cough and sputum volume/purulence beyond normal variation in a known COPD patient.

Management:
Controlled oxygen: Target SpO₂ 88–92%; venturi mask; AVOID over-oxygenation
Bronchodilators: Salbutamol 2.5–5 mg + Ipratropium 500 µg nebulised Q6H
Corticosteroid: Prednisolone 40 mg OD oral for 5 days
Antibiotic (if purulent): Amoxicillin-Clavulanate 625 mg TDS or Doxycycline 100 mg BD
Consider NIV: If pH <7.35 with hypercapnia despite therapy

Monitoring & escalation:
- Arterial blood gas on arrival and after 1 hour of oxygen therapy
- Escalate to ICU/HDU for NIV failure, worsening acidosis, or reduced consciousness""",
    },
    {
        "source_document": "treatment_protocols.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "Key Drug Interactions & Cautions",
        "chunk_type": "table",
        "content": """Key Drug Interactions & Cautions (Appendix):
Azithromycin + other QTc-prolonging drugs: Prolonged QTc, arrhythmia risk — Review ECG; avoid stacking
ACE-i/ARB + Spironolactone: Hyperkalaemia — Monitor potassium closely
Metformin + iodinated contrast: Lactic acidosis if AKI — Withhold around contrast if eGFR low
Warfarin + Metronidazole/Macrolide: ↑INR, bleeding — Monitor INR; dose-adjust
NSAIDs + ACE-i + Diuretic ('triple whammy'): Acute kidney injury — AVOID combination
Clopidogrel + high-dose PPI: ↓antiplatelet effect — Prefer pantoprazole""",
    },
    # Drug Formulary
    {
        "source_document": "drug_formulary.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "Drug Formulary Tier System",
        "chunk_type": "text",
        "content": """MediAssist Approved Drug Formulary (PHAR-FORM-006 v9.0)
Tier system for drug authorisation:
Tier 1 — Generic first-line: Open to all prescribers, subsidised for staff
Tier 2 — Branded preferred: Open to all prescribers
Tier 3 — Specialist use: Requires HOD approval
Tier 4 — Restricted: Requires CMO approval
Substitution policy: When a Tier 2 drug is unavailable, pharmacist may substitute equivalent Tier 1 generic without prescription change. Tier 3/4 substitutions require prescribing doctor's written approval.""",
    },
    {
        "source_document": "drug_formulary.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "Antimicrobials Formulary",
        "chunk_type": "table",
        "content": """Antimicrobials Formulary:
Amoxicillin (Penicillin, Oral): 500 mg TDS, Tier 1, Room temp. Avoid in penicillin allergy.
Amoxicillin-Clavulanate (Penicillin/inhibitor, Oral/IV): 1.2 g Q8H, Tier 2, Room temp. GI upset common.
Piperacillin-Tazobactam (Beta-lactam/inhibitor, IV): 4.5 g Q8H, Tier 2, Refrigerate post-reconstitution. De-escalate on culture.
Ceftriaxone (3rd-gen cephalosporin, IV/IM): 1–2 g OD, Tier 2, Room temp. Avoid with calcium in neonates.
Azithromycin (Macrolide, Oral/IV): 500 mg OD, Tier 1, Room temp. QTc prolongation risk.
Clarithromycin (Macrolide, Oral): 500 mg BD, Tier 2, Room temp. Many drug interactions.
Meropenem (Carbapenem, IV): 1 g Q8H, Tier 3, Room temp. HOD approval required.
Vancomycin (Glycopeptide, IV): 15–20 mg/kg Q12H, Tier 3, Room temp. TDM; trough 15–20 mg/L.
Linezolid (Oxazolidinone, Oral/IV): 600 mg BD, Tier 3. Monitor platelets if >14 days.
Metronidazole (Nitroimidazole, Oral/IV): 500 mg TDS, Tier 1. Avoid alcohol.
Ciprofloxacin (Fluoroquinolone, Oral/IV): 500 mg BD, Tier 2. Avoid in children <18 yr.
Clindamycin (Lincosamide, Oral/IV): 600 mg Q8H, Tier 2. C. difficile risk.
Doxycycline (Tetracycline, Oral): 100 mg BD, Tier 1. Photosensitivity.
Fluconazole (Azole antifungal, Oral/IV): 150–400 mg OD, Tier 2. Hepatic monitoring.
Acyclovir (Antiviral, Oral/IV): 5–10 mg/kg Q8H, Tier 2. Maintain hydration.
Colistin (Polymyxin, IV): Per ideal body weight, Tier 4. CMO approval; nephrotoxic.""",
    },
    {
        "source_document": "drug_formulary.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "Cardiovascular Drugs Formulary",
        "chunk_type": "table",
        "content": """Cardiovascular Drugs:
Amlodipine (Oral): 5–10 mg OD, Tier 1. Contraindicated: severe aortic stenosis.
Telmisartan (Oral): 40–80 mg OD, Tier 1. Contraindicated: pregnancy, bilateral renal artery stenosis.
Atorvastatin (Oral): 10–80 mg nocte, Tier 1. Contraindicated: active liver disease.
Metoprolol (Oral/IV): 25–100 mg BD, Tier 1. Contraindicated: cardiogenic shock, 2°/3° heart block.
Ramipril (Oral): 2.5–10 mg OD, Tier 1. Contraindicated: pregnancy, angioedema history.
Aspirin (Oral): 75–300 mg OD, Tier 1. Contraindicated: active peptic ulcer, bleeding.
Clopidogrel (Oral): 75 mg OD (300 mg load), Tier 2. Contraindicated: active bleeding.
Digoxin (Oral/IV): 0.125–0.25 mg OD, Tier 2. Contraindicated: VF; toxicity if hypokalaemic.
Furosemide (Oral/IV): 20–80 mg OD/BD, Tier 1. Contraindicated: anuria, severe hypokalaemia.
Spironolactone (Oral): 25–50 mg OD, Tier 2. Contraindicated: hyperkalaemia, severe renal impairment.""",
    },
    {
        "source_document": "drug_formulary.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "Analgesics, Antipyretics & Respiratory Drugs",
        "chunk_type": "table",
        "content": """Analgesics & Antipyretics:
Paracetamol (Oral/IV/Suppository): 0.5–1 g Q6H (max 4 g/day). NOT controlled.
Ibuprofen (Oral): 200–400 mg Q8H. NOT controlled.
Diclofenac (Oral/IM): 50 mg BD–TDS. NOT controlled.
Tramadol (Oral/IV): 50–100 mg Q6H. Controlled (schedule).
Morphine (Oral/IV/SC): Titrated to effect. YES — narcotic register.
Fentanyl (IV/transdermal): Titrated; patch 12–100 µg/h. YES — narcotic register.
Buprenorphine (Sublingual/patch): Per pain protocol. Controlled (schedule).
Pregabalin (Oral): 75–150 mg BD. Controlled (schedule).

Respiratory Drugs:
Salbutamol (Inhaled/Neb): 100–200 µg PRN / 2.5–5 mg neb, Tier 1. Tremor, tachycardia.
Ipratropium (Inhaled/Neb): 500 µg Q6H neb, Tier 1. Dry mouth.
Budesonide (Inhaled): 200–400 µg BD, Tier 2. Rinse mouth; candidiasis risk.
Montelukast (Oral): 10 mg nocte, Tier 2. Neuropsychiatric caution.
Theophylline (Oral): Per level, Tier 3. Narrow therapeutic index; TDM required.""",
    },
    {
        "source_document": "drug_formulary.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "High-Alert Medications & Renal Dose Adjustments",
        "chunk_type": "text",
        "content": """High-Alert Medications (independent double-check required before administration):
Insulin: Refrigerate 2–8°C. Units NEVER abbreviated as 'U'; double-check dose.
Heparin: Room temp; separate from insulin. Double-check; aPTT monitoring.
Potassium Chloride (conc.): Locked; NEVER on open shelf. Never IV push; dilute and infuse.
Morphine: Narcotic cupboard, double-locked. Narcotic register entry per dose.
Methotrexate: Room temp; cytotoxic labelling. Weekly (NOT daily) dosing; confirm schedule.

Renal Dose Adjustments (selected drugs):
Metformin: eGFR 30–50 = max 1g/day; eGFR <30 = AVOID
Meropenem: eGFR 30–50 = reduce to Q12H; eGFR <30 = Q24H specialist input
Vancomycin: eGFR 30–50 = extend interval per TDM; eGFR <30 = per TDM close monitoring
Enoxaparin: eGFR 30–50 = standard with monitoring; eGFR <30 = reduce to OD; consider UFH
Digoxin: eGFR 30–50 = reduce dose, check levels; eGFR <30 = marked reduction; toxicity risk""",
    },
    {
        "source_document": "drug_formulary.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "LASA Medications & IV Fluids",
        "chunk_type": "table",
        "content": """Look-Alike Sound-Alike (LASA) Medications:
DOPamine vs DOBUTamine: Different haemodynamic effect; confirm infusion label
epHEDrine vs epINEPHrine: Very different potency; check ampoule
ceFAZolin vs cefTRIAXone: Confirm spectrum and indication
hydroXYzine vs hydrALAZINE: Antihistamine vs antihypertensive
clonazePAM vs cloNIDine: Anticonvulsant vs antihypertensive

IV Fluids Quick Reference:
0.9% Sodium Chloride (isotonic): Resuscitation, maintenance
Ringer's Lactate (isotonic balanced): Resuscitation; avoid in hyperkalaemia
5% Dextrose (isotonic→hypotonic): Free water; hypernatraemia
DNS 5% Dext + 0.9% NaCl (hypertonic): Maintenance with glucose
20% Mannitol (hypertonic): Raised intracranial pressure (specialist use)""",
    },
    # Diagnostic Reference
    {
        "source_document": "diagnostic_reference.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "Haematology & Biochemistry Reference Ranges",
        "chunk_type": "table",
        "content": """Haematology Reference Ranges (LAB-DIAG-007 v6.1):
Haemoglobin (male): Normal 13–17 g/dL; Critical <7 g/dL → Activate transfusion protocol
Haemoglobin (female): Normal 12–15 g/dL; Critical <7 g/dL → Activate transfusion protocol
WBC count: Normal 4–11×10⁹/L; Critical >30×10⁹/L → Haematology consult
Platelet count: Normal 150–400×10⁹/L; Critical <50×10⁹/L → Bleeding-risk protocol
PT/INR: Normal 0.9–1.2; Critical INR >5 → Withhold anticoagulant; review
aPTT: Normal 26–36s; Critical >90s → Review heparin; bleeding risk
D-dimer: Normal <0.5 µg/mL; Marked rise → Consider VTE

Biochemistry Reference Ranges:
Sodium: Normal 135–145 mEq/L; Critical <120 or >160 → Correct slowly
Potassium: Normal 3.5–5.0 mEq/L; Critical <3.0 or >6.0 → Cardiac monitoring if extreme
Creatinine: Normal 0.6–1.3 mg/dL; Rapid rise → Assess AKI; review nephrotoxics
Glucose (fasting): Normal 70–100 mg/dL; Critical <50 or >400
HbA1c: Normal <5.7%; ≥6.5% = diabetes
ALT/AST: Normal <40 U/L; >10× ULN = hepatocellular injury
Troponin I: Normal <0.04 ng/mL; >0.4 = significant → Serial; correlate with ECG
Procalcitonin: Normal <0.5 ng/mL; >2 ng/mL suggests bacterial sepsis""",
    },
    {
        "source_document": "diagnostic_reference.pdf",
        "collection": "clinical",
        "access_roles": ["doctor", "admin"],
        "section_title": "ECG Interpretation & ABG Reference",
        "chunk_type": "table",
        "content": """ECG Interpretation Quick Guide:
Rate: Normal 60–100 bpm; <60 bradycardia; >100 tachycardia
P-R interval: Normal 120–200 ms; >200 ms = 1° AV block
QRS duration: Normal <120 ms; >120 ms = bundle branch block
QTc: Normal <440 ms (male), <460 ms (female); Prolonged → arrhythmia risk
ST elevation: Isoelectric normally; >1 mm in ≥2 contiguous leads = STEMI protocol

Common arrhythmias:
AF — irregularly irregular, absent P waves
VT — broad-complex, regular, >100 bpm; medical emergency
SVT — narrow-complex tachycardia, often regular

Arterial Blood Gas (ABG) Interpretation:
pH: Normal 7.35–7.45; <7.35 acidosis; >7.45 alkalosis
PaCO₂: Normal 35–45 mmHg (respiratory component)
HCO₃⁻: Normal 22–26 mEq/L (metabolic component)
PaO₂: Normal 80–100 mmHg; <60 = respiratory failure
Lactate: Normal 0.5–2.2 mmol/L; >4 suggests hypoperfusion/sepsis; ≥2 triggers sepsis-6 review""",
    },

    # ─── NURSING COLLECTION ──────────────────────────────────────────────────
    {
        "source_document": "icu_nursing_procedures.pdf",
        "collection": "nursing",
        "access_roles": ["nurse", "doctor", "admin"],
        "section_title": "SOP 1 — Central Venous Catheter (CVC) Care",
        "chunk_type": "text",
        "content": """SOP 1 — Central Venous Catheter (CVC) Care (NURS-ICU-008 v5.0)

Frequency: Dressing change every 72 hours, or sooner if soiled, loose, or no longer occlusive.

Equipment checklist:
- Sterile gloves and sterile dressing pack
- Chlorhexidine 2% in 70% alcohol solution
- Sterile drape, transparent semi-permeable dressing, date label

Procedure:
1. Perform hand hygiene and don PPE
2. Remove old dressing and discard in yellow (biomedical) bin
3. Inspect insertion site for redness, swelling, or discharge
4. Perform hand hygiene again and apply sterile gloves
5. Clean site with chlorhexidine using concentric (inside-out) motion
6. Allow to air-dry for at least 30 seconds — do NOT fan or blow
7. Apply new transparent dressing
8. Label dressing with date and your initials
9. Document procedure and site assessment in care record

Escalate to doctor immediately for: purulent discharge, fever >38.5°C with no other source, or tracking erythema extending >2 cm from insertion site.""",
    },
    {
        "source_document": "icu_nursing_procedures.pdf",
        "collection": "nursing",
        "access_roles": ["nurse", "doctor", "admin"],
        "section_title": "SOP 2 — Mechanical Ventilator Management",
        "chunk_type": "text",
        "content": """SOP 2 — Mechanical Ventilator Management

Initial settings:
Mode: Assist-control / Volume-control (AC/VC)
Tidal volume: 6–8 mL/kg ideal body weight
Respiratory rate: 12–16 breaths/min
FiO₂: Start 1.0, then titrate to SpO₂ 94–98%
PEEP: 5 cmH₂O (default)

Hourly monitoring:
- SpO₂, end-tidal CO₂ (EtCO₂)
- Peak and plateau airway pressures
- Delivered tidal volume
- Ventilator alarm status

Alarm response:
High pressure (>40 cmH₂O): Check for secretions/kinking/coughing → suction if indicated → call doctor if persists
Low SpO₂ (<90%): Increase FiO₂ → assess airway and circuit → call doctor immediately

VAP prevention bundle:
- Head of bed (HOB) elevation 30–45°
- Oral care with chlorhexidine every 4 hours
- Subglottic suctioning where available
- Daily sedation vacation and readiness-to-wean assessment""",
    },
    {
        "source_document": "icu_nursing_procedures.pdf",
        "collection": "nursing",
        "access_roles": ["nurse", "doctor", "admin"],
        "section_title": "SOP 3 — Nasogastric Tube (NGT) Insertion & Management",
        "chunk_type": "text",
        "content": """SOP 3 — Nasogastric Tube (NGT) Insertion & Management

Sizing: Adult 14–16 Fr; Paediatric: select by age-appropriate formula.

Insertion procedure:
1. Measure from tip of nose to earlobe to xiphoid process; mark the tube
2. Lubricate tip with water-soluble gel
3. Insert through nostril, advancing gently
4. Ask patient to swallow (sips of water if permitted) as you advance
5. Advance to measured length
6. Confirm position by aspirate pH <5.5 AND chest X-ray before first feed

Feeding & gastric residual monitoring (GRV checked every 4 hours):
Initiation: Start at 20 mL/hr
GRV <200 mL: Increase by 20 mL/hr every 4 hours
GRV 200–400 mL: Hold feed 1 hour and recheck
GRV >400 mL: Hold feed; notify dietitian and doctor

SAFETY: Never confirm NGT position by auscultation alone before feeding.""",
    },
    {
        "source_document": "icu_nursing_procedures.pdf",
        "collection": "nursing",
        "access_roles": ["nurse", "doctor", "admin"],
        "section_title": "SOP 4 — IV Cannula Insertion & Sizing",
        "chunk_type": "text",
        "content": """SOP 4 — IV Cannula Insertion

Site selection (order of preference): Forearm → antecubital fossa → dorsum of hand. Avoid legs except in emergency.

Cannula sizing by indication:
Blood transfusion: ≥18G
Rapid fluid resuscitation: ≥16G
Routine medication: 20–22G
Paediatric <5 kg: 24G
Paediatric 5–20 kg: 22G
Paediatric >20 kg: 20G

Failed attempt protocol:
- Maximum 2 attempts per nurse
- After 2 failed attempts, escalate to senior nurse or doctor

Cannula change: Replace every 72–96 hours, or immediately if signs of phlebitis (Visual Infusion Phlebitis [VIP] score ≥2).""",
    },
    {
        "source_document": "icu_nursing_procedures.pdf",
        "collection": "nursing",
        "access_roles": ["nurse", "doctor", "admin"],
        "section_title": "SOP 5 — Patient Restraint Protocol",
        "chunk_type": "text",
        "content": """SOP 5 — Patient Restraint Protocol

Principle: Restraint is a LAST RESORT to prevent imminent harm (self-extubation, falls) and must NEVER be used as routine care or for staff convenience.

Authorisation:
- Requires verbal doctor's order, with written order within 1 hour
- Re-authorisation required every 24 hours

Monitoring while restrained:
- Neurovascular check every 2 hours — circulation, sensation and movement in restrained limb
- Offer range-of-motion exercises every 2 hours
- Document every check

Documentation requirements:
- Reason for restraint and alternatives tried
- Time applied and type of restraint
- All monitoring observations
- Communication with the family""",
    },
    {
        "source_document": "icu_nursing_procedures.pdf",
        "collection": "nursing",
        "access_roles": ["nurse", "doctor", "admin"],
        "section_title": "SOP 6 — Endotracheal Suctioning",
        "chunk_type": "text",
        "content": """SOP 6 — Endotracheal Suctioning (performed only when clinically indicated, not on fixed routine)

Indications:
- Visible or audible secretions / coarse breath sounds
- Rising peak airway pressure or falling tidal volume
- Desaturation or sawtooth pattern on flow-volume loop

Procedure:
1. Hand hygiene; don gloves, apron and eye protection
2. Pre-oxygenate with FiO₂ 1.0 for 30–60 seconds
3. Use closed in-line suction catheter where available; select catheter ≤ half the ETT internal diameter
4. Insert WITHOUT suction; apply suction on withdrawal for no more than 10–15 seconds
5. Limit to two passes; allow recovery between passes
6. Return ventilator settings to baseline and reassess
7. Document secretion colour, volume and patient's tolerance

Stop suctioning immediately for SpO₂ <90%, bradycardia, or new arrhythmia — re-oxygenate the patient.""",
    },
    {
        "source_document": "icu_nursing_procedures.pdf",
        "collection": "nursing",
        "access_roles": ["nurse", "doctor", "admin"],
        "section_title": "SOP 7 — Pressure Injury Prevention",
        "chunk_type": "text",
        "content": """SOP 7 — Pressure Injury Prevention

Risk assessment: Assess every ICU patient using Braden Scale on admission and at least every 24 hours. Score ≤18 indicates increased risk.

Preventive bundle:
- Repositioning: Turn patient every 2 hours and document the position
- Support surface: Use pressure-redistributing mattress for high-risk patients
- Skin inspection: Inspect bony prominences each shift
- Moisture management: Keep skin clean and dry; apply barrier cream as needed
- Nutrition: Refer at-risk patients to the dietitian

Staging quick reference:
Stage 1: Non-blanching erythema with intact skin
Stage 2: Partial-thickness skin loss; a shallow open ulcer
Stage 3: Full-thickness skin loss with fat visible
Stage 4: Full-thickness tissue loss with muscle or bone visible""",
    },
    # Infection Control
    {
        "source_document": "infection_control.pdf",
        "collection": "nursing",
        "access_roles": ["nurse", "doctor", "admin"],
        "section_title": "Five Moments of Hand Hygiene & PPE Guide",
        "chunk_type": "text",
        "content": """Infection Control Guidelines (NURS-IC-009 v4.2)

Five Moments of Hand Hygiene (WHO framework):
1. Before patient contact — to protect the patient from your hands
2. Before an aseptic procedure — to protect the patient from infection
3. After body-fluid exposure risk — to protect yourself and the environment
4. After patient contact — to protect yourself and the environment
5. After contact with patient surroundings — to protect yourself and the environment

Technique:
- Alcohol-based hand rub: 20–30 seconds
- Soap-and-water handwash: 40–60 seconds
- Use soap and water when hands are visibly soiled or after caring for C. difficile patient

PPE Selection Guide:
Routine patient contact: Gloves only
Contact with blood/body fluids: Gloves + Apron + Surgical mask (if splash risk) + Eye protection
Suspected respiratory infection: Gloves + Apron/Gown + N95 + Goggles/shield
Aerosol-generating procedure: Gloves + Full gown + N95/PAPR + Full face shield
Aerosol-generating procedures include: intubation, extubation, bronchoscopy, open suctioning, non-invasive ventilation.""",
    },
    {
        "source_document": "infection_control.pdf",
        "collection": "nursing",
        "access_roles": ["nurse", "doctor", "admin"],
        "section_title": "Transmission-Based Precautions & HAI Surveillance",
        "chunk_type": "table",
        "content": """Transmission-Based Precautions:
Contact (MRSA, VRE, C. difficile, norovirus): Single room preferred; dedicated equipment; visitors gown + gloves
Droplet (Influenza, pertussis, meningococcus): Surgical mask within 1 metre; single room preferred
Airborne (TB, measles, chickenpox): Negative-pressure room; N95; limit patient transport

Isolation Signage:
Contact: Yellow sign — gown and gloves before entry
Droplet: Blue sign — surgical mask within 1 metre
Airborne: Red sign — N95 plus negative-pressure room

HAI Surveillance (four under active surveillance):
CAUTI — catheter-associated urinary tract infection
CLABSI — central line-associated bloodstream infection
VAP — ventilator-associated pneumonia
SSI — surgical site infection
Any suspected HAI must be reported to infection control nurse within 24 hours.
A root-cause analysis (RCA) is conducted for every confirmed HAI.""",
    },
    {
        "source_document": "infection_control.pdf",
        "collection": "nursing",
        "access_roles": ["nurse", "doctor", "admin"],
        "section_title": "Waste Segregation & Sharps Injury Management",
        "chunk_type": "table",
        "content": """Waste Segregation (segregate at point of generation):
Yellow bin: Biomedical/infectious — dressings, blood-soaked items, body fluids
Red bin: Anatomical/contaminated plastics — tubing, catheters, IV sets
Blue/White translucent bin: Glassware & sharps — vials, ampoules, needles (puncture-proof)
Black bin: General (non-hazardous) — office and domestic waste
White (cytotoxic) bin: Cytotoxic/pharmaceutical — chemotherapy waste

Needlestick & Sharps Injury Management (medical emergency — act immediately):
1. Encourage wound to bleed gently; wash with soap and running water (do not scrub)
2. Do NOT suck the wound; for splashes to eyes/mouth, irrigate with water or saline
3. Report to shift in-charge; attend Emergency department / occupational health without delay
4. Identify source patient; risk-assess for HIV, Hepatitis B and Hepatitis C
5. Commence PEP if indicated — ideally within 2 hours, and no later than 72 hours for HIV
6. Complete incident report and arrange baseline and follow-up serology

Prevention: Never recap needles. Dispose in puncture-proof sharps container, filled no more than three-quarters.""",
    },

    # ─── EQUIPMENT COLLECTION ────────────────────────────────────────────────
    {
        "source_document": "equipment_manual.pdf",
        "collection": "equipment",
        "access_roles": ["technician", "admin"],
        "section_title": "Patient Monitoring System — MediAssist BM-500",
        "chunk_type": "text",
        "content": """Patient Monitoring System — MediAssist BM-500 (BME-EQManual-012 v7.0)
Multi-parameter monitor for ECG, SpO₂, NIBP, respiratory rate and temperature. 12-inch colour display; 4-hour battery backup.

Setup procedure:
1. Power on and allow self-test to complete (~45 seconds)
2. Enter patient ID
3. Connect leads in order: ECG leads first, then SpO₂ probe, then BP cuff
4. Confirm valid trace on each parameter before leaving bedside

Alarm parameter defaults:
SpO₂: Default 90–100% (adjustable 80–100%)
Heart Rate: Default 50–120 bpm (adjustable 30–250 bpm)
NIBP Systolic: Default 90–160 mmHg (adjustable 60–240 mmHg)
Temperature: Default 35.5–38.5°C (adjustable 34–42°C)

Fault codes:
E-01: ECG lead off → Re-attach/replace lead
E-02: SpO₂ probe disconnected → Reconnect or replace probe
E-03: NIBP cuff leak → Check cuff and tubing; replace cuff
E-07: Battery low (<15%) → Connect to mains; service battery if recurrent
E-12: Internal sensor failure → REMOVE FROM SERVICE IMMEDIATELY; log in CMMS

Maintenance:
Daily: Clean display with 70% IPA wipe; verify alarm audibility; check battery charge
Monthly: SpO₂ verification against reference pulse oximeter
6-monthly: NIBP calibration (tolerance ±3 mmHg)""",
    },
    {
        "source_document": "equipment_manual.pdf",
        "collection": "equipment",
        "access_roles": ["technician", "admin"],
        "section_title": "Infusion Pump — DriveFlow IP-200",
        "chunk_type": "text",
        "content": """Infusion Pump — DriveFlow IP-200
Syringe and volumetric infusion pump with DERR software and drug library of 150 pre-programmed protocols.

Programming steps:
1. Select infusion mode (syringe or volumetric)
2. Enter drug name from on-board library
3. Enter patient weight; system calculates safe dose range
4. Confirm rate against displayed limits
5. Start infusion and verify running display

Occlusion pressure alarm settings:
Default: 300 mmHg; Venous lines: reduce to 200 mmHg; Arterial lines: maintain at 300 mmHg

High-alert drug protocols (hard limits — cannot be overridden): Dopamine, Dobutamine, Noradrenaline, Insulin, Heparin, Morphine

Fault codes:
F-01: Air in line → Purge line; check connections
F-03: Occlusion → Check for kinks/clamps; restart
F-05: Door open → Close door securely
F-08: Battery failure → Service battery; use mains
F-12: Drug library update required → REMOVE FROM SERVICE; update library; log in CMMS

Maintenance schedule:
After each patient use: Clean with 70% IPA
Weekly: Functional check by biomedical team
Annual: Full service by authorised service engineer
Every 18 months: Replace battery""",
    },
    {
        "source_document": "equipment_manual.pdf",
        "collection": "equipment",
        "access_roles": ["technician", "admin"],
        "section_title": "Autoclave Steriliser — SterilPro 3000",
        "chunk_type": "text",
        "content": """Autoclave Steriliser — SterilPro 3000
134-litre chamber steam steriliser supporting gravity and pre-vacuum cycles.

Cycle selection:
Gravity 121°C: 103 kPa, 15 min hold — for unwrapped instruments, fluids
Gravity 134°C: 206 kPa, 3 min hold — for unwrapped solid instruments
Pre-vacuum 134°C: 206 kPa, 3.5 min hold — for wrapped sets, porous & hollow loads

Routine testing:
Bowie-Dick test: Mandatory every morning before first load. FAIL = DO NOT USE; call biomedical team
Biological indicator (BI) test: Weekly. Positive result = quarantine all loads from that week; notify infection control

Daily log requirements (every cycle): cycle number, cycle type, temperature/pressure chart, pass/fail result, operator ID, load contents

Fault codes:
E-01: Door seal failure → Inspect/replace gasket; leak test
E-04: Steam generator low water → Refill/check supply
E-07: Temperature sensor fault → DO NOT USE; call biomedical
E-11: Vacuum pump failure → Do not run pre-vacuum cycle; service pump""",
    },
    {
        "source_document": "equipment_manual.pdf",
        "collection": "equipment",
        "access_roles": ["technician", "admin"],
        "section_title": "Portable X-Ray Unit — RadiPro MX-150",
        "chunk_type": "text",
        "content": """Portable X-Ray Unit — RadiPro MX-150
150 kW mobile X-ray unit with wireless DR panel, DICOM compatibility, battery operation (~50 exposures/charge).

Technique chart:
Chest AP (adult): 90 kVp, 5 mAs, No grid. Erect preferred.
Chest AP (paediatric): 70 kVp, 3 mAs, No grid. Short exposure time.
Abdomen AP: 80 kVp, 15 mAs, Grid required. Expiration phase.
Pelvis: 85 kVp, 20 mAs, Grid required. Gonad shielding.
Knee AP: 65 kVp, 8 mAs, No grid.

Radiation safety:
- All personnel stand >2 m from unit or behind protective barrier during exposure
- Operator must wear dosimetry badge at all times
- Log exposure count weekly

Fault codes:
F-02: DR panel not detected → Re-pair panel; check battery
F-05: Battery below 20% → Charge before use
F-09: kV generator fault → REMOVE FROM SERVICE IMMEDIATELY; log in CMMS

Maintenance:
Monthly: Clean, battery check, exposure-counter log
Quarterly: HV cable inspection, collimator check
Annual: kV/mAs calibration by service engineer + radiation-leakage test
Battery: Replace every 3 years; do not store fully discharged""",
    },
    {
        "source_document": "equipment_manual.pdf",
        "collection": "equipment",
        "access_roles": ["technician", "admin"],
        "section_title": "Preventive Maintenance Calendar & Commissioning",
        "chunk_type": "table",
        "content": """Preventive Maintenance Calendar Summary:
BM-500 Monitor: Daily (clean, battery), Monthly (SpO₂ check, NIBP 6-monthly), Annual (full service)
DriveFlow IP-200: After each use (clean), Weekly (functional check), Annual (service + 18-mo battery)
SterilPro 3000: Daily (Bowie-Dick), Weekly (BI test), Monthly (seal inspection), Annual (validation & calibration)
RadiPro MX-150: Weekly (exposure log), Monthly (clean, battery), Annual (kV/mAs calibration; leakage test)

Fault codes mandating immediate removal from service:
E-12 (BM-500): Internal sensor failure → Remove from service; raise ticket
F-12 (DriveFlow IP-200): Drug library update required → Remove from service; raise ticket
F-09 (RadiPro MX-150): kV generator fault → Remove from service; raise ticket

Commissioning & Acceptance Testing (every new or repaired device):
- Electrical safety: earth leakage within IEC 60601 limits
- Functional test: all parameters within manufacturer tolerance
- Calibration certificate: valid and on file
- Asset tagging: EQ-CAMPUS-XXXX label applied and registered
- User training: ward staff trained and sign-off recorded

Decontamination before service: No device may be handed to biomedical engineering until decontaminated and certificate attached.""",
    },

    # ─── GENERAL COLLECTION ──────────────────────────────────────────────────
    {
        "source_document": "leave_policy.pdf",
        "collection": "general",
        "access_roles": ["doctor", "nurse", "billing_executive", "technician", "admin"],
        "section_title": "Leave Types & Entitlements",
        "chunk_type": "table",
        "content": """Leave & Attendance Policy (HR-LEAVE-002 v4.1) — Applies to all permanent employees

Leave Entitlements:
Earned Leave (EL): Clinical staff 15 days/yr; Non-clinical 18 days/yr; Carry forward max 30 days
Sick Leave (SL): 12 days/yr for all; Medical certificate required beyond 3 consecutive days
Casual Leave (CL): Clinical staff 8 days/yr; Non-clinical 10 days/yr; Cannot be clubbed with EL
Maternity Leave: 182 days (per Maternity Benefit Act, 1961)
Paternity Leave: 7 days; Within 3 months of child's birth
Bereavement Leave: 3 days; Immediate family only
Study Leave: 5 days/yr (clinical staff only); CME/certification courses only
Compensatory Off: As accrued; avail within 60 days of accrual""",
    },
    {
        "source_document": "leave_policy.pdf",
        "collection": "general",
        "access_roles": ["doctor", "nurse", "billing_executive", "technician", "admin"],
        "section_title": "Leave Application Process & On-Call Compensation",
        "chunk_type": "text",
        "content": """Leave Application Process:
All leave is applied through MediAssist HR Portal. Verbal approvals are NOT valid.

Notice periods:
Earned Leave (EL): Apply at least 7 days in advance; supervisor approves; HOD if longer than 5 days
Casual Leave (CL): Apply at least 2 days in advance; immediate supervisor approves
Sick Leave (SL): Notify same day via app; supervisor regularises on return

Approval rule: Any leave longer than 5 consecutive days requires HOD approval, regardless of leave type.

Attendance tracking:
- Biometric punch and mobile check-in app (geo-fenced to campus)
- Grace period: 10 minutes applies to shift start times
- Late arrival beyond grace period recorded; after 3 occurrences in calendar month, each further late arrival is marked as half-day
- Missed punches must be regularised within 48 hours

On-Call Compensation:
Resident doctors: ₹800/night; ₹1,600 on Sundays and public holidays
Nurses: ₹500/night; ₹1,000 on Sundays and public holidays

Leave Encashment:
Accumulated EL above 30-day carry-forward cap encashed annually each March (basic salary).
On separation, full EL balance encashed in final settlement.
Sick, Casual and Compensatory leave are NOT encashable.""",
    },
    {
        "source_document": "code_of_conduct.pdf",
        "collection": "general",
        "access_roles": ["doctor", "nurse", "billing_executive", "technician", "admin"],
        "section_title": "Professional Conduct, Patient Confidentiality & Social Media",
        "chunk_type": "text",
        "content": """Code of Conduct & Ethics Policy (COMP-COC-003 v5.2) — Applies to all staff and contractors

Professional Conduct:
Every MediAssist employee is expected to act with professionalism at all times: punctuality, respectful communication, respect for clinical and administrative hierarchy.
Zero tolerance for verbal or physical abuse directed at patients, visitors or colleagues. Substantiated abuse is treated as gross misconduct.

Patient Confidentiality:
- Patient records, diagnoses and treatment details must NEVER be disclosed outside authorised clinical and billing channels
- Staff are bound by HIPAA-equivalent obligations under the Indian IT Act
- Photographing patients, their records or charts on personal devices is STRICTLY PROHIBITED

Social Media Policy:
- No posting of patient images, case details or identifiable information on any platform
- No disparagement of MediAssist, colleagues, or competitor hospitals online
- Personal opinions must not be presented as the official position of MediAssist

Conflict of Interest:
- Staff must not refer patients to external facilities/labs/pharmacies in which they hold a financial interest
- Doctors must disclose any relationship with pharmaceutical companies (speaking fees, sponsorships, advisory roles) to Office of Compliance annually""",
    },
    {
        "source_document": "code_of_conduct.pdf",
        "collection": "general",
        "access_roles": ["doctor", "nurse", "billing_executive", "technician", "admin"],
        "section_title": "Gifts, POSH, Data & Disciplinary Process",
        "chunk_type": "text",
        "content": """Gifts & Gratuity:
- Gifts up to ₹500: permitted; use professional judgement
- Gifts above ₹500: must be declared to administration
- Gifts above ₹2,000: must be refused, or deposited with administration

Anti-Harassment Policy (POSH):
- POSH Committee constituted at each campus, chaired by a senior woman officer with an external member
- Complaints: posh@mediassist.in
- Investigations completed within 15-day internal timeline (statutory limit 90 days)
- Penalties range up to termination

Data & Systems:
- No unauthorised software on hospital devices
- No sharing of login credentials under any circumstances
- Suspected data breaches must be reported to IT Security within 2 hours of discovery

Disciplinary Process (graduated, proportionate to conduct):
1. Verbal warning (documented)
2. Written warning
3. Final written warning
4. Termination
Gross misconduct (patient harm, data theft, billing fraud, assault) may result in immediate termination.

Anti-Bribery: No employee may offer, solicit or accept any bribe, kickback or referral commission.
Whistleblower Protection: Report concerns to ethics@mediassist.in or anonymous ethics hotline. Good-faith reporters are protected.""",
    },
    {
        "source_document": "general_faqs.pdf",
        "collection": "general",
        "access_roles": ["doctor", "nurse", "billing_executive", "technician", "admin"],
        "section_title": "Payroll, Benefits & IT Systems FAQs",
        "chunk_type": "text",
        "content": """General Staff FAQs (HR-FAQ-004 v3.0)

Payroll & Benefits:
Q1. When is salary credited? Last working day of every month via NEFT.
Q2. How to access payslips? HR Portal → Payroll → My Payslips (last 36 months available).
Q3. PF contribution rate? 12% employee + 12% employer of basic salary; UAN on payslip.
Q4. How to update bank account? HR Portal → Profile → Bank Details; upload cancelled cheque. Takes effect next payroll cycle.
Q5. What health insurance is provided? Family floater ₹5,00,000/year under group policy with New India Assurance (self, spouse, two children).
Q6. Gratuity? Yes, after 5 years continuous service per Payment of Gratuity Act.

IT & Systems:
Q7. How to reset password? Self-service reset link on login page, or call IT Support at ext. 2200. Minimum 12 characters, rotated every 90 days.
Q8. Lost/stolen laptop? Report to IT Security (ithelp@mediassist.in) and supervisor. Device remotely locked and wiped; file police complaint.
Q9. New system access request? IT Service Desk portal with HOD approval. Provisioned within two working days.
Q10. Personal use of hospital Wi-Fi? Limited personal use of GUEST Wi-Fi permitted. Clinical network is strictly for work devices.
Q11. Clinical software issue during shift? Call 24×7 IT Support hotline at ext. 2200; clinical-system incidents are P1, responded within 15 minutes.""",
    },
    {
        "source_document": "general_faqs.pdf",
        "collection": "general",
        "access_roles": ["doctor", "nurse", "billing_executive", "technician", "admin"],
        "section_title": "HR, Facilities & Safety FAQs",
        "chunk_type": "text",
        "content": """Facilities FAQs:
Q12. Staff cafeteria? Lower ground floor of each campus; open 7:00 am – 11:00 pm, subsidised meals for all staff grades.
Q13. Crèche facility? Yes, at Hyderabad Central and Pune Speciality campuses; children 6 months to 6 years; available all shifts.
Q14. Conference room booking? Facilities → Room Booking on intranet; up to 30 days in advance.
Q15. Parking? Basement B1–B2 allocated by grade; two-wheeler parking at ground level; EV charging bays on B1.

HR & Administration FAQs:
Q16. How to apply for leave? All leave via HR Portal. See Leave & Attendance Policy for notice periods.
Q17. Who approves ICU doctor leave? ICU department HOD; leave >5 days additionally requires Medical Director's noting.
Q18. Experience letter/employment certificate? HR Portal → Letters; issued within five working days.
Q19. Notice period for resignation? 30 days for non-clinical staff; 60 days for clinical staff.
Q20. Internal transfer? Apply via Internal Job Posting board on HR Portal with HOD endorsement.
Q21. Annual appraisal? Runs each April on goal-based framework; mid-year check-in October.

Safety & Emergencies:
Q22. Fire evacuation? Stop work, help patients nearby, proceed to nearest fire exit and assembly point. Do not use lifts.
Q23. Medical emergency involving staff? Dial 7777 from any internal extension — Code Blue.
Q24. Patient fall? Do NOT move patient; call for clinical help immediately; nurse will assess and document.
Q25. Workplace safety hazard? Report via Facilities → Safety Report or to floor warden. Urgent hazards reported by phone immediately.""",
    },
    {
        "source_document": "staff_handbook.pdf",
        "collection": "general",
        "access_roles": ["doctor", "nurse", "billing_executive", "technician", "admin"],
        "section_title": "About MediAssist, Org Structure & Values",
        "chunk_type": "text",
        "content": """MediAssist Staff Handbook (HR-HBK-001 v6.0)

About MediAssist Health Network:
Founded in 2008 in Hyderabad. Operates 12 hospitals across Telangana, Karnataka and Maharashtra, supported by 40+ clinics and diagnostic centres.
Family of approximately 8,500 staff caring for over two million patient visits every year.
Head office: Hyderabad, Telangana.

Campuses:
- Hyderabad Central (Hyderabad, Telangana): Multi-speciality flagship with emergency services
- Secunderabad (Secunderabad, Telangana): Cardiac sciences and critical care
- Bengaluru Onco Centre (Bengaluru, Karnataka): Oncology and radiation therapy
- Pune Speciality (Pune, Maharashtra): Orthopaedics and mother-and-child care
- Mysuru Clinic Hub (Mysuru, Karnataka): Day-care, dialysis and outpatient services

Values: Patient First, Integrity, Clinical Excellence, Continuous Learning, Team Respect

Working Hours:
Administrative/billing/HR/IT: 9:00 am – 6:00 pm, Monday to Saturday
Clinical staff: 3 rotating shifts — Morning 7:00 am–3:00 pm, Afternoon 3:00–11:00 pm, Night 11:00 pm–7:00 am""",
    },
    {
        "source_document": "staff_handbook.pdf",
        "collection": "general",
        "access_roles": ["doctor", "nurse", "billing_executive", "technician", "admin"],
        "section_title": "Emergency Codes, Training & Key Contacts",
        "chunk_type": "text",
        "content": """Emergency Codes (all staff must memorise):
Code Blue — adult cardiac or respiratory arrest: Dial 7777; start BLS if trained
Code Pink — infant or child abduction: Secure exits and alert security
Code Red — fire: Raise alarm and evacuate via fire exits; NEVER use lifts
Code Orange — hazardous material spill: Cordon area; call facilities and safety
Code Grey — violent or aggressive person: Call security and ensure personal safety
Code Yellow — internal or external disaster (mass casualty): Report to muster point

Training & Professional Development:
Mandatory induction training within 30 days: BLS, infection control, fire safety, POSH
Clinical staff: Continuing Medical Education (CME) credits annually; study leave 5 days/yr
Technicians: Equipment-specific certification before independent operation of any biomedical device

Probation:
Clinical staff: 6 months probation
Non-clinical staff: 3 months probation
During probation notice period: 15 days (either party)

Key Contacts:
HR Helpdesk: 1800-180-4500 (toll-free) / hr.help@mediassist.in
IT Support: ithelp@mediassist.in / ext. 2200
Facilities Desk: facilities@mediassist.in / ext. 1100
Medical Director's Office: md.office@mediassist.in / ext. 1000
POSH Committee: posh@mediassist.in
Emergency (internal): dial 7777""",
    },
]

# Role → permitted collections mapping
ROLE_COLLECTIONS = {
    "doctor": ["clinical", "nursing", "general"],
    "nurse": ["nursing", "general"],
    "billing_executive": ["billing", "general"],
    "technician": ["equipment", "general"],
    "admin": ["clinical", "nursing", "billing", "equipment", "general"],
}

def get_accessible_docs(role: str) -> list[dict]:
    """Return all document chunks accessible to this role."""
    allowed = ROLE_COLLECTIONS.get(role, [])
    return [doc for doc in DOCUMENTS if doc["collection"] in allowed]

def get_role_collections(role: str) -> list[str]:
    return ROLE_COLLECTIONS.get(role, [])
