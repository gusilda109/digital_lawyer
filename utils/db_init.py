# utils/db_init.py
from __future__ import annotations
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DB_DIR = ROOT / "db"
DB_PATH = DB_DIR / "app.sqlite"

DDL = r"""
PRAGMA foreign_keys = ON;

-- =========================
-- Пользователи
-- =========================
CREATE TABLE IF NOT EXISTS Users (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  fio               TEXT,
  email             TEXT,
  phone             TEXT,
  resident_region   TEXT,
  resident_city     TEXT,
  resident_address  TEXT,
  preferred_court_id INTEGER,  -- FK -> Courts.id (опц.)
  FOREIGN KEY(preferred_court_id) REFERENCES Courts(id)
    ON UPDATE CASCADE ON DELETE SET NULL
);

-- =========================
-- Суды
-- =========================
CREATE TABLE IF NOT EXISTS Courts (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  name             TEXT,     -- офиц. наименование суда
  court_level      TEXT,     -- "мировой" | "районный" | ...
  region           TEXT,     -- субъект РФ
  city             TEXT,
  address          TEXT,
  jurisdiction_notes TEXT
);

-- =========================
-- Дела
-- =========================
CREATE TABLE IF NOT EXISTS Cases (
  id                 INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id            INTEGER,  -- FK -> Users.id
  court_id           INTEGER,  -- FK -> Courts.id (может быть NULL)
  category           TEXT,     -- 'return_goods' | 'housing_utilities' | 'minor_injury'
  description        TEXT,
  opponent_name      TEXT,
  opponent_address   TEXT,
  amount             REAL,
  event_date         TEXT,     -- ISO 8601
  p_success          REAL,     -- 0..1
  status             TEXT,     -- draft|analysis|docs_ready|scheduled
  created_at         TEXT DEFAULT (datetime('now')),
  updated_at         TEXT,

  court_name_override   TEXT,
  court_address_override TEXT,

  -- I. Возврат товара (ЗоЗПП)
  rg_has_purchase_doc         INTEGER CHECK (rg_has_purchase_doc IN (0,1) OR rg_has_purchase_doc IS NULL),
  rg_has_claim_letter         INTEGER CHECK (rg_has_claim_letter IN (0,1) OR rg_has_claim_letter IS NULL),
  rg_has_claim_send_proof     INTEGER CHECK (rg_has_claim_send_proof IN (0,1) OR rg_has_claim_send_proof IS NULL),
  rg_has_goods_return_proof   INTEGER CHECK (rg_has_goods_return_proof IN (0,1) OR rg_has_goods_return_proof IS NULL),
  rg_opt_media_product        INTEGER CHECK (rg_opt_media_product IN (0,1) OR rg_opt_media_product IS NULL),
  rg_opt_chat_with_seller     INTEGER CHECK (rg_opt_chat_with_seller IN (0,1) OR rg_opt_chat_with_seller IS NULL),
  rg_opt_seller_response      INTEGER CHECK (rg_opt_seller_response IN (0,1) OR rg_opt_seller_response IS NULL),
  rg_opt_delivery_expenses_docs INTEGER CHECK (rg_opt_delivery_expenses_docs IN (0,1) OR rg_opt_delivery_expenses_docs IS NULL),
  rg_opt_witnesses            INTEGER CHECK (rg_opt_witnesses IN (0,1) OR rg_opt_witnesses IS NULL),

  -- II. ЖКХ
  hu_has_bills_contracts      INTEGER CHECK (hu_has_bills_contracts IN (0,1) OR hu_has_bills_contracts IS NULL),
  hu_has_payment_docs         INTEGER CHECK (hu_has_payment_docs IN (0,1) OR hu_has_payment_docs IS NULL),
  hu_has_property_contract    INTEGER CHECK (hu_has_property_contract IN (0,1) OR hu_has_property_contract IS NULL),
  hu_has_claim_to_uk          INTEGER CHECK (hu_has_claim_to_uk IN (0,1) OR hu_has_claim_to_uk IS NULL),
  hu_has_claim_send_proof     INTEGER CHECK (hu_has_claim_send_proof IN (0,1) OR hu_has_claim_send_proof IS NULL),
  hu_has_compensation_calc    INTEGER CHECK (hu_has_compensation_calc IN (0,1) OR hu_has_compensation_calc IS NULL),
  hu_opt_inspection_acts      INTEGER CHECK (hu_opt_inspection_acts IN (0,1) OR hu_opt_inspection_acts IS NULL),
  hu_opt_issue_photos         INTEGER CHECK (hu_opt_issue_photos IN (0,1) OR hu_opt_issue_photos IS NULL),
  hu_opt_chat_with_uk         INTEGER CHECK (hu_opt_chat_with_uk IN (0,1) OR hu_opt_chat_with_uk IS NULL),
  hu_opt_expert_reports       INTEGER CHECK (hu_opt_expert_reports IN (0,1) OR hu_opt_expert_reports IS NULL),
  hu_opt_neighbor_witnesses   INTEGER CHECK (hu_opt_neighbor_witnesses IN (0,1) OR hu_opt_neighbor_witnesses IS NULL),
  hu_opt_damage_expense_docs  INTEGER CHECK (hu_opt_damage_expense_docs IN (0,1) OR hu_opt_damage_expense_docs IS NULL),

  hu_mo_has_motion_body       INTEGER CHECK (hu_mo_has_motion_body IN (0,1) OR hu_mo_has_motion_body IS NULL),
  hu_mo_has_support_docs      INTEGER CHECK (hu_mo_has_support_docs IN (0,1) OR hu_mo_has_support_docs IS NULL),
  hu_mo_has_copy_proof        INTEGER CHECK (hu_mo_has_copy_proof IN (0,1) OR hu_mo_has_copy_proof IS NULL),
  hu_ob_has_service_contract  INTEGER CHECK (hu_ob_has_service_contract IN (0,1) OR hu_ob_has_service_contract IS NULL),
  hu_ob_has_charge_calc       INTEGER CHECK (hu_ob_has_charge_calc IN (0,1) OR hu_ob_has_charge_calc IS NULL),
  hu_ob_has_work_acts         INTEGER CHECK (hu_ob_has_work_acts IN (0,1) OR hu_ob_has_work_acts IS NULL),
  hu_ob_has_claim_answers     INTEGER CHECK (hu_ob_has_claim_answers IN (0,1) OR hu_ob_has_claim_answers IS NULL),
  hu_ob_has_financial_docs    INTEGER CHECK (hu_ob_has_financial_docs IN (0,1) OR hu_ob_has_financial_docs IS NULL),

  -- III. Лёгкий вред здоровью
  mi_has_med_docs             INTEGER CHECK (mi_has_med_docs IN (0,1) OR mi_has_med_docs IS NULL),
  mi_has_trauma_cert          INTEGER CHECK (mi_has_trauma_cert IN (0,1) OR mi_has_trauma_cert IS NULL),
  mi_has_causality_proof      INTEGER CHECK (mi_has_causality_proof IN (0,1) OR mi_has_causality_proof IS NULL),
  mi_has_treatment_receipts   INTEGER CHECK (mi_has_treatment_receipts IN (0,1) OR mi_has_treatment_receipts IS NULL),
  mi_has_preclaim             INTEGER CHECK (mi_has_preclaim IN (0,1) OR mi_has_preclaim IS NULL),
  mi_has_identity_doc         INTEGER CHECK (mi_has_identity_doc IN (0,1) OR mi_has_identity_doc IS NULL),
  mi_opt_accident_act         INTEGER CHECK (mi_opt_accident_act IN (0,1) OR mi_opt_accident_act IS NULL),
  mi_opt_scene_media          INTEGER CHECK (mi_opt_scene_media IN (0,1) OR mi_opt_scene_media IS NULL),
  mi_opt_witnesses            INTEGER CHECK (mi_opt_witnesses IN (0,1) OR mi_opt_witnesses IS NULL),
  mi_opt_forensic_exam        INTEGER CHECK (mi_opt_forensic_exam IN (0,1) OR mi_opt_forensic_exam IS NULL),
  mi_opt_defendant_corresp    INTEGER CHECK (mi_opt_defendant_corresp IN (0,1) OR mi_opt_defendant_corresp IS NULL),
  mi_opt_sick_leave           INTEGER CHECK (mi_opt_sick_leave IN (0,1) OR mi_opt_sick_leave IS NULL),
  mi_opt_income_statement     INTEGER CHECK (mi_opt_income_statement IN (0,1) OR mi_opt_income_statement IS NULL),
  mi_opt_psych_report         INTEGER CHECK (mi_opt_psych_report IN (0,1) OR mi_opt_psych_report IS NULL),

  mi_mo_has_motion_body       INTEGER CHECK (mi_mo_has_motion_body IN (0,1) OR mi_mo_has_motion_body IS NULL),
  mi_mo_has_support_docs      INTEGER CHECK (mi_mo_has_support_docs IN (0,1) OR mi_mo_has_support_docs IS NULL),
  mi_mo_has_copy_proof        INTEGER CHECK (mi_mo_has_copy_proof IN (0,1) OR mi_mo_has_copy_proof IS NULL),
  mi_ob_has_no_causality_docs INTEGER CHECK (mi_ob_has_no_causality_docs IN (0,1) OR mi_ob_has_no_causality_docs IS NULL),
  mi_ob_has_due_care_docs     INTEGER CHECK (mi_ob_has_due_care_docs IN (0,1) OR mi_ob_has_due_care_docs IS NULL),
  mi_ob_has_alt_cause_med     INTEGER CHECK (mi_ob_has_alt_cause_med IN (0,1) OR mi_ob_has_alt_cause_med IS NULL),
  mi_ob_has_claim_notices     INTEGER CHECK (mi_ob_has_claim_notices IN (0,1) OR mi_ob_has_claim_notices IS NULL),
  mi_ob_has_support_witnesses INTEGER CHECK (mi_ob_has_support_witnesses IN (0,1) OR mi_ob_has_support_witnesses IS NULL),

  FOREIGN KEY(user_id)  REFERENCES Users(id)  ON UPDATE CASCADE ON DELETE SET NULL,
  FOREIGN KEY(court_id) REFERENCES Courts(id) ON UPDATE CASCADE ON DELETE SET NULL,
  CHECK (p_success IS NULL OR (p_success >= 0.0 AND p_success <= 1.0)),
  CHECK (category IS NULL OR category IN ('return_goods','housing_utilities','minor_injury')),
  CHECK (status   IS NULL OR status   IN ('draft','analysis','docs_ready','scheduled'))
);

CREATE INDEX IF NOT EXISTS idx_cases_user     ON Cases(user_id);
CREATE INDEX IF NOT EXISTS idx_cases_court    ON Cases(court_id);
CREATE INDEX IF NOT EXISTS idx_cases_category ON Cases(category);
CREATE INDEX IF NOT EXISTS idx_cases_status   ON Cases(status);

-- =========================
-- Документы
-- =========================
CREATE TABLE IF NOT EXISTS Documents (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  case_id      INTEGER NOT NULL,
  doc_type     TEXT,          -- 'pretension' | 'claim' | 'objection' | 'motion'
  template_name TEXT,
  file_path    TEXT,
  mime_type    TEXT,
  file_size    INTEGER,
  kb_articles  TEXT,          -- JSON/CSV
  created_at   TEXT DEFAULT (datetime('now')),
  FOREIGN KEY(case_id) REFERENCES Cases(id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_docs_case_id ON Documents(case_id);
CREATE INDEX IF NOT EXISTS idx_docs_type    ON Documents(doc_type);

-- =========================
-- Сроки/этапы (Календарь)
-- =========================
CREATE TABLE IF NOT EXISTS Deadlines (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  case_id    INTEGER NOT NULL,
  title      TEXT,
  due_date   TEXT,        -- ISO 8601
  status     TEXT,        -- 'planned' | 'done' | 'overdue'
  source     TEXT,        -- kb.timeline.*
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT,
  FOREIGN KEY(case_id) REFERENCES Cases(id) ON UPDATE CASCADE ON DELETE CASCADE,
  CHECK (status IS NULL OR status IN ('planned','done','overdue'))
);
CREATE INDEX IF NOT EXISTS idx_dead_case_due ON Deadlines(case_id, due_date);
"""

def main() -> None:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.executescript(DDL)
    print(f"{DB_PATH}")

if __name__ == "__main__":
    main()
