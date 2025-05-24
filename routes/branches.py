# ferremas_api/routes/branches.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from models import Branch, Seller, UserInDB
from database import fetch_branch_data, fetch_seller_data
from auth import has_roles

router = APIRouter()

@router.get("/branches", response_model=List[Branch], summary="Obtener listado de sucursales")
async def get_branches():
    """
    Recupera el listado completo de sucursales de FERREMAS.
    """
    branches = await fetch_branch_data()
    if branches is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo obtener el listado de sucursales")
    return branches

@router.get("/branches/{branch_id}", response_model=Branch, summary="Obtener detalles de una sucursal")
async def get_branch_by_id(branch_id: int):
    """
    Recupera los detalles de una sucursal específica por su ID.
    (Caso de uso: Como cliente, quiero poder mirar los detalles de una sucursal) [cite: 65]
    """
    branch = await fetch_branch_data(branch_id=branch_id)
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sucursal no encontrada")
    return branch[0] # fetch_branch_data devuelve una lista

@router.get("/branches/{branch_id}/sellers", response_model=List[Seller], summary="Obtener listado de vendedores por sucursal")
async def get_sellers_by_branch(branch_id: int, current_user: UserInDB = Depends(has_roles(["admin", "jefe_tienda"]))):
    """
    Recupera el listado de vendedores asignados a una sucursal específica.
    Requiere rol de 'admin' o 'jefe_tienda'.
    (Caso de uso: Como administrador de tienda, quiero poder ver mis vendedores) [cite: 65]
    """
    sellers = await fetch_seller_data(branch_id=branch_id)
    if sellers is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo obtener el listado de vendedores para la sucursal")
    return sellers

@router.get("/sellers/{seller_id}", response_model=Seller, summary="Obtener un vendedor identificable")
async def get_seller_by_id(seller_id: int, current_user: UserInDB = Depends(has_roles(["admin", "jefe_tienda", "bodega", "client"]))):
    """
    Recupera los detalles de un vendedor específico por su ID.
    Accesible por admin, jefe_tienda, bodega y clientes.
    """
    seller = await fetch_seller_data(seller_id=seller_id)
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendedor no encontrado")
    return seller[0]