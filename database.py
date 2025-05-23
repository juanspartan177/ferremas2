# ferremas_api/database.py
import httpx
from typing import List, Dict, Any, Optional

from config import settings
from models import Product, Branch, Seller

async def fetch_from_ferremas_api(endpoint: str) -> Optional[List[Dict[str, Any]]]:
    """
    Función genérica para hacer peticiones GET a la API de Ferremas.
    """
    url = f"{settings.FERREMAS_DB_API_URL}/{endpoint}"
    headers = {"token": settings.FERREMAS_DB_API_TOKEN}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status() # Lanza una excepción para códigos de estado HTTP 4xx/5xx
            return response.json()
    except httpx.HTTPStatusError as e:
        print(f"Error HTTP al obtener {endpoint}: {e.response.status_code} - {e.response.text}")
        return None
    except httpx.RequestError as e:
        print(f"Error de red o conexión al obtener {endpoint}: {e}")
        return None

async def fetch_product_data(product_id: Optional[int] = None) -> Optional[List[Product]]:
    """
    Obtiene el catálogo completo de productos o un producto específico.
    """
    endpoint = "products"
    if product_id:
        endpoint = f"products/{product_id}"
    
    data = await fetch_from_ferremas_api(endpoint)
    if data:
        if product_id:
            return [Product(**data)] # Si es un solo producto, lo envuelve en una lista para consistencia
        return [Product(**item) for item in data]
    return None

async def fetch_branch_data(branch_id: Optional[int] = None) -> Optional[List[Branch]]:
    """
    Obtiene el listado completo de sucursales o una sucursal específica.
    """
    endpoint = "branches"
    if branch_id:
        endpoint = f"branches/{branch_id}"

    data = await fetch_from_ferremas_api(endpoint)
    if data:
        if branch_id:
            return [Branch(**data)]
        return [Branch(**item) for item in data]
    return None

async def fetch_seller_data(branch_id: Optional[int] = None, seller_id: Optional[int] = None) -> Optional[List[Seller]]:
    """
    Obtiene el listado de vendedores por sucursal o un vendedor específico.
    """
    endpoint = "sellers"
    if branch_id:
        endpoint = f"branches/{branch_id}/sellers"
    if seller_id:
        endpoint = f"sellers/{seller_id}"

    data = await fetch_from_ferremas_api(endpoint)
    if data:
        if seller_id and not isinstance(data, list): # Si es un solo vendedor y no es una lista
            return [Seller(**data)]
        return [Seller(**item) for item in data]
    return None

# Funciones para operaciones de escritura (ej. agregar/modificar productos)
async def add_product_to_ferremas_api(product: Product) -> Optional[Product]:
    """
    Agrega un nuevo producto a la API de Ferremas.
    """
    url = f"{settings.FERREMAS_DB_API_URL}/products"
    headers = {"token": settings.FERREMAS_DB_API_TOKEN, "Content-Type": "application/json"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=product.model_dump())
            response.raise_for_status()
            return Product(**response.json())
    except httpx.HTTPStatusError as e:
        print(f"Error HTTP al agregar producto: {e.response.status_code} - {e.response.text}")
        return None
    except httpx.RequestError as e:
        print(f"Error de red o conexión al agregar producto: {e}")
        return None

async def update_product_in_ferremas_api(product_id: int, product_update: dict) -> Optional[Product]:
    """
    Actualiza un producto existente en la API de Ferremas.
    """
    url = f"{settings.FERREMAS_DB_API_URL}/products/{product_id}"
    headers = {"token": settings.FERREMAS_DB_API_TOKEN, "Content-Type": "application/json"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=headers, json=product_update)
            response.raise_for_status()
            return Product(**response.json())
    except httpx.HTTPStatusError as e:
        print(f"Error HTTP al actualizar producto: {e.response.status_code} - {e.response.text}")
        return None
    except httpx.RequestError as e:
        print(f"Error de red o conexión al actualizar producto: {e}")
        return None
# database.py contenido
# ... otro código ...

def fetch_product_data():
    # Tu código para obtener datos de productos va aquí
    pass # O la implementación real

def fetch_branch_data():
    # Tu código para obtener datos de sucursales va aquí
    pass

def fetch_seller_data():
    # Tu código para obtener datos de vendedores va aquí
    pass

# ... otro código ...