"""
Загрузка данных из Google Sheets и преобразование в модели.
"""

import re
import pandas as pd
import requests
import io
import streamlit as st
from typing import Dict, List, Set

from models import Laboratory, Section, Indicator

# ============================================================
# КОНФИГУРАЦИЯ ЛАБОРАТОРИЙ
# ============================================================
LAB_CONFIGS = {
    'ИЛ ЦТС': {
        'file1': '1pYge7ubGx7_rHxvs0X_xLK8GXIQUnH7P',
        'file2': '1CXXkOkqUpT-tgrQv4I7-TKH0zrC86CS4'
    },
    'ИЛ ТЕХЭКСПЕРТ': {
        'file1': '1tNKL2TLWamo6XDp_G2pOJ1tINEZ-xsMB',
        'file2': '1VUDsNPy5dGh_VkslZxak1VFDgeSP8uhp'
    }
}


# ============================================================
# ЗАГРУЗКА ОДНОГО EXCEL-ФАЙЛА
# ============================================================
def _load_single_excel(file_id: str, source_name: str) -> pd.DataFrame:
    """
    Загружает Excel-файл из Google Sheets по ID.
    source_name: 'ч1' или 'ч2'
    Возвращает сырой DataFrame.
    """
    url = f'https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx'
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        df_raw = pd.read_excel(io.BytesIO(response.content))
        df_raw.columns = df_raw.columns.str.strip()
        df_raw['_source'] = source_name
        return df_raw
    except Exception as e:
        st.error(f"Ошибка загрузки файла {file_id} ({source_name}): {e}")
        return pd.DataFrame()


# ============================================================
# ПАРСИНГ EXCEL В СПИСОК РАЗДЕЛОВ
# ============================================================
def _parse_excel_to_sections(df_raw: pd.DataFrame) -> List[Section]:
    """
    Парсит сырой DataFrame и возвращает список разделов (Section).
    """
    sections_dict: Dict[str, Section] = {}
    current_section_num = None
    source = df_raw['_source'].iloc[0] if not df_raw.empty else 'ч1'

    for _, row in df_raw.iterrows():
        # Определяем номер раздела из колонки 'N П/П'
        n_pp = row.get('N П/П', '')
        if pd.notna(n_pp) and str(n_pp).strip() != '':
            match = re.search(r'\d+\.(\d+)\.', str(n_pp))
            if match:
                current_section_num = int(match.group(1))

        if current_section_num is None:
            continue

        # Создаём или получаем раздел
        section_id = f"{source}_{current_section_num}"
        if section_id not in sections_dict:
            sections_dict[section_id] = Section(
                source=source,
                number=current_section_num,
                full_id=section_id
            )
        
        section = sections_dict[section_id]

        # Продукция
        objects_val = row.get('Наименование объекта', '')
        if pd.notna(objects_val) and str(objects_val).strip():
            for obj in str(objects_val).split(';'):
                obj_clean = obj.strip()
                if obj_clean:
                    section.products.add(obj_clean)

        # Стандарты (НЕ разделяем по ; — сохраняем всю ячейку как один стандарт)
        standards_val = row.get('Документы, устанавливающие правила и методы исследований (испытаний) и измерений', '')
        if pd.notna(standards_val) and str(standards_val).strip():
            std_full = str(standards_val).strip()
            section.standards.add(std_full)

        # ТН ВЭД
        tnved_val = row.get('КОД ТН ВЭД ЕАЭС', '')
        if pd.notna(tnved_val) and str(tnved_val).strip():
            for code in str(tnved_val).split(';'):
                code_clean = code.strip()
                if code_clean and code_clean.isdigit():
                    section.tnved_codes.add(code_clean)

        # Показатели
        indicator_name = row.get('Определяемая характеристика (Показатель)', '')
        if pd.notna(indicator_name) and str(indicator_name).strip():
            name_clean = str(indicator_name).strip()
            range_clean = ''
            indicator_range = row.get('Диапазон определения', '')
            if pd.notna(indicator_range) and str(indicator_range).strip():
                range_clean = str(indicator_range).strip()
                range_clean = re.sub(r'-\n', '\n', range_clean)
                range_clean = re.sub(r'\n-', '\n', range_clean)
            
            # Добавляем показатель, если его ещё нет
            indicator = Indicator(name=name_clean, range_value=range_clean)
            section.indicators.append(indicator)

    return list(sections_dict.values())


# ============================================================
# ЗАГРУЗКА ВСЕХ ЛАБОРАТОРИЙ
# ============================================================
@st.cache_data(ttl=3600, show_spinner="Загрузка данных лабораторий...")
def load_laboratories() -> Dict[str, Laboratory]:
    """
    Загружает данные всех лабораторий из Google Sheets.
    Возвращает словарь {название_лаборатории: Laboratory}.
    """
    laboratories = {}

    for lab_name, config in LAB_CONFIGS.items():
        with st.spinner(f'Загрузка {lab_name}...'):
            # Загружаем оба файла
            df1 = _load_single_excel(config['file1'], 'ч1')
            df2 = _load_single_excel(config['file2'], 'ч2')

            if df1.empty and df2.empty:
                st.error(f"Не удалось загрузить данные для {lab_name}")
                continue

            # Парсим разделы из каждого файла
            sections = []
            if not df1.empty:
                sections.extend(_parse_excel_to_sections(df1))
            if not df2.empty:
                sections.extend(_parse_excel_to_sections(df2))

            # Создаём лабораторию
            laboratories[lab_name] = Laboratory(name=lab_name, sections=sections)

    return laboratories


# ============================================================
# ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ (для обратной совместимости)
# ============================================================
def parse_excel_to_sections(excel_content: bytes, source_name: str) -> List[Section]:
    """
    Парсит Excel-файл из байтов и возвращает список разделов.
    Оставлена для обратной совместимости.
    """
    df_raw = pd.read_excel(io.BytesIO(excel_content))
    df_raw.columns = df_raw.columns.str.strip()
    df_raw['_source'] = source_name
    return _parse_excel_to_sections(df_raw)