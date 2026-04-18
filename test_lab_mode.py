import streamlit as st

labs = ["ИЛ ЦТС", "ИЛ ТЕХЭКСПЕРТ"]

if "current_lab" not in st.session_state:
    st.session_state.current_lab = labs[0]
if "search_mode" not in st.session_state:
    st.session_state.search_mode = "Поиск по стандартам"


def set_mode():
    st.session_state.search_mode = st.session_state.mode_selector


with st.sidebar:
    selected_lab = st.radio("Лаборатория", labs, index=labs.index(st.session_state.current_lab), key="lab_selector")
    if selected_lab != st.session_state.current_lab:
        st.session_state.current_lab = selected_lab
        st.rerun()

    st.divider()
    st.radio("Режим", ["Поиск по стандартам", "Поиск по показателям"],
             index=0 if st.session_state.search_mode == "Поиск по стандартам" else 1,
             key="mode_selector",
             on_change=set_mode)

st.write(f"Лаборатория: {st.session_state.current_lab}")
st.write(f"Режим: {st.session_state.search_mode}")

if st.session_state.search_mode == "Поиск по показателям":
    st.text_input("Показатель")
else:
    st.text_input("Стандарт")