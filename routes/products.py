# ferremas_api/routes/products.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from models import Product, UserInDB
from database import fetch_product_data, add_product_to_ferremas_api, update_product_in_ferremas_api
from auth import has_role # Importar la función has_role para control de acceso

router = APIRouter()

@router.get("/products", response_model=List[Product], summary="Obtener catálogo de productos")
async def get_products():
    """
    Recupera el catálogo completo de productos disponibles en FERREMAS.
    """
    products = await fetch_product_data()
    if products is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo obtener el catálogo de productos")
    return products

@router.get("/products/{product_id}", response_model=Product, summary="Obtener un producto específico")
async def get_product_by_id(product_id: int):
    """
    Recupera los detalles de un producto específico por su ID.
    """
    product = await fetch_product_data(product_id=product_id)
    if not product: # fetch_product_data devuelve una lista, incluso si es un solo producto
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return product[0] # Retorna el primer elemento de la lista

@router.get("/products/promotions", response_model=List[Product], summary="Obtener productos en promoción")
async def get_promotion_products():
    """
    Recupera una lista de productos que actualmente están en promoción.
    """
    all_products = await fetch_product_data()
    if all_products is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo obtener el catálogo de productos para promociones")
    
    promotion_products = [product for product in all_products if product.is_promotion]
    return promotion_products

@router.get("/products/newArrivals", response_model=List[Product], summary="Obtener productos como novedades")
async def get_new_arrival_products():
    """
    Recupera una lista de productos marcados como novedades.
    """
    all_products = await fetch_product_data()
    if all_products is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo obtener el catálogo de productos para novedades")
    
    new_arrival_products = [product for product in all_products if product.is_new_arrival]
    return new_arrival_products

@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED, summary="Agregar un nuevo producto al catálogo")
async def add_product(product: Product, current_user: UserInDB = Depends(has_role(["admin", "mantenedor"]))):
    """
    Permite a los usuarios con rol de 'admin' o 'mantenedor' agregar un nuevo producto al catálogo.
    """
    created_product = await add_product_to_ferremas_api(product)
    if created_product is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo agregar el producto")
    return created_product

@router.put("/products/{product_id}/markPromotion", response_model=Product, summary="Marcar/desmarcar producto como promoción")
async def mark_product_promotion(product_id: int, is_promotion: bool, current_user: UserInDB = Depends(has_role(["admin", "mantenedor"]))):
    """
    Permite a los usuarios con rol de 'admin' o 'mantenedor' marcar o desmarcar un producto como promoción.
    """
    product_update = {"is_promotion": is_promotion}
    updated_product = await update_product_in_ferremas_api(product_id, product_update)
    if updated_product is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo actualizar el estado de promoción del producto")
    return updated_product

@router.put("/products/{product_id}/markNewArrival", response_model=Product, summary="Marcar/desmarcar producto como novedad")
async def mark_product_new_arrival(product_id: int, is_new_arrival: bool, current_user: UserInDB = Depends(has_role(["admin", "mantenedor"]))):
    """
    Permite a los usuarios con rol de 'admin' o 'mantenedor' marcar o desmarcar un producto como novedad.
    """
    product_update = {"is_new_arrival": is_new_arrival}
    updated_product = await update_product_in_ferremas_api(product_id, product_update)
    if updated_product is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo actualizar el estado de novedad del producto")
    return updated_product
# routes/products.py

from fastapi import APIRouter

# You MUST define an instance of APIRouter and name it 'router'
# Or whatever name you are trying to import in main.py
router = APIRouter()

@router.get("/products/")
async def read_products():
    # Your logic for reading products
    return {"message": "List of products"}

# Add other product-related endpoints here using @router.post, @router.put, etc.