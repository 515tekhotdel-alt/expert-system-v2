"""
Бизнес-логика экспертной системы.
Чистые функции, не зависящие от Streamlit.
"""

from typing import List, Set, Dict, Tuple
from collections import defaultdict
from models import Section, Indicator, Laboratory


# ============================================================
# ГРУППИРОВКА РАЗДЕЛОВ ДЛЯ ОТОБРАЖЕНИЯ
# ============================================================
def group_sections_for_display(sections: Set[str]) -> str:
    """
    Преобразует множество разделов ('ч1_3', 'ч1_30', 'ч2_7')
    в читаемую строку: 'ч1: 3, 30; ч2: 7'
    """
    if not sections:
        return ''
    
    by_source = defaultdict(list)
    for section in sections:
        if '_' in section:
            source, num = section.split('_', 1)
            try:
                by_source[source].append(int(num))
            except ValueError:
                by_source[source].append(num)
        else:
            by_source['ч1'].append(section)

    result_parts = []
    for source in sorted(by_source.keys()):
        nums = sorted(set(by_source[source]))
        if not nums:
            continue
            
        grouped = []
        start = end = nums[0]
        
        for n in nums[1:]:
            if n == end + 1:
                end = n
            else:
                grouped.append(str(start) if start == end else f"{start}-{end}")
                start = end = n
        grouped.append(str(start) if start == end else f"{start}-{end}")
        
        result_parts.append(f"{source}: {', '.join(grouped)}")
    
    return '; '.join(result_parts)


# ============================================================
# ПОИСК ПРОДУКЦИИ
# ============================================================
def search_products(lab: Laboratory, query: str) -> Dict[str, Set[str]]:
    """
    Ищет продукцию по подстроке query.
    Возвращает словарь: {формулировка_продукции: множество_разделов}
    """
    result: Dict[str, Set[str]] = defaultdict(set)
    query_lower = query.lower()
    
    for section in lab.sections:
        for product in section.products:
            if query_lower in product.lower():
                result[product].add(section.full_id)
    
    return dict(result)


# ============================================================
# ФИЛЬТРАЦИЯ ПО ТН ВЭД
# ============================================================
def filter_by_tnved(lab: Laboratory, tnved_code: str, product_sections: Set[str]) -> Set[str]:
    """
    Находит разделы, где встречается код ТН ВЭД, и пересекает с product_sections.
    """
    tnved_sections = set()
    
    for section in lab.sections:
        for code in section.tnved_codes:
            if tnved_code in code:
                tnved_sections.add(section.full_id)
    
    return tnved_sections.intersection(product_sections)


# ============================================================
# ФИЛЬТРАЦИЯ ПО СТАНДАРТУ И ТН ВЭД
# ============================================================
def filter_by_standard_and_tnved(
    lab: Laboratory, 
    standard_query: str, 
    tnved_code: str,
    product_sections: Set[str]
) -> Set[str]:
    """
    Находит разделы, где встречается стандарт И код ТН ВЭД, и пересекает с product_sections.
    """
    std_sections = set()
    tnved_sections = set()
    std_query_lower = standard_query.lower()
    
    for section in lab.sections:
        # Стандарты
        for std in section.standards:
            if std_query_lower in std.lower():
                std_sections.add(section.full_id)
        
        # ТН ВЭД
        for code in section.tnved_codes:
            if tnved_code in code:
                tnved_sections.add(section.full_id)
    
    common = std_sections.intersection(tnved_sections)
    return common.intersection(product_sections)


# ============================================================
# ИЗВЛЕЧЕНИЕ ПОКАЗАТЕЛЕЙ
# ============================================================
def extract_indicators(
    lab: Laboratory,
    sections: Set[str],
    selected_standards: List[str]
) -> List[Dict]:
    """
    Извлекает показатели из выбранных разделов и стандартов.
    Возвращает список словарей с ключами: 'standard', 'section', 'name', 'range'
    """
    result = []
    
    # Создаём индекс: full_id -> Section
    section_index = {s.full_id: s for s in lab.sections}
    
    # Создаём индекс: стандарт -> список разделов
    std_to_sections: Dict[str, Set[str]] = defaultdict(set)
    if selected_standards:
        for section in lab.sections:
            for std in section.standards:
                std_lower = std.lower()
                for sel_std in selected_standards:
                    if sel_std.lower() in std_lower:
                        std_to_sections[std].add(section.full_id)
    
    for section_id in sorted(sections):
        section = section_index.get(section_id)
        if not section:
            continue
        
        # Определяем, какие стандарты относятся к этому разделу
        relevant_standards = []
        if selected_standards:
            for std, secs in std_to_sections.items():
                if section_id in secs:
                    relevant_standards.append(std)
        
        # Если стандарты не выбраны — не добавляем показатели
        if selected_standards and not relevant_standards:
            continue
        
        # Добавляем показатели
        for indicator in section.indicators:
            if relevant_standards:
                for std in relevant_standards:
                    result.append({
                        'standard': std,
                        'section': section_id,
                        'name': indicator.name,
                        'range': indicator.range_value
                    })
            else:
                # Если стандарты не выбраны, не выводим показатели (по бизнес-логике)
                pass
    
    return result


# ============================================================
# ПЕРЕСЕЧЕНИЕ МНОЖЕСТВ РАЗДЕЛОВ
# ============================================================
def intersect_sections(*sets: Set[str]) -> Set[str]:
    """
    Пересекает несколько множеств разделов.
    Если множество пустое — возвращает пустое множество.
    """
    if not sets:
        return set()
    
    # Отфильтровываем пустые множества
    non_empty = [s for s in sets if s]
    if not non_empty:
        return set()
    
    result = non_empty[0].copy()
    for s in non_empty[1:]:
        result.intersection_update(s)
    
    return result