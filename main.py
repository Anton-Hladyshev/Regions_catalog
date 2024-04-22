from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query

from models import CatalogOfUnits, UnitModel
from output_classes import TerritoriesCatalog, TerritoryFrame

app = FastAPI(title="Довідник КАТОТТГ")


@app.get("/api/katottg/{code}", response_model=UnitModel)
def get_unit_by_code(code: Annotated[str, Path(description="Код КАТОТТГ", max_length=19)]):
    try:
        unit = TerritoryFrame(code=code)
        return unit.show_result()

    except IndexError:
        raise HTTPException(status_code=404, detail="Територіальну одиницю не знайдено")


@app.get("/api/katottg", response_model=CatalogOfUnits)
def get_list_of_units(
    page: Annotated[int, Query(description="Номер сторінки", ge=1, le=10000)] = 1,
    page_size: Annotated[int, Query(description="Кількість елементів на сторінці", gt=1, le=1000)] = 20,
    code: Annotated[str | None, Query(description="Фільтр по коду КАТОТТГ")] = None,
    name: Annotated[str | None, Query(description="Фільтр по назві території")] = None,
    level: Annotated[int | None, Query(description="Фільтр по рівню території")] = None,
    parent: Annotated[str | None, Query(description="Фільтр по коду КАТОТТГ території вищого рівня")] = None,
    category: Annotated[str | None, Query(description="Фільтр по категорії території")] = None,
    search: Annotated[str | None, Query(description="Шукати по назві")] = None,
):
    try:
        catalog = TerritoriesCatalog(
            page=page,
            page_size=page_size,
            code=code,
            name=name,
            level=level,
            parent=parent,
            category=category,
            search=search,
        )

        return catalog.compose_and_show_result()

    except IndexError:
        raise HTTPException(status_code=404, detail="Територіальну одиницю не знайдено")
