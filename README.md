# ferremas2
main.py: Archivo principal de nuestra aplicación FastAPI.
config.py: Para manejar la configuración de la API (token de la base de datos, etc.).
auth.py: Contendrá la lógica de autenticación y autorización.
models.py: Definirá los modelos de datos (schemas) para las solicitudes y respuestas de la API.
database.py: Manejará la conexión y las operaciones con la API de la base de datos de Ferremas.
routes/: Carpeta para organizar las rutas de la API por módulos.
products.py: Rutas relacionadas con los productos.
branches.py: Rutas relacionadas con las sucursales.
.env: Archivo para variables de entorno (sensibles, como tokens).
.gitignore: Para especificar archivos y carpetas que Git debe ignorar.
README.md: Documentación del proyecto.


Explicación .config.py
Importa os y load_dotenv para trabajar con variables de entorno.
La clase Settings almacena las configuraciones.
FERREMAS_DB_API_TOKEN y FERREMAS_DB_API_URL son extraídos del archivo .env o usan los valores por defecto proporcionados en la documentación.
SECRET_KEY, ALGORITHM y ACCESS_TOKEN_EXPIRE_MINUTES son para la generación y validación de tokens JWT para la autenticación interna.

Explicación.env:
Aquí colocas tus variables de entorno. Es crucial no subir este archivo a tu repositorio público de Git, por eso lo incluimos en .gitignore.

Explicación models.py:
Define los esquemas de datos utilizando Pydantic, lo que permite la validación automática de solicitudes y respuestas de la API.
User, UserInDB, Token, TokenData son para el sistema de autenticación.
Product, Branch, Seller, ContactMessage, OrderItem, SingleOrder son para los modelos de datos específicos de Ferremas, basándose en los requerimientos del caso.
StripePayment y CurrencyConversion son modelos para la integración con Stripe y la API de conversión de divisas

Explicación auth.py:
pwd_context: Utiliza passlib para hashear y verificar contraseñas de forma segura.
oauth2_scheme: Define el esquema de seguridad OAuth2 con Bearer token.
FAKE_USERS_DB: Una "base de datos" en memoria para los usuarios y sus roles (Administrador, Mantenedor, Jefe de tienda, Bodega, Cliente, Cuentas de servicio). En un proyecto real, esto interactuaría con una base de datos persistente.
verify_password, get_user, authenticate_user: Funciones para manejar la autenticación de usuarios.
create_access_token: Genera un JSON Web Token (JWT) con la información del usuario (nombre de usuario y rol) y una fecha de expiración.
get_current_user: Es una dependencia que se utiliza en las rutas protegidas para extraer y validar el token JWT del encabezado de la solicitud, asegurando que el usuario esté autenticado.
has_role: Es una función decoradora que permite restringir el acceso a rutas específicas basándose en el rol del usuario autenticado. Esto implementa el control de acceso basado en roles (RBAC).

Explicación database.py:
Utiliza httpx para realizar solicitudes HTTP asíncronas a la "API Base de Datos FERREMAS" proporcionada.
Workspace_from_ferremas_api: Es una función auxiliar genérica para realizar llamadas GET a la API de Ferremas, incluyendo el token de autenticación requerido.
Workspace_product_data, Workspace_branch_data, Workspace_seller_data: Funciones específicas para obtener datos de productos, sucursales y vendedores, según los requerimientos.
add_product_to_ferremas_api, update_product_in_ferremas_api: Funciones para interactuar con la API de Ferremas para operaciones de escritura, en este caso, agregar y actualizar productos, necesarias para el rol de mantenedor.

carpeta routes
routes/__init__.py: vacío por el momento

Explicación routes/products.py:
Crea un APIRouter para organizar las rutas de productos.
@router.get("/products"): Permite obtener el catálogo completo de productos.
@router.get("/products/{product_id}"): Permite obtener un producto específico por su ID.
@router.get("/products/promotions"): Filtra y devuelve productos marcados como "promoción".
@router.get("/products/newArrivals"): Filtra y devuelve productos marcados como "novedades".
@router.post("/products"): Permite a "mantenedores" o "administradores" agregar productos nuevos. Protegido con Depends(has_role(["admin", "mantenedor"])).
@router.put("/products/{product_id}/markPromotion") y @router.put("/products/{product_id}/markNewArrival"): Permite a "mantenedores" o "administradores" marcar productos como promoción o novedad.

Explicación routes/branches.py:
APIRouter para las rutas de sucursales.
@router.get("/branches"): Obtiene el listado de sucursales.
@router.get("/branches/{branch_id}"): Obtiene detalles de una sucursal específica, cumpliendo el caso de uso "Como cliente, quiero poder mirar los detalles de una sucursal".
@router.get("/branches/{branch_id}/sellers"): Obtiene los vendedores de una sucursal. Protegido para "administrador" o "jefe de tienda". Cumple el caso de uso "Como administrador de tienda, quiero poder ver mis vendedores".
@router.get("/sellers/{seller_id}"): Obtiene un vendedor por su ID.

Explicación  main.py:
FastAPI(): Instancia la aplicación FastAPI. Se configuran el título, descripción y versión.
app.include_router(): Incluye los routers de productos y sucursales, organizando las rutas en módulos.
@app.post("/token"): Ruta para obtener un token JWT. Aquí los usuarios se autentican con nombre de usuario y contraseña, y si son válidos, se les devuelve un token de acceso.
@app.post("/api/v1/orders"): Permite a los clientes colocar pedidos. Incluye una simulación básica de validación de stock y cumple el caso de uso de realizar una compra.
@app.post("/api/v1/contact"): Permite a los clientes enviar mensajes de contacto.
@app.post("/api/v1/payments/stripe"): Integra la pasarela de pagos Stripe. Se simula la interacción con la API de Stripe.
@app.post("/api/v1/currencyConversion"): Integra la funcionalidad de conversión de divisas. Se simula la obtención de la tasa de cambio, pero se explica cómo se integraría con la API del Banco Central de Chile o una alternativa.
