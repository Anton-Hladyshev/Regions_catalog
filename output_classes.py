import re

import pandas as pd
from transliterate import translit

df = pd.read_excel("Territories_bd.xlsx")
df = df[2:]
df.columns = df.iloc[0]
df = df[1:]


class TerritoryFrame:
    """Returns a dictionary of parameters of a territory
    input: str or pd.Series
    """

    def __init__(self, code: str | pd.Series) -> None:
        if type(code) == pd.Series:
            self.item = code
            self.code = code.iloc[self.get_level()]
            self.sample = self.form_sample()
            self.name = code.iloc[6]
            self.category = code.iloc[5]

        else:
            self.code = code
            self.item = df[
                (df.iloc[:, 0] == code)
                | (df.iloc[:, 1] == code)
                | (df.iloc[:, 2] == code)
                | (df.iloc[:, 3] == code)
                | (df.iloc[:, 4] == code)
            ].iloc[0]
            self.sample = self.form_sample()
            self.name = self.get_name()
            self.category = self.get_category()
        self.level = self.get_level()
        self.childern_count = self.get_children_count()
        self.parent_id = self.get_parent_id()

    def form_sample(self) -> pd.DataFrame:
        if isinstance(self.code, str):
            general_sample = df[
                (df.iloc[:, 0] == self.code)
                | (df.iloc[:, 1] == self.code)
                | (df.iloc[:, 2] == self.code)
                | (df.iloc[:, 3] == self.code)
                | (df.iloc[:, 4] == self.code)
            ]
        else:
            general_sample = df[(df.iloc[:, self.get_level()] == self.code)]

        if general_sample.shape[0] > 1:
            children_node = general_sample.iloc[1].iloc[:5].notna()
            children_level = 0
            while children_level < 5 and children_node.iloc[children_level]:
                children_level += 1
            children_level -= 1
            if children_level < 4:
                return general_sample[(general_sample.iloc[:, children_level].notna())][
                    (general_sample.iloc[:, children_level + 1].isna())
                ]
            else:
                return general_sample[(general_sample.iloc[:, children_level].notna())]
        else:
            return pd.DataFrame([])

    def get_name(self) -> str:
        return self.item.iloc[6]

    def get_level(self) -> int:
        levels = self.item.iloc[:5].notna()
        level = 0
        while level < 5 and levels.iloc[level]:
            level += 1
        return level - 1

    def get_category(self) -> str:
        return self.item.iloc[5]

    def get_parent_id(self) -> str | None:
        if self.level > 0:
            parent_level = self.level - 1
            parent = self.item.iloc[parent_level]
            return parent
        else:
            return None

    def get_children_count(self) -> int:
        return self.sample.shape[0]

    def show_result(self) -> dict:
        dct_res = {
            "code": self.code,
            "name": self.name.strip(),
            "name_en": translit(self.name, "uk", reversed=True).strip(),
            "level": self.level + 1,
            "parent_id": self.parent_id,
            "category": self.category,
            "children_count": self.childern_count,
        }

        return dct_res


class TerritoriesCatalog:
    """Returns a catalog of dictionaries of territories
    attributes: page - a number of page
                page_size - a number of dictionaries on a page
                code - a code of a territory
                name - a name of a territory
                level - a level of a territory
                parent - a code of a parent territory whose children territories you want to have
                category - a category of a territory
                search - you can search a territory information by its name with a regular expression searcher
    """

    def __init__(
        self,
        page: int = 1,
        page_size: int = 20,
        code: str | None = None,
        name: str | None = None,
        level: int | None = None,
        parent: str | None = None,
        category: str | None = None,
        search: str | None = None,
    ) -> None:
        self.page = page
        self.page_size = page_size
        self.code = code
        self.name = name
        self.level = level
        self.parent = parent
        self.category = category
        self.search = search

    def has_next(self, lenght) -> bool:
        if self.page * self.page_size < lenght:
            return True

        return False

    def has_previous(self, query) -> bool:
        page_to_verify = 1
        if (
            query[(self.page_size * page_to_verify) - self.page_size: page_to_verify * self.page_size].shape[0] > 0
            and self.page > 1
        ):
            return True
        return False

    @staticmethod
    def find_children_level_if_parent(code) -> int | None:
        unit = TerritoryFrame(code)
        if unit.childern_count:
            children_node = df[(df.iloc[:, unit.level]) == code].iloc[1].iloc[:5].notna()
            children_level = 0
            while children_level < 5 and children_node.iloc[children_level]:
                children_level += 1
            children_level -= 1
            return children_level
        else:
            return None

    def set_code(self) -> str:
        if self.code is not None:
            request = f"[(df.iloc[:, 0] == '{self.code}') | (df.iloc[:, 1] == '{self.code}') | (df.iloc[:, 2] == '{self.code}') | (df.iloc[:, 3] == '{self.code}') | (df.iloc[:, 4] == '{self.code}')]"
            if self.level is None:
                request += ".iloc[0]"
            return request
        else:
            return ""

    def set_name(self) -> str:
        if self.name is not None:
            return f"[(df.iloc[:, 6] == '{self.name}')]"
        else:
            return ""

    def set_level(self) -> str:
        if self.level is not None:
            if self.level < 5:
                return f"[(df.iloc[:, {self.level-1}].notna()) & (df.iloc[:, {self.level}].isna())]"
            else:
                return f"[(df.iloc[:, {self.level-1}].notna())]"
        else:
            return ""

    def set_parent(self) -> str:
        if self.parent is not None:
            children_level = self.find_children_level_if_parent(self.parent)
            if children_level is not None:
                if children_level < 4:
                    return f"[(df.iloc[:, {children_level-1}] == '{self.parent}')][(df.iloc[:, {children_level}].notna())][(df.iloc[:, {children_level+1}].isna())]"
                else:
                    return f"[(df.iloc[:, {children_level-1}] == '{self.parent}')][(df.iloc[:, {children_level}].notna())]"
        else:
            return ""

    def set_category(self) -> str:
        if self.category is not None:
            return f"[(df.iloc[:, 5] == '{self.category}')]"
        else:
            return ""

    def search_by_pattern(self, query) -> pd.DataFrame | pd.Series:
        if self.search is not None:
            if isinstance(query, pd.DataFrame):
                return query[df["Назва об’єкта"].str.contains(self.search, flags=re.IGNORECASE, regex=True)]

            elif isinstance(query, pd.Series):
                filtred_series = query.str.extract(f"({self.search})", expand=False).notna()
                if filtred_series.iloc[6]:
                    return query

                else:
                    return pd.DataFrame([])
        else:
            return query

    def compose_and_show_result(self) -> dict:
        result_query_in_string = (
            f"df{self.set_parent()}{self.set_code()}{self.set_name()}{self.set_level()}{self.set_category()}"
        )
        print(result_query_in_string)
        intermidiate_query = eval(result_query_in_string)
        has_next = self.has_next(intermidiate_query.shape[0])
        has_previous = self.has_previous(intermidiate_query)
        result_query_in_string += f".iloc[{(self.page_size*self.page) - self.page_size}:{self.page*self.page_size}]"
        dct_res = {"has_next": has_next, "has_previous": has_previous, "page": self.page, "result": []}

        result_query = self.search_by_pattern(eval(result_query_in_string))
        if isinstance(result_query, pd.Series):
            dct_res["result"].append(TerritoryFrame(result_query).show_result())

        else:
            for index, element in result_query.iterrows():
                dct_res["result"].append(TerritoryFrame(element).show_result())

        return dct_res
