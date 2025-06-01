from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Dict, Any, Optional
import httpx
from currency_converter import CurrencyConverter

from auth import authenticate_user, create_access_token, get_current_user, has_roles
from models import Token, User, SingleOrder, ContactMessage, StripePayment, CurrencyConversion, Product, Branch, Seller
from database import fetch_product_data, fetch_branch_data, fetch_seller_data
from routes import products, branches

app = FastAPI(
    debug=True,
    title="API de Integración de Ferremas",
    description="API para la integración de servicios de Ferremas, incluyendo productos, sucursales, pedidos, pagos y conversión de divisas.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir los routers de las rutas
app.include_router(products.router, prefix="/api/v1")
app.include_router(branches.router, prefix="/api/v1")

# --- Rutas de Autenticación ---
@app.post("/token", response_model=Token, summary="Obtener token de autenticación")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username, "roles": [user.roles]})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Rutas de Pedidos ---
@app.post("/api/v1/orders", status_code=status.HTTP_201_CREATED, summary="Colocar un pedido (monoproducto o multiproducto)")
async def place_order(order: SingleOrder, current_user: User = Depends(has_roles(["client"]))):
    for item in order.items:
        product_info = await fetch_product_data(product_id=item.product_id)
        if not product_info or product_info[0].stock < item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Producto con ID {item.product_id} no disponible o stock insuficiente.")
    print(f"Pedido recibido de {order.client_username} para la sucursal {order.branch_id}: {order.items}")
    return {"message": "Pedido colocado exitosamente", "order_details": order.model_dump()}

# --- Rutas de Contacto ---
@app.post("/api/v1/contact", status_code=status.HTTP_202_ACCEPTED, summary="Solicitud de contacto con un vendedor")
async def contact_seller(message: ContactMessage):
    print(f"Mensaje de contacto recibido de {message.client_name} ({message.client_email}):")
    print(f"Asunto: {message.subject}")
    print(f"Mensaje: {message.message}")
    if message.seller_id:
        seller_info = await fetch_seller_data(seller_id=message.seller_id)
        if seller_info:
            print(f"Dirigido al vendedor: {seller_info[0].name} ({seller_info[0].email})")
        else:
            print(f"Vendedor con ID {message.seller_id} no encontrado.")
    return {"message": "Su solicitud de contacto ha sido enviada."}

# --- Integración con Stripe (Pasarela de Pagos) ---
@app.post("/api/v1/payments/stripe", status_code=status.HTTP_200_OK, summary="Procesar pago con Stripe")
async def process_stripe_payment(payment: StripePayment, current_user: User = Depends(has_roles(["client", "service_account"]))):
    print(f"Simulando procesamiento de pago con Stripe para un monto de {payment.amount} {payment.currency}")
    return {"message": "Pago simulado procesado exitosamente con Stripe."}

# --- Integración con API de Conversión de Divisas ---
async def get_exchange_rate(from_currency: str, to_currency: str) -> Optional[float]:
    if from_currency.upper() == "CLP" and to_currency.upper() == "USD":
        return 0.00105
    elif from_currency.upper() == "USD" and to_currency.upper() == "CLP":
        return 950.0
    else:
        return None

@app.post("/api/v1/currencyConversion", response_model=CurrencyConversion, summary="Convertir divisas en tiempo real")
async def convert_currency(conversion_request: CurrencyConversion, current_user: User = Depends(has_roles(["client", "service_account"]))):
    exchange_rate = await get_exchange_rate(conversion_request.from_currency, conversion_request.to_currency)
    if exchange_rate is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo obtener la tasa de cambio para las monedas especificadas.")
    converted_amount = conversion_request.amount * exchange_rate
    return CurrencyConversion(
        amount=conversion_request.amount,
        from_currency=conversion_request.from_currency,
        to_currency=conversion_request.to_currency,
        converted_amount=converted_amount
    )