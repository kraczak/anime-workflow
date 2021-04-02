from typing import List, Dict, Callable

from bs4 import Tag


class TableParser:
    def __init__(self, row_tag: str = 'tr', col_tag: str = 'td'):
        self.row_tag = row_tag
        self.col_tag = col_tag

    def parse(
            self,
            table: Tag,
            columns: List[str],
            href: List[int] = None,
            skip_rows: List[int] = None,
            skip_cols: List[int] = None,
    ) -> List[Dict[str, str]]:
        row_list = table.find_all(self.row_tag)
        skip_cols = skip_cols or []
        skip_rows = skip_rows or []
        href = href or []
        result = []
        for i, row in enumerate(row_list):
            if i not in skip_rows:
                kwargs = self.parse_row(row, columns, skip_cols, href)
                result.append(kwargs)
        return result

    def parse_row(
            self,
            row: Tag,
            columns: List[str],
            skip_cols: List[int],
            href: List[int],
            href_getter: Callable = None
    ) -> Dict[str, str]:
        href_getter = href_getter or self.default_href_getter
        kwargs = {}
        for i, col_tag in enumerate(row.find_all(self.col_tag)):
            if i in href:
                kwargs['url'] = href_getter(col_tag)
            if i not in skip_cols:
                kwargs[columns[i]] = col_tag.get_text()
        return kwargs

    @staticmethod
    def default_href_getter(tag: Tag):
        return tag.find_all('a', href=True).get('href')