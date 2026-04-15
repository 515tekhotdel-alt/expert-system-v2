"""
Тест для отладки Таблицы 3 (поиск стандартов).
"""
import streamlit as st
from data_loader import load_laboratories

st.set_page_config(page_title="Тест Таблицы 3", layout="wide")
st.title("🐞 Тест: поиск стандартов в Таблице 3")

# Загружаем данные
if 'labs_data' not in st.session_state:
    with st.spinner('Загрузка данных...'):
        st.session_state.labs_data = load_laboratories()
        st.session_state.current_lab = list(st.session_state.labs_data.keys())[0]

lab = st.session_state.labs_data[st.session_state.current_lab]
st.markdown(f"### Лаборатория: {st.session_state.current_lab}")

# Поля ввода
product_input = st.text_input("Продукция", value="белье")
tnved_input = st.text_input("ТН ВЭД (через запятую)", value="6115, 6116")
standard_input = st.text_input("Стандарт", value="22648")

if st.button("🔍 Найти"):
    # Парсим ввод
    tnved_list = [t.strip() for t in tnved_input.replace(';', ',').split(',') if t.strip()]
    std_lower = standard_input.strip().lower()

    st.markdown("---")
    st.markdown("### 🐞 Результаты поиска")
    st.write(f"**Ищем стандарт:** '{standard_input}'")
    st.write(f"**ТН ВЭД:** {tnved_list}")

    # Сначала ищем разделы по продукции (упрощённо)
    product_sections = set()
    for section in lab.sections:
        for prod in section.products:
            if product_input.lower() in prod.lower():
                product_sections.add(section.full_id)

    st.write(f"**Разделов по продукции '{product_input}':** {len(product_sections)}")

    # Теперь ищем стандарт по всем разделам
    st.markdown("---")
    st.markdown("### Поиск стандарта по ВСЕМ разделам:")

    found_in_lab = []
    for section in lab.sections:
        for s in section.standards:
            if std_lower in s.lower():
                found_in_lab.append((section.full_id, s))
                break

    st.write(f"**Всего разделов с этим стандартом в лаборатории:** {len(found_in_lab)}")
    for sec, std_name in found_in_lab[:10]:
        st.write(f"  - {sec}: {std_name}")
    if len(found_in_lab) > 10:
        st.write(f"  ... и ещё {len(found_in_lab) - 10}")

    st.markdown("---")
    st.markdown("### Проверка для каждой пары (стандарт + ТН ВЭД):")

    for code in tnved_list:
        st.markdown(f"**ТН ВЭД: {code}**")
        found_for_code = []

        for section in lab.sections:
            # Проверяем стандарт
            std_found = False
            full_std_name = standard_input
            for s in section.standards:
                if std_lower in s.lower():
                    full_std_name = s
                    std_found = True
                    break

            if not std_found:
                continue

            # Проверяем ТН ВЭД
            tnved_found = False
            for tn in section.tnved_codes:
                if code in tn:
                    tnved_found = True
                    break

            if not tnved_found:
                continue

            # Проверяем продукцию
            in_product = section.full_id in product_sections

            found_for_code.append({
                'section': section.full_id,
                'standard': full_std_name,
                'in_product': in_product
            })

        st.write(f"Найдено разделов: {len(found_for_code)}")
        for item in found_for_code:
            status = "✅ в продукции" if item['in_product'] else "❌ НЕ в продукции"
            st.write(f"  - {item['section']}: {item['standard']} {status}")

    st.markdown("---")
    st.success("Готово")