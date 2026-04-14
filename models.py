"""
Модели данных для экспертной системы.
Описывают структуру области аккредитации лаборатории.
"""

from dataclasses import dataclass, field
from typing import List, Set


@dataclass
class Indicator:
    """Показатель испытаний"""
    name: str                    # Название показателя (Определяемая характеристика)
    range_value: str             # Диапазон определения (может содержать \n)


@dataclass
class Section:
    """Раздел области аккредитации"""
    source: str                  # 'ч1' или 'ч2'
    number: int                  # номер раздела (3, 30, 98)
    full_id: str                 # 'ч1_3', 'ч1_30', 'ч2_7'
    
    products: Set[str] = field(default_factory=set)      # список продукций в этом разделе
    standards: Set[str] = field(default_factory=set)     # список стандартов
    tnved_codes: Set[str] = field(default_factory=set)   # список кодов ТН ВЭД
    indicators: List[Indicator] = field(default_factory=list)  # список показателей


@dataclass
class Laboratory:
    """Лаборатория"""
    name: str                    # 'ИЛ ЦТС' или 'ИЛ ТЕХЭКСПЕРТ'
    sections: List[Section] = field(default_factory=list)  # все разделы лаборатории
    
    def get_all_products(self) -> Set[str]:
        """Возвращает множество всех уникальных продукций в лаборатории"""
        products = set()
        for section in self.sections:
            products.update(section.products)
        return products
    
    def find_sections_by_product(self, query: str) -> List[Section]:
        """Находит разделы, где продукция содержит подстроку query"""
        query_lower = query.lower()
        return [
            section for section in self.sections
            if any(query_lower in product.lower() for product in section.products)
        ]