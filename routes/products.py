# ferremas_api/routes/products.py
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from typing import List
from models import Product, UserInDB
from database import (
    fetch_product_data,
    add_product_to_ferremas_api,
    update_product_in_ferremas_api,
)
from auth import has_roles

router = APIRouter()

@router.get("/products", response_model=List[Product], summary="Obtener catálogo de productos")
async def get_products():
    """
    Recupera el catálogo completo de productos disponibles en FERREMAS.
    """
    products = await fetch_product_data()
    if products is None:
        raise HTTPException(status_code=500, detail="No se pudo obtener el catálogo de productos")
    return products

@router.get("/products/{product_id}", response_model=Product, summary="Obtener un producto específico")
async def get_product_by_id(product_id: int = Path(..., description="ID del producto")):
    """
    Recupera los detalles de un producto específico por su ID.
    """
    product = await fetch_product_data(product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product[0]

@router.get("/products/promotions", response_model=List[Product], summary="Obtener productos en promoción")
async def get_promotion_products():
    """
    Recupera una lista de productos que actualmente están en promoción.
    """
    all_products = await fetch_product_data()
    if all_products is None:
        raise HTTPException(status_code=500, detail="No se pudo obtener el catálogo para promociones")

    return [p for p in all_products if p.is_promotion]

@router.get("/products/newArrivals", response_model=List[Product], summary="Obtener productos como novedades")
async def get_new_arrival_products():
    """
    Recupera una lista de productos marcados como novedades.
    """
    all_products = await fetch_product_data()
    if all_products is None:
        raise HTTPException(status_code=500, detail="No se pudo obtener el catálogo para novedades")

    return [p for p in all_products if p.is_new_product]

@router.post("/products", response_model=Product, status_code=201, summary="Agregar un nuevo producto al catálogo")
async def add_product(
    product: Product,
    current_user: UserInDB = Depends(has_roles(["admin", "mantenedor"]))
):
    """
    Permite a los usuarios con rol de 'admin' o 'mantenedor' agregar un nuevo producto al catálogo.
    """
    created_product = await add_product_to_ferremas_api(product)
    if created_product is None:
        raise HTTPException(status_code=500, detail="No se pudo agregar el producto")
    return created_product

@router.put("/products/{product_id}/markPromotion", response_model=Product, summary="Marcar/desmarcar producto como promoción")
async def mark_product_promotion(
    product_id: int = Path(..., description="ID del producto"),
    is_promotion: bool = Query(..., description="Estado de promoción"),
    current_user: UserInDB = Depends(has_roles(["admin", "mantenedor"]))
):
    """
    Marca o desmarca un producto como promoción.
    """
    updated = await update_product_in_ferremas_api(product_id, {"is_promotion": is_promotion})
    if updated is None:
        raise HTTPException(status_code=500, detail="No se pudo actualizar promoción")
    return updated

@router.put("/products/{product_id}/markNewArrival", response_model=Product, summary="Marcar/desmarcar producto como novedad")
async def mark_product_new_arrival(
    product_id: int = Path(..., description="ID del producto"),
    is_new_product: bool = Query(..., description="Estado de novedad"),
    current_user: UserInDB = Depends(has_roles(["admin", "mantenedor"]))
):
    """
    Marca o desmarca un producto como novedad.
    """
    updated = await update_product_in_ferremas_api(product_id, {"is_new_product": is_new_product})
    if updated is None:
        raise HTTPException(status_code=500, detail="No se pudo actualizar novedad")
    return updated
