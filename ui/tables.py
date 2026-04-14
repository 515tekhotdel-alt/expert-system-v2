"""Компоненты таблиц с чекбоксами."""
import streamlit as st
import pandas as pd
from typing import List, Dict, Set


def render_product_table(data: List[Dict], selected: Set[int]) -> Set[int]:
    """Таблица 1. Продукция."""
    if not data:
        return selected
    
    st.markdown("**📦 Таблица 1. Продукция**")
    
    df = pd.DataFrame(data)
    df_display = df[['Формулировка продукции', 'Разделы']].copy()
    
    # Используем session_state для хранения чекбоксов
    cb_key = "product_checkboxes"
    if cb_key not in st.session_state:
        st.session_state[cb_key] = {i: False for i in range(len(df_display))}
    
    # Обновляем из selected
    for idx in selected:
        if idx < len(df_display):
            st.session_state[cb_key][idx] = True
    
    # Создаём колонку с чекбоксами через отдельные виджеты
    cols = st.columns([0.1, 0.45, 0.45])
    cols[0].write("**Выбор**")
    cols[1].write("**Формулировка продукции**")
    cols[2].write("**Разделы**")
    
    new_selected = set()
    for idx, row in df_display.iterrows():
        cols = st.columns([0.1, 0.45, 0.45])
        checked = cols[0].checkbox(
            " ",
            key=f"prod_cb_{idx}",
            value=st.session_state[cb_key].get(idx, False),
            label_visibility="collapsed"
        )
        st.session_state[cb_key][idx] = checked
        if checked:
            new_selected.add(idx)
        cols[1].write(str(row['Формулировка продукции']))
        cols[2].write(str(row['Разделы']))
    
    return new_selected

def render_tnved_table(data: List[Dict], selected: Set[int]) -> Set[int]:
    """Таблица 2. ТН ВЭД."""
    if not data:
        return selected
    
    st.markdown("**📟 Таблица 2. ТН ВЭД**")
    
    df = pd.DataFrame(data)
    df_display = df[['ТН ВЭД', 'Разделы']].copy()
    
    cb_key = "tnved_checkboxes"
    if cb_key not in st.session_state:
        st.session_state[cb_key] = {i: False for i in range(len(df_display))}
    
    for idx in selected:
        if idx < len(df_display):
            st.session_state[cb_key][idx] = True
    
    cols = st.columns([0.1, 0.3, 0.6])
    cols[0].write("**Выбор**")
    cols[1].write("**ТН ВЭД**")
    cols[2].write("**Разделы**")
    
    new_selected = set()
    for idx, row in df_display.iterrows():
        cols = st.columns([0.1, 0.3, 0.6])
        checked = cols[0].checkbox(
            " ",
            key=f"tnved_cb_{idx}",
            value=st.session_state[cb_key].get(idx, False),
            label_visibility="collapsed"
        )
        st.session_state[cb_key][idx] = checked
        if checked:
            new_selected.add(idx)
        cols[1].write(str(row['ТН ВЭД']))
        cols[2].write(str(row['Разделы']))
    
    return new_selected


def render_standard_table(data: List[Dict], selected: Set[int]) -> Set[int]:
    """Таблица 3. Стандарты."""
    if not data:
        return selected
    
    st.markdown("**📄 Таблица 3. Стандарты**")
    
    df = pd.DataFrame(data)
    df_display = df[['Стандарт', 'ТН ВЭД', 'Разделы']].copy()
    
    cb_key = "standard_checkboxes"
    if cb_key not in st.session_state:
        st.session_state[cb_key] = {i: False for i in range(len(df_display))}
    
    for idx in selected:
        if idx < len(df_display):
            st.session_state[cb_key][idx] = True
    
    cols = st.columns([0.1, 0.35, 0.2, 0.35])
    cols[0].write("**Выбор**")
    cols[1].write("**Стандарт**")
    cols[2].write("**ТН ВЭД**")
    cols[3].write("**Разделы**")
    
    new_selected = set()
    for idx, row in df_display.iterrows():
        cols = st.columns([0.1, 0.35, 0.2, 0.35])
        checked = cols[0].checkbox(
            " ",
            key=f"std_cb_{idx}",
            value=st.session_state[cb_key].get(idx, False),
            label_visibility="collapsed"
        )
        st.session_state[cb_key][idx] = checked
        if checked:
            new_selected.add(idx)
        cols[1].write(str(row['Стандарт']))
        cols[2].write(str(row['ТН ВЭД']))
        cols[3].write(str(row['Разделы']))
    
    return new_selected