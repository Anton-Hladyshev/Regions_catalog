# 🗂️ KATOTTG Directory — Classifier of Addresses of Territories of Objects of Administrative-Territorial and Territorial Division

This FastAPI-based service provides access to territorial unit data classified by **KATOTTG** — the Ukrainian classifier of administrative and territorial units.

---

## 🧭 Endpoints

### 1. 🔍 Get Unit by KATOTTG Code

**GET** `/api/katottg/{code}`

Returns a single territorial unit by its unique KATOTTG code.

#### 🔧 Path Parameters:
| Name | Type | Description |
|------|------|-------------|
| `code` | `string` (max length: 19) | KATOTTG code of the territorial unit |

#### 🧾 Response:
Returns a JSON object describing the unit.

#### 🛑 Errors:
- `404 Not Found` — Territorial unit not found

#### 📦 Example Request:
```http
GET /api/katottg/1234567890123456789
```

---

### 2. 📚 Get a Paginated List of Units

**GET** `/api/katottg`

Returns a paginated list of territorial units with optional filters.

#### 🔧 Query Parameters:

| Name       | Type     | Constraints         | Description |
|------------|----------|---------------------|-------------|
| `page`     | `int`    | `1 ≤ page ≤ 10000`  | Page number (default: 1) |
| `page_size`| `int`    | `2 ≤ size ≤ 1000`   | Number of items per page (default: 20) |
| `code`     | `string` | Optional            | Filter by KATOTTG code |
| `name`     | `string` | Optional            | Filter by territorial unit name |
| `level`    | `int`    | Optional            | Filter by administrative level |
| `parent`   | `string` | Optional            | Filter by parent unit's KATOTTG code |
| `category` | `string` | Optional            | Filter by category of the unit |
| `search`   | `string` | Optional            | Search by name (partial match) |

#### 🧾 Response:
Returns a paginated list of units matching the filters.

#### 🛑 Errors:
- `404 Not Found` — No territorial units found for given filters

#### 📦 Example Request:
```http
GET /api/katottg?page=1&page_size=10&level=2&search=kyiv
```

---

## ✅ Response Models

- `UnitModel` – Returned by `/api/katottg/{code}`
- `CatalogOfUnits` – Returned by `/api/katottg`

*(For exact schema definitions, refer to your Pydantic models in the source code.)*

---

## 🌐 API Documentation

By default, FastAPI interactive documentation is available at the root:

🔗 [Swagger UI (OpenAPI)](http://localhost:8000/)

---

## ℹ️ Notes

- This service uses the [FastAPI](https://fastapi.tiangolo.com/) framework.
- All endpoints return responses in **JSON** format.
- KATOTTG = “Classifier of Addresses of Territories of Objects of Administrative-Territorial and Territorial Division” (Ukraine).

