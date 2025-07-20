from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query

from models import CatalogOfUnits, UnitModel
from output_classes import TerritoriesCatalog, TerritoryFrame

app = FastAPI(title="KATOTTG Directory — Classifier of Addresses of Territories of Objects of Administrative-Territorial and Territorial Division", docs_url='/', redoc_url=None)


@app.get("/api/katottg/{code}", response_model=UnitModel)
def get_unit_by_code(code: Annotated[str, Path(description="Код КАТОТТГ", max_length=19)]):
    try:
        unit = TerritoryFrame(code=code)
        return unit.show_result()

    except IndexError:
        raise HTTPException(status_code=404, detail="Територіальну одиницю не знайдено/ Unknown territorial unit")


@app.get("/api/katottg", response_model=CatalogOfUnits)
def get_list_of_units(
    page: Annotated[int, Query(description="Номер сторінки / Page number", ge=1, le=10000)] = 1,
    page_size: Annotated[int, Query(description="Кількість елементів на сторінці / Number of elements on a page", gt=1, le=1000)] = 20,
    code: Annotated[str | None, Query(description="Фільтр по коду КАТОТТГ / Filter by a code of a territory unit (KATOTTG — Classifier of Addresses of Territories of Objects of Administrative-Territorial and Territorial Division)")] = None,
    name: Annotated[str | None, Query(description="Фільтр по назві території / Filter by the name of a territorial unit")] = None,
    level: Annotated[int | None, Query(description="Фільтр по рівню території / Filter by a administrative level of territorial unit")] = None,
    parent: Annotated[str | None, Query(description="Фільтр по коду КАТОТТГ території вищого рівня / Filter by a code of a territory unit (KATOTTG) of  a higher administratice level")] = None,
    category: Annotated[str | None, Query(description="Фільтр по категорії території / Filter by a category of a territory")] = None,
    search: Annotated[str | None, Query(description="Шукати по назві / Search by the name")] = None,
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
        raise HTTPException(status_code=404, detail="Територіальну одиницю не знайдено / Unknown territorial unit")
