"""Боковая панель (выбор лаборатории, статистика)."""
import streamlit as st
from typing import Dict
from models import Laboratory


def render_sidebar(labs_data: Dict[str, Laboratory], current_lab: str):
    with st.sidebar:
        st.header("🔬 Лаборатория")

        lab_options = list(labs_data.keys())

        # Красивые названия с иконками
        lab_display = []
        for lab in lab_options:
            if lab == "ИЛ ЦТС":
                lab_display.append("🧬 ИЛ ЦТС")
            else:
                lab_display.append("🧪 ИЛ ТЕХЭКСПЕРТ")

        current_index = lab_options.index(current_lab) if current_lab in lab_options else 0

        selected_index = st.radio(
            "🔍 Выберите лабораторию:",
            options=range(len(lab_options)),
            format_func=lambda i: lab_display[i],
            index=current_index,
            key="lab_selector"
        )
        selected_lab = lab_options[selected_index]

        if selected_lab != current_lab:
            st.session_state.current_lab = selected_lab
            st.session_state.lab = labs_data[selected_lab]
            st.rerun()

        st.divider()

        lab = labs_data[current_lab]
        st.markdown("### 📊 Статистика")
        st.write(f"**Всего разделов:** {len(lab.sections)}")
        st.write(f"**Продукции:** {len(lab.get_all_products())}")
        st.divider()
        st.markdown("### 📊 Логи использования")

        # Поле для ввода пароля
        admin_password = st.text_input("Пароль администратора", type="password", key="admin_pass")

        if st.button("📥 Скачать логи (CSV)"):
            if admin_password == st.secrets["ADMIN_PASSWORD"]:
                if os.path.exists("usage_logs.csv"):
                    with open("usage_logs.csv", "rb") as f:
                        st.download_button(
                            label="Нажмите для скачивания",
                            data=f,
                            file_name="usage_logs.csv",
                            mime="text/csv"
                        )
                else:
                    st.warning("Логов пока нет")
            else:
                st.error("❌ Неверный пароль")