# ferremas_api/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Dict, Any
import httpx # Para simular llamadas a Stripe y Banco Central de Chile
from currency_converter import CurrencyConverter # Librería para conversión de divisas, si la usas

from auth import authenticate_user, create_access_token, get_current_user, has_roles
from models import Token, User, SingleOrder, ContactMessage, StripePayment, CurrencyConversion, Product, Branch, Seller
from database import fetch_product_data, fetch_branch_data, fetch_seller_data
from routes import products, branches # Importar los routers de rutas
from typing import Optional, List # Asegúrate de que Optional esté aquí
# main.py

from fastapi import FastAPI
# ... other imports ...

from routes import products # This imports the products module

app = FastAPI(
    debug=True,
)

# ... other app configurations ...

# Then, you include the router from the imported module
app.include_router(products.router, prefix="/api/v1")

# ... other main.py code ...
# ... otras importaciones
app = FastAPI(
    title="API de Integración de Ferremas",
    description="API para la integración de servicios de Ferremas, incluyendo productos, sucursales, pedidos, pagos y conversión de divisas.",
    version="2.0.0",
    docs_url="/docs", # URL para la documentación OpenAPI (Swagger UI) [cite: 51]
    redoc_url="/redoc" # URL para la documentación ReDoc
)

# Incluir los routers de las rutas
app.include_router(products.router, prefix="/api/v1")
app.include_router(branches.router, prefix="/api/v1")

# --- Rutas de Autenticación ---
@app.post("/token", response_model=Token, summary="Obtener token de autenticación")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para que los usuarios obtengan un token de acceso JWT.
    Requiere username y password.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Incluir el rol en los datos del token
    access_token = create_access_token(data={"sub": user.username, "roles": [user.roles]})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Rutas de Pedidos ---
@app.post("/api/v1/orders", status_code=status.HTTP_201_CREATED, summary="Colocar un pedido (monoproducto o multiproducto)")
async def place_order(order: SingleOrder, current_user: User = Depends(has_roles(["client"]))):
    """
    Permite a un cliente colocar un pedido de uno o varios productos.
    (Caso de uso: Como cliente, quiero poder realizar una compra) [cite: 65]
    """
    # Aquí iría la lógica para procesar el pedido, como:
    # 1. Validar stock de productos [cite: 46]
    # 2. Calcular el total del pedido
    # 3. Guardar el pedido en la base de datos (o simularlo)
    # 4. Integrar con el sistema de pagos (Stripe) [cite: 52]

    # Simulación de validación de productos y stock
    for item in order.items:
        product_info = await fetch_product_data(product_id=item.product_id)
        if not product_info or product_info[0].stock < item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Producto con ID {item.product_id} no disponible o stock insuficiente.")

    print(f"Pedido recibido de {order.client_username} para la sucursal {order.branch_id}: {order.items}")
    return {"message": "Pedido colocado exitosamente", "order_details": order.model_dump()}

# --- Rutas de Contacto ---
@app.post("/api/v1/contact", status_code=status.HTTP_202_ACCEPTED, summary="Solicitud de contacto con un vendedor")
async def contact_seller(message: ContactMessage):
    """
    Permite a los clientes enviar un mensaje para solicitar contacto con un vendedor.
    """
    # Aquí se simularía el envío de un correo electrónico o una notificación al vendedor
    # o a un sistema de CRM.
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
    """
    Procesa un pago utilizando la API de Stripe.
    Se requiere un rol de 'client' o 'service_account'.
    """
    # Aquí se realizaría la integración real con la API de Stripe[cite: 52, 53].
    # Por simplicidad, se simula una llamada exitosa.
    print(f"Simulando procesamiento de pago con Stripe para un monto de {payment.amount} {payment.currency}")
    # Ejemplo de cómo llamarías a la API de Stripe (pseudocódigo):
    # try:
    #     stripe.PaymentIntent.create(
    #         amount=int(payment.amount * 100), # Stripe espera centavos
    #         currency=payment.currency,
    #         payment_method=payment.payment_method_id,
    #         confirm=True,
    #         description="Compra en Ferremas"
    #     )
    #     return {"message": "Pago procesado exitosamente con Stripe."}
    # except stripe.error.StripeError as e:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "Pago simulado procesado exitosamente con Stripe."}


# --- Integración con API de Conversión de Divisas (Banco Central de Chile o similar) ---
# Se puede usar una librería como `CurrencyConverter` o hacer llamadas directas a una API.
# Para este ejemplo, usaremos una simulación o una librería simple si no hay una API gratuita y bien documentada
# para el BCCh fácil de integrar directamente.
# La documentación menciona que se puede usar otra API si es mejor[cite: 65].
# Para simplificar y dado que la API del BCCh puede requerir configuración más compleja,
# usaremos una simulación o una librería si es viable.
# Si la librería `CurrencyConverter` no es suficiente para divisas específicas,
# se necesitaría integrar con una API externa (como Free Currency API, Open Exchange Rates, etc.).

# Simulación de la API del Banco Central de Chile o similar
async def get_exchange_rate(from_currency: str, to_currency: str) -> Optional[float]:
    """
    Simula la obtención de la tasa de cambio de una API externa.
    En un entorno real, esto se integraría con la API del Banco Central de Chile [cite: 56]
    o una API de divisas externa.
    """
    # Ejemplo de URL para una API de divisas gratuita (reemplazar por una real si se usa)
    # response = await httpx.get(f"https://api.example.com/latest?from={from_currency}&to={to_currency}")
    # data = response.json()
    # return data["rates"][to_currency]

    # Simulación de tasas de cambio (ejemplo)
    if from_currency.upper() == "CLP" and to_currency.upper() == "USD":
        return 0.00105 # Aproximado
    elif from_currency.upper() == "USD" and to_currency.upper() == "CLP":
        return 950.0   # Aproximado
    else:
        return None # No se encontró la tasa de cambio

@app.post("/api/v1/currencyConversion", response_model=CurrencyConversion, summary="Convertir divisas en tiempo real")
async def convert_currency(conversion_request: CurrencyConversion, current_user: User = Depends(has_roles(["client", "service_account"]))):
    """
    Convierte una cantidad de una moneda a otra en tiempo real utilizando una API externa.
    Se requiere un rol de 'client' o 'service_account'.
    """
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