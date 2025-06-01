# ferremas_api/models.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List

# --- Modelos de usuario y autenticación ---

class User(BaseModel):
    username: str
    roles: List[str]  # Roles visibles (client, admin, etc.)
    # Campos opcionales adicionales si se necesitan:
    # email: Optional[EmailStr] = None
    # full_name: Optional[str] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    roles: List[str] = []

# --- Modelos principales de negocio ---

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
    email: EmailStr
    branch_id: int

# --- Modelos para pedidos y contacto ---

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class SingleOrder(BaseModel):
    client_username: str
    items: List[OrderItem]
    branch_id: int

class ContactMessage(BaseModel):
    client_name: str
    client_email: EmailStr
    subject: str
    message: str
    seller_id: Optional[int] = None

# --- Modelos para integración externa ---

class StripePayment(BaseModel):
    amount: float
    currency: str
    payment_method_id: str

class CurrencyConversion(BaseModel):
    amount: float
    from_currency: str
    to_currency: str
    converted_amount: float
