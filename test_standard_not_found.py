"""
Тест: проверка поиска несуществующего стандарта
"""
import streamlit as st
from data_loader import load_laboratories

st.set_page_config(page_title="Тест поиска стандарта", layout="wide")
st.title("🐞 Тест: поиск несуществующего стандарта")

# Загружаем данные
if 'labs_data' not in st.session_state:
    with st.spinner('Загрузка данных...'):
        st.session_state.labs_data = load_laboratories()
        st.session_state.current_lab = list(st.session_state.labs_data.keys())[0]

lab = st.session_state.labs_data[st.session_state.current_lab]
st.markdown(f"### Лаборатория: {st.session_state.current_lab}")

# Поля ввода
standard_input = st.text_input("Введите стандарт", value="99999")

if st.button("🔍 Искать"):
    std_lower = standard_input.strip().lower()

    st.markdown("---")
    st.markdown("### 🐞 Результаты поиска")
    st.write(f"**Ищем стандарт:** '{standard_input}'")

    found_any = False
    found_sections = []

    for section in lab.sections:
        for s in section.standards:
            if std_lower in s.lower():
                found_any = True
                found_sections.append((section.full_id, s))
                break

    st.write(f"**Всего разделов в лаборатории:** {len(lab.sections)}")
    st.write(f"**Найдено разделов с этим стандартом:** {len(found_sections)}")

    if found_sections:
        st.success("✅ Стандарт найден в следующих разделах:")
        for sec, std_name in found_sections[:10]:
            st.write(f"  - {sec}: {std_name}")
    else:
        st.warning(f"❌ Стандарт '{standard_input}' не найден в области аккредитации")