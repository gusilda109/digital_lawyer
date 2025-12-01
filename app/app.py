import streamlit as st
import sqlite3
from datetime import date
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent

BASE_DIR = Path(__file__).resolve().parent.parent  # /mnt/.../digital_attorney
DB_PATH = BASE_DIR / "db" / "app.sqlite"

@st.cache_resource
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

LOGO_PATH = APP_DIR / "logo_lawyer.png"

st.set_page_config(page_title="Цифровой правозащитник", page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else None)

EVIDENCE_SCHEMA = {
    "return_goods": {
        "claim": {  # Иск о возврате товара
            "required": [
                {"id": "purchase_doc", "label": "Документ о покупке товара (чек/квитанция/договор/заказ/выписка)"},
                {"id": "claim", "label": "Претензия о возврате товара и денег"},
                {"id": "claim_send_proof", "label": "Доказательство направления претензии продавцу"},
                {"id": "return_proof", "label": "Доказательство возврата товара продавцу"},
            ],
            "optional": [
                {"id": "photos_before", "label": "Фото/видео товара перед возвратом"},
                {"id": "chat_with_seller", "label": "Переписка с продавцом"},
                {"id": "seller_reply", "label": "Ответ продавца на претензию"},
                {"id": "delivery_cost_docs", "label": "Документы об оплате доставки"},
                {"id": "witnesses", "label": "Свидетельские показания"},
            ],
        },
    },

    "housing_utilities": {
        "claim": {  # Иск о компенсации/возмещении расходов за услуги ЖКХ
            "required": [
                {"id": "utility_contracts", "label": "Квитанции/счета/договоры на услуги ЖКХ"},
                {"id": "payment_docs", "label": "Платёжные документы (чеки/выписки)"},
                {"id": "ownership_or_rent", "label": "Договор собственности или найма жилого помещения"},
                {"id": "pretrial_claim", "label": "Претензия в адрес УК/поставщика"},
                {"id": "claim_send_proof", "label": "Подтверждение отправки претензии"},
                {"id": "compensation_calc", "label": "Расчёт суммы компенсации"},
            ],
            "optional": [
                {"id": "inspection_acts", "label": "Акты обследования/фиксации нарушений"},
                {"id": "issue_photos", "label": "Фото/видео неисправностей"},
                {"id": "chat_with_uk", "label": "Переписка с УК/поставщиком услуг"},
                {"id": "expert_reports", "label": "Заключения экспертов/техотчёты"},
                {"id": "witnesses", "label": "Показания свидетелей (соседей)"},
                {"id": "loss_docs", "label": "Документы о понесённых убытках"},
            ],
        },
        "motion": {  # Ходатайство по делу о ЖКХ
            "required": [
                {"id": "motion_text", "label": "Само ходатайство с обоснованием"},
                {"id": "motion_support_docs", "label": "Документы, подтверждающие необходимость экспертизы/проверки/истребования"},
                {"id": "motion_copy_proof", "label": "Подтверждение направления копии другой стороне"},
            ],
            "optional": [
                {"id": "motion_acts_photos", "label": "Акты и фото, на которые ссылается заявитель"},
                {"id": "uk_replies", "label": "Ответы или отказы от УК / РСО"},
                {"id": "collective_claims", "label": "Коллективные обращения жильцов"},
                {"id": "independent_expert", "label": "Заключение независимого специалиста"},
            ],
        },
        "objection": {  # Возражение на иск по делу о ЖКХ
            "required": [
                {"id": "utility_contract", "label": "Договор на оказание ЖКХ-услуг"},
                {"id": "billing_calc", "label": "Расчёты начислений и оплаты"},
                {"id": "acts_done", "label": "Акты выполненных работ"},
                {"id": "claim_answers", "label": "Ответы на претензии"},
                {"id": "finance_docs", "label": "Финансовые документы (выписки, счета)"},
            ],
            "optional": [
                {"id": "emergency_logs", "label": "Журналы аварийных выездов, отчёты диспетчерской"},
                {"id": "network_photos", "label": "Фотофиксация состояния сетей"},
                {"id": "service_quality_exam", "label": "Экспертиза качества услуг"},
                {"id": "uk_staff_witnesses", "label": "Показания сотрудников УК"},
                {"id": "internal_docs", "label": "Переписка и внутренние акты реагирования"},
            ],
        },
    },

    "minor_injury": {
        "claim": {  # Иск о возмещении лёгкого вреда здоровью
            "required": [
                {"id": "med_docs", "label": "Медицинские документы (справки/выписки/диагноз)"},
                {"id": "er_certificate", "label": "Справка из травмпункта/больницы"},
                {"id": "causality_proof", "label": "Доказательства причинной связи (акт/фото/свидетели)"},
                {"id": "treatment_payments", "label": "Чеки/квитанции на лечение/лекарства/транспорт"},
                {"id": "pretrial_claim", "label": "Претензия или досудебное обращение (при наличии)"},
                {"id": "passport", "label": "Документ о личности истца (паспорт)"},
            ],
            "optional": [
                {"id": "incident_act", "label": "Акт о несчастном случае/происшествии"},
                {"id": "incident_media", "label": "Фото/видео с места происшествия"},
                {"id": "witnesses", "label": "Свидетельские показания"},
                {"id": "forensic_exam", "label": "Судебно-медицинская экспертиза"},
                {"id": "chat_with_insurer", "label": "Переписка с ответчиком/страховой"},
                {"id": "sick_leave", "label": "Больничный лист"},
                {"id": "income_before", "label": "Справка о доходах до травмы"},
                {"id": "psych_report", "label": "Психологическое заключение"},
            ],
        },
        "motion": {  # Ходатайство по делу о вреде здоровью
            "required": [
                {"id": "motion_text", "label": "Само ходатайство с обоснованием"},
                {"id": "motion_support_docs", "label": "Документы, подтверждающие необходимость экспертизы или вызова свидетелей"},
                {"id": "motion_copy_proof", "label": "Подтверждение направления копии другой стороне"},
            ],
            "optional": [
                {"id": "med_extracts", "label": "Медицинские выписки, подтверждающие необходимость экспертизы"},
                {"id": "incident_scheme", "label": "Акт происшествия, схема места события"},
                {"id": "org_answers", "label": "Ответы органов/организаций (например, отказ выдать акт)"},
                {"id": "witness_claims", "label": "Свидетельские показания, коллективные обращения"},
            ],
        },
        "objection": {  # Возражение на иск по вреду здоровью
            "required": [
                {"id": "no_causality_acts", "label": "Акты проверок об отсутствии причинной связи"},
                {"id": "good_faith_docs", "label": "Доказательства добросовестности ответчика (меры безопасности и т.п.)"},
                {"id": "other_med_docs", "label": "Медицинские документы об иных причинах травмы"},
                {"id": "plaintiff_notifications", "label": "Переписка или уведомления истца"},
                {"id": "defendant_witnesses", "label": "Свидетельские показания в пользу ответчика"},
            ],
            "optional": [
                {"id": "place_inspection_acts", "label": "Акты осмотра места происшествия"},
                {"id": "good_state_media", "label": "Фото/видео, подтверждающие исправное состояние"},
                {"id": "independent_expert", "label": "Заключение независимого эксперта"},
                {"id": "training_docs", "label": "Документы о проведении инструктажей и предупреждений"},
                {"id": "internal_check_protocols", "label": "Протоколы внутренней проверки, служебные записки"},
            ],
        },
    },
}



if LOGO_PATH.exists():
    st.image(str(LOGO_PATH))
else:
    st.warning(f"Логотип не найден: {LOGO_PATH}. Поместите файл сюда или поменяйте путь.")

st.header("Анкета дела — общие данные")


courts = [
    {"id": 1, "name": "Мировой судья участка №1, г. Москва", "address": "ул. Примерная, 1"},
    {"id": 2, "name": "Районный суд Центрального района, г. Самара", "address": "пр. Судебный, 10"},
    {"id": 3, "name": "Ленинский районный суд, г. Казань", "address": "ул. Правовая, 5"},
]
court_labels = [c["name"] for c in courts]

CATEGORY_LABELS = {
    "Возврат товара": "return_goods",
    "Компенсация услуг ЖКХ": "housing_utilities",
    "Мелкий вред здоровью": "minor_injury",
}

DOC_TYPE_LABELS = {
    "return_goods": {
        "Иск о возврате товара": "claim",
    },
    "housing_utilities": {
        "Иск о компенсации за услуги ЖКХ": "claim",
        "Ходатайство по делу о ЖКХ": "motion",
        "Возражение на иск по делу о ЖКХ": "objection",
    },
    "minor_injury": {
        "Иск о возмещении вреда здоровью (лёгкий вред)": "claim",
        "Ходатайство по делу о вреде здоровью": "motion",
        "Возражение на иск по вреду здоровью": "objection",
    },
}


st.subheader("Выбор категории спора")

CATEGORY_LABELS = {
    "Возврат товара": "return_goods",
    "Компенсация услуг ЖКХ": "housing_utilities",
    "Мелкий вред здоровью": "minor_injury",
}

category_label = st.selectbox(
    "Категория спора *",
    ["— Выберите категорию —"] + list(CATEGORY_LABELS.keys()),
    key="category_label",
)

internal_cat = CATEGORY_LABELS.get(category_label) if category_label in CATEGORY_LABELS else None

doc_label = None
internal_doc_type = None

if internal_cat:
    st.subheader("Тип документа")
    doc_options = list(DOC_TYPE_LABELS[internal_cat].keys())
    doc_label = st.selectbox(
        "Тип документа *",
        ["— Выберите тип документа —"] + doc_options,
        key="doc_label",
    )
    if doc_label in DOC_TYPE_LABELS[internal_cat]:
        internal_doc_type = DOC_TYPE_LABELS[internal_cat][doc_label]

# Показать список доказательств только если выбраны и категория, и тип документа
if internal_cat and internal_doc_type:
    schema = EVIDENCE_SCHEMA.get(internal_cat, {}).get(internal_doc_type, {})
    st.subheader("Доказательства по выбранному документу")

    if schema.get("required"):
        st.markdown("**Необходимые доказательства**")
        for item in schema["required"]:
            st.checkbox(
                item["label"],
                key=f"ev_{internal_cat}_{internal_doc_type}_{item['id']}",
            )
            st.file_uploader(
                "Файл (опционально)",
                key=f"file_{internal_cat}_{internal_doc_type}_{item['id']}",
                label_visibility="collapsed",
            )
            st.divider()

    if schema.get("optional"):
        st.markdown("**Желательные доказательства**")
        for item in schema["optional"]:
            st.checkbox(
                item["label"],
                key=f"ev_{internal_cat}_{internal_doc_type}_{item['id']}",
            )
            st.file_uploader(
                "Файл (опционально)",
                key=f"file_{internal_cat}_{internal_doc_type}_{item['id']}",
                label_visibility="collapsed",
            )
            st.divider()

def save_case(users_payload: dict, cases_payload: dict) -> int:
    conn = get_conn()
    cur = conn.cursor()

    # Users
    cur.execute(
        """
        INSERT INTO Users (fio, email, phone,
                           resident_region, resident_city, resident_address)
        VALUES (:fio, :email, :phone,
                :resident_region, :resident_city, :resident_address)
        """,
        users_payload,
    )
    user_id = cur.lastrowid

    # Привязываем дело к пользователю
    cases_payload = dict(cases_payload)  # на всякий случай копия
    cases_payload["user_id"] = user_id

    cur.execute(
        """
        INSERT INTO Cases (user_id, court_id, category, description,
                           opponent_name, opponent_address,
                           amount, event_date, status,
                           court_name_override, court_address_override)
        VALUES (:user_id, :court_id, :category, :description,
                :opponent_name, :opponent_address,
                :amount, :event_date, :status,
                :court_name_override, :court_address_override)
        """,
        cases_payload,
    )
    case_id = cur.lastrowid
    conn.commit()
    return case_id


with st.form("case_form"):
    st.subheader("Данные истца")
    fio = st.text_input("ФИО истца *", placeholder="Иванов Иван Иванович", key="fio")
    col1, col2, col3 = st.columns(3)
    with col1:
        region = st.text_input("Регион истца *", placeholder="Московская область", key="region")
    with col2:
        city = st.text_input("Город истца *", placeholder="Москва", key="city")
    with col3:
        address = st.text_input("Адрес истца *", placeholder="ул. Пушкина, д. 10, кв. 5", key="address")

    colc1, colc2 = st.columns(2)
    with colc1:
        email = st.text_input("Email (опц.)", placeholder="name@example.com", key="email")
    with colc2:
        phone = st.text_input("Телефон (опц.)", placeholder="+7 900 000-00-00", key="phone")

    st.subheader("Суд")
    court_idx = st.selectbox("Суд *", options=range(len(court_labels)), format_func=lambda i: court_labels[i], key="court_idx")
    override = st.checkbox("Переопределить название/адрес суда вручную?")
    court_name_override = ""
    court_address_override = ""
    if override:
        court_name_override = st.text_input("Название суда (ручной ввод)", key="court_name_override")
        court_address_override = st.text_input("Адрес суда (ручной ввод)", key="court_address_override")

    st.subheader("Ответчик")
    opponent_name = st.text_input("Ответчик: наименование *", key="opponent_name", placeholder="ООО «Ромашка» / Петров П.П.")
    opponent_address = st.text_input("Ответчик: адрес (желательно)", key="opponent_address", placeholder="г. Москва, ...")

    st.subheader("Детали спора")
    amount = st.number_input("Сумма требований (руб.) *", min_value=0, step=100, key="amount")
    event_date = st.date_input("Дата события *", value=date.today(), key="event_date")
    description = st.text_area(
        "Описание ситуации (3–6 предложений) *",
        height=150,
        placeholder="Кратко опишите, что произошло...",
        key="description",
    )

    

    # Показать список доказательств по выбранной категории
    



    submitted = st.form_submit_button("Сохранить черновик")



    if submitted:
        errors = {}

        if not fio.strip():
            errors["fio"] = "Укажите ФИО истца."
        if not region.strip():
            errors["region"] = "Укажите регион истца."
        if not city.strip():
            errors["city"] = "Укажите город истца."
        if not address.strip():
            errors["address"] = "Укажите адрес истца."

        if court_idx is None or court_idx < 0 or court_idx >= len(courts):
            errors["court_idx"] = "Выберите суд из справочника."

        if not opponent_name.strip():
            errors["opponent_name"] = "Укажите наименование ответчика."

        if amount is None or amount <= 0:
            errors["amount"] = "Сумма требований должна быть больше 0."

        if event_date is None:
            errors["event_date"] = "Укажите дату события."
        elif event_date > date.today():
            errors["event_date"] = "Дата события не может быть в будущем."

        if not description.strip():
            errors["description"] = "Опишите ситуацию (минимум 1–2 предложения)."
        
        if category_label == "— Выберите категорию —":
            errors["category"] = "Выберите категорию спора."

        

        category_label = st.session_state.get("category_label")
        doc_label = st.session_state.get("doc_label")

        # Категория и тип документа обязательны
        if not category_label or category_label == "— Выберите категорию —":
            errors["category"] = "Выберите категорию спора."

        internal_cat = CATEGORY_LABELS.get(category_label) if category_label in CATEGORY_LABELS else None
        internal_doc_type = None

        if internal_cat:
            if not doc_label or doc_label == "— Выберите тип документа —":
                errors["doc_type"] = "Выберите тип документа."
            else:
                internal_doc_type = DOC_TYPE_LABELS[internal_cat].get(doc_label)

        # Обязательные доказательства: должна стоять галочка
        if internal_cat and internal_doc_type:
            schema = EVIDENCE_SCHEMA.get(internal_cat, {}).get(internal_doc_type, {})
            for item in schema.get("required", []):
                if not st.session_state.get(f"ev_{internal_cat}_{internal_doc_type}_{item['id']}"):
                    errors[f"ev_required_{item['id']}"] = (
                        f"Обязательное доказательство не отмечено: «{item['label']}»."
                    )



        if errors:
            st.error("Пожалуйста, исправьте ошибки в форме.")

            if "category" in errors: st.caption(f"❌ {errors['category']}")
            if "fio" in errors: st.caption(f"❌ {errors['fio']}")
            if "region" in errors: st.caption(f"❌ {errors['region']}")
            if "city" in errors: st.caption(f"❌ {errors['city']}")
            if "address" in errors: st.caption(f"❌ {errors['address']}")
            if "court_idx" in errors: st.caption(f"❌ {errors['court_idx']}")
            if "opponent_name" in errors: st.caption(f"❌ {errors['opponent_name']}")
            if "amount" in errors: st.caption(f"❌ {errors['amount']}")
            if "event_date" in errors: st.caption(f"❌ {errors['event_date']}")
            if "description" in errors: st.caption(f"❌ {errors['description']}")
            if "category" in errors:
                st.caption(f"❌ {errors['category']}")
            if "doc_type" in errors:
                st.caption(f"❌ {errors['doc_type']}")

            for k, v in errors.items():
                if k.startswith("ev_required_"):
                    st.caption(f"❌ {v}")


    
        else:
            
            

            selected_court = courts[court_idx]

            # Users
            users_payload = {
                "fio": fio.strip(),
                "resident_region": region.strip(),
                "resident_city": city.strip(),
                "resident_address": address.strip(),
                "email": (email or "").strip() or None,
                "phone": (phone or "").strip() or None,
            }

            # internal_cat и internal_doc_type мы уже посчитали выше в этом же if submitted
            # (из category_label и doc_label)
            cases_payload = {
                "court_id": None,
                "court_name_override": (court_name_override or "").strip() or None,
                "court_address_override": (court_address_override or "").strip() or None,
                "opponent_name": opponent_name.strip(),
                "opponent_address": (opponent_address or "").strip() or None,
                "amount": float(amount),
                "event_date": event_date.isoformat(),
                "description": description.strip(),
                "status": "draft",
                "category": internal_cat,          # 'return_goods' / 'housing_utilities' / 'minor_injury'
            }
            case_id = save_case(users_payload, cases_payload)
            st.success(f"Черновик сохранён в базе данных (дело ID = {case_id}).")


