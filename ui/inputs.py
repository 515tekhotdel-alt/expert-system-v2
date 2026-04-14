"""Поля ввода (продукция, ТН ВЭД, стандарты)."""
import streamlit as st


def render_product_input(default_value: str = "") -> str:
    """Поле ввода продукции с автодополнением (заглушка)."""
    return st.text_input(
        "📦 Продукция",
        value=default_value,
        placeholder="например: белье, замша, стекло",
        key="product_input_main"
    )


def render_tnved_input(default_list: list) -> str:
    """Поле ввода кодов ТН ВЭД."""
    default_text = ", ".join(default_list) if default_list else ""
    return st.text_area(
        "📟 Коды ТН ВЭД",
        value=default_text,
        placeholder="6115, 6116, 6117",
        height=80,
        key="tnved_input_main"
    )


def render_standard_input(default_list: list) -> str:
    """Поле ввода стандартов."""
    default_text = ", ".join(default_list) if default_list else ""
    return st.text_area(
        "📄 Стандарты",
        value=default_text,
        placeholder="ГОСТ 1234-2020, МР 2915-82",
        height=80,
        key="standard_input_main"
    )