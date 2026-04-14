import streamlit as st

def clear_form():
    st.session_state.field_text = ""

def set_test_data():
    st.session_state.field_text = "тестовые данные"

if 'field_text' not in st.session_state:
    st.session_state.field_text = ''

with st.form(key="test_form"):
    user_input = st.text_input("Введите текст", value=st.session_state.field_text)
    
    col1, col2 = st.columns(2)
    with col1:
        clear_btn = st.form_submit_button("Очистить", on_click=clear_form)
    with col2:
        test_btn = st.form_submit_button("Тест", on_click=set_test_data)

# После ЛЮБОЙ кнопки формы сохраняем значение
if clear_btn or test_btn:
    st.session_state.field_text = user_input
    st.rerun()

st.write(f"Текущее значение: '{st.session_state.field_text}'")