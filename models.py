# ferremas_api/models.py
from pydantic import BaseModel, Field
from typing import Optional, List

class User(BaseModel):
    username: str
    password: str
    role: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    roles: List[str] = [] # Para manejar múltiples roles si fuera necesario

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    model: Optional[str] = None
    brand: Optional[str] = None
    code: Optional[str] = None
    stock: int
    category: str
    is_new_arrival: Optional[bool] = False
    is_promotion: Optional[bool] = False

class Branch(BaseModel):
    id: Optional[int] = None
    name: str
    address: str
    phone: str

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
