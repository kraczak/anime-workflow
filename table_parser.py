from typing import List, Dict, Callable, Type
from urllib.parse import urljoin

from bs4 import Tag
from pydantic import BaseModel


class TableParser:
    def __init__(self, row_tag: str = 'tr', col_tag: str = 'td'):
        self.row_tag = row_tag
        self.col_tag = col_tag

    def parse(
            self,
            table: Tag,
            output_class: Type[BaseModel],
            columns: List[str],
            href: List[int] = None,
            href_getter: Callable = None,
            skip_rows: List[int] = None,
            skip_cols: List[int] = None,
            base_url: str = None
    ) -> List:
        row_list = table.find_all(self.row_tag)
        skip_cols = skip_cols or []
        skip_rows = skip_rows or []
        href_getter = href_getter or self.default_href_getter
        href = href or []
        result = []
        for i, row in enumerate(row_list):
            if i not in skip_rows:
                kwargs = self.parse_row(row, columns, skip_cols, href, href_getter, base_url)
                result.append(output_class(**kwargs))
        return result

    def parse_row(
            self,
            row: Tag,
            columns: List[str],
            skip_cols: List[int],
            href: List[int],
            href_getter: Callable,
            base_url: str = None
    ) -> Dict[str, str]:
        kwargs = {}
        k = 0
        for i, col_tag in enumerate(row.find_all(self.col_tag)):
            if i in href:
                url = href_getter(col_tag)
                if base_url is not None:
                    url = urljoin(base_url, url)
                kwargs['url'] = url
            if i not in skip_cols:
                kwargs[columns[i-k]] = col_tag.get_text()
            else:
                k += 1
        return kwargs

    @staticmethod
    def default_href_getter(tag: Tag) -> str:
        return tag.find('a', href=True).get('href')