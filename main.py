# ferremas_api/main.py
# ferremas_api/main.py
from fastapi import FastAPI, HTTPException
from typing import List
import logging
import os
import uvicorn
import httpx

from config import settings
from models import Product, Branch, Seller

app = FastAPI()

logger = logging.getLogger("ferremas_api")
logging.basicConfig(level=logging.INFO)

async def fetch_from_ferremas_api(endpoint: str):
    url = f"{settings.FERREMAS_DB_API_URL}/{endpoint}"
    headers = {"token": settings.FERREMAS_DB_API_TOKEN}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Error HTTP al obtener {endpoint}: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        logger.error(f"Error de red o conexión al obtener {endpoint}: {e}")
    return None

@app.get("/products", response_model=List[Product])
async def get_products():
    data = await fetch_from_ferremas_api("products")
    if data is None:
        raise HTTPException(status_code=500, detail="Error al obtener productos")
    return [Product(**item) for item in data]

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    data = await fetch_from_ferremas_api(f"products/{product_id}")
    if data is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return Product(**data)

@app.get("/branches", response_model=List[Branch])
async def get_branches():
    data = await fetch_from_ferremas_api("branches")
    if data is None:
        raise HTTPException(status_code=500, detail="Error al obtener sucursales")
    return [Branch(**item) for item in data]

@app.get("/branches/{branch_id}", response_model=Branch)
async def get_branch(branch_id: int):
    data = await fetch_from_ferremas_api(f"branches/{branch_id}")
    if data is None:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return Branch(**data)

@app.get("/branches/{branch_id}/sellers", response_model=List[Seller])
async def get_sellers_by_branch(branch_id: int):
    data = await fetch_from_ferremas_api(f"branches/{branch_id}/sellers")
    if data is None:
        raise HTTPException(status_code=500, detail="Error al obtener vendedores")
    return [Seller(**item) for item in data]

@app.get("/sellers", response_model=List[Seller])
async def get_sellers():
    data = await fetch_from_ferremas_api("sellers")
    if data is None:
        raise HTTPException(status_code=500, detail="Error al obtener vendedores")
    return [Seller(**item) for item in data]

@app.get("/sellers/{seller_id}", response_model=Seller)
async def get_seller(seller_id: int):
    data = await fetch_from_ferremas_api(f"sellers/{seller_id}")
    if data is None:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    return Seller(**data)

@app.get("/")
async def root():
    return {"message": "API Ferremas funcionando correctamente"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # Solo activar reload en desarrollo local (no en producción)
    reload_flag = os.environ.get("ENV", "production") == "development"

