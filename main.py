# ferremas_api/main.py
from fastapi import FastAPI
from typing import List, Optional

import httpx
from config import settings
from models import Product, Branch, Seller

app = FastAPI()

async def fetch_from_ferremas_api(endpoint: str):
    url = f"{settings.FERREMAS_DB_API_URL}/{endpoint}"
    headers = {"token": settings.FERREMAS_DB_API_TOKEN}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        print(f"Error HTTP al obtener {endpoint}: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Error de red o conexión al obtener {endpoint}: {e}")
    return None

@app.get("/products", response_model=List[Product])
async def get_products():
    data = await fetch_from_ferremas_api("products")
    if data:
        return [Product(**item) for item in data]
    return []

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    data = await fetch_from_ferremas_api(f"products/{product_id}")
    if data:
        return Product(**data)
    return {}

@app.get("/branches", response_model=List[Branch])
async def get_branches():
    data = await fetch_from_ferremas_api("branches")
    if data:
        return [Branch(**item) for item in data]
    return []

@app.get("/branches/{branch_id}", response_model=Branch)
async def get_branch(branch_id: int):
    data = await fetch_from_ferremas_api(f"branches/{branch_id}")
    if data:
        return Branch(**data)
    return {}

@app.get("/branches/{branch_id}/sellers", response_model=List[Seller])
async def get_sellers_by_branch(branch_id: int):
    data = await fetch_from_ferremas_api(f"branches/{branch_id}/sellers")
    if data:
        return [Seller(**item) for item in data]
    return []

@app.get("/sellers", response_model=List[Seller])
async def get_sellers():
    data = await fetch_from_ferremas_api("sellers")
    if data:
        return [Seller(**item) for item in data]
    return []

@app.get("/sellers/{seller_id}", response_model=Seller)
async def get_seller(seller_id: int):
    data = await fetch_from_ferremas_api(f"sellers/{seller_id}")
    if data:
        return Seller(**data)
    return {}

# También puedes agregar las funciones para POST y PUT si quieres

