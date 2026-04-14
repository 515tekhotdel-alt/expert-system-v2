import streamlit as st
from st_keyup import st_keyup  # Импортируем новый компонент [citation:1]
from data_loader import load_laboratories

st.set_page_config(page_title="Тест streamlit-keyup", layout="wide")
st.title("🧪 Тест живых автоподсказок с streamlit-keyup")

# Загружаем данные
if 'labs_data' not in st.session_state:
    with st.spinner('Загрузка данных лабораторий...'):
        st.session_state.labs_data = load_laboratories()
        st.session_state.current_lab = list(st.session_state.labs_data.keys())[0]

lab = st.session_state.labs_data[st.session_state.current_lab]
all_products = lab.get_all_products()

st.markdown(f"### Лаборатория: {st.session_state.current_lab}")
st.markdown(f"*Всего продукции в области: {len(all_products)}*")

# Используем st_keyup для "живого" ввода [citation:1]
product_input = st_keyup(
    "📦 Введите часть названия продукции",
    placeholder="например: белье",
    key="product_test_keyup"
)

# Подсказки в реальном времени
if product_input and len(product_input) >= 2:
    suggestions = [p for p in all_products if product_input.lower() in p.lower()]
    if suggestions:
        st.markdown(f"**📋 Найдено в области ({len(suggestions)}):**")
        suggestions_text = ""
        for s in suggestions[:20]:
            suggestions_text += f"• {s}\n"
        if len(suggestions) > 20:
            suggestions_text += f"... и еще {len(suggestions)-20}"
        st.text(suggestions_text)
    else:
        st.warning("❌ Ничего не найдено")
elif product_input and len(product_input) < 2:
    st.caption("Введите минимум 2 символа")

st.write(f"DEBUG: текущий запрос = '{product_input}'")