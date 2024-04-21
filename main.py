from fastapi import FastAPI, Query, Path, HTTPException
from typing import Union
from typing_extensions import Annotated

from models import Unit_Model, Catalog_of_units
from output_classes import Territory_frame, Teritories_catalog

app = FastAPI(title='Довідник КАТОТТГ')



@app.get("/api/katottg/{code}", response_model=Unit_Model)
def get_unit_by_code(code: Annotated[str, Path(description='Код КАТОТТГ', max_length=19)]):
    try:
        unit = Territory_frame(code=code)
        return unit.show_result()

    except IndexError:
        raise HTTPException(status_code=404, detail='Територіальну одиницю не знайдено')

@app.get("/api/katottg", response_model=Catalog_of_units)
def get_list_of_units(page: Annotated[Union[int, None], Query(description='Номер сторінки', ge=1, le=10000)] = 1,
                      page_size: Annotated[Union[int, None], Query(description='Кількість елементів на сторінці', gt=1, le=1000)] = 20,
                      code: Annotated[Union[str, None], Query(description='Фільтр по коду КАТОТТГ')] = None,
                      name: Annotated[Union[str, None], Query(description='Фільтр по назві території')] = None,
                      level: Annotated[Union[int, None], Query(description='Фільтр по рівню території')] = None,
                      parent: Annotated[Union[str, None], Query(description='Фільтр по коду КАТОТТГ території вищого рівня')] = None,
                      category: Annotated[Union[str, None], Query(description='Фільтр по категорії території')] = None,
                      search: Annotated[Union[str, None], Query(description='Шукати по назві')] = None):

    try:
        catalog = Teritories_catalog(page=page,
                                page_size=page_size,
                                code=code,
                                name=name,
                                level=level,
                                parent=parent,
                                category=category,
                                search=search)

        return catalog.compose_and_show_result()

    except IndexError:
        raise HTTPException(status_code=404, detail='Територіальну одиницю не знайдено')
