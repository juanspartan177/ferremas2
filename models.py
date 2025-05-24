# ferremas_api/models.py
from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    username: str
    roles: List[str] # Asumiendo que quieres que los roles sean públicos
    # Añade otros campos que quieras exponer del usuario (ej. email, full_name, etc.)
    # Por ejemplo:
    # email: Optional[str] = None
    # full_name: Optional[str] = None

class UserInDB(User): # UserInDB hereda de User
    hashed_password: str

# Modelos para la autenticación
class Token(BaseModel):
    access_token: str
    token_type: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    roles: List[str] = [] # Para manejar múltiples roles si fuera necesario

class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: str
    brand: str
    is_promotion: bool = False
    is_new_product: bool = False


class Branch(BaseModel):
    id: int
    name: str
    address: str
    city: str
    phone: str
    latitude: float
    longitude: float

class Seller(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    branch_id: int

class ContactMessage(BaseModel):
    client_name: str
    client_email: str
    subject: str
    message: str
    seller_id: Optional[int] = None

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class SingleOrder(BaseModel):
    client_username: str
    items: List[OrderItem] # Lista para permitir monoproducto o multiproducto
    branch_id: int
    
class StripePayment(BaseModel):
    amount: float
    currency: str
    payment_method_id: str # ID del método de pago de Stripe

class CurrencyConversion(BaseModel):
    amount: float
    from_currency: str
    to_currency: str
    converted_amount: float