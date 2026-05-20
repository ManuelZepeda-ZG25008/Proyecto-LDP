Para dejar los controladores limpios y puristas, está prohibido usar try-catch en las rutas. En su lugar, dejé un Middleware Global en src/api/middleware/error_handler.py que captura los errores automáticamente.

En src/domain/exceptions.py creé tres excepciones madres. Cuando ustedes programen sus módulos, sus excepciones específicas deben heredar obligatoriamente de estas tres:

DomainValidationError -> El middleware la captura y devuelve un HTTP 400 Bad Request.

ResourceNotFoundError -> El middleware la captura y devuelve un HTTP 404 Not Found.

ResourceAlreadyExistsError -> El middleware la captura y devuelve un HTTP 409 Conflict.

 Ejemplo de cómo usarlo en sus módulos:
Si estás haciendo Paquetes, en tu archivo de excepciones o en tu lógica de aplicación definís tu error heredando de la base correspondiente:

from src.domain.exceptions import ResourceNotFoundError

class PackageNotFoundError(ResourceNotFoundError):
    \"\"\"Hereda de la base. El middleware ya sabe qué hacer con ella.\"\"\"
    pass

Cuando lances el error en tu caso de uso con un raise PackageNotFoundError("El paquete no existe, maje"), el sistema detendrá el flujo y le enviará al cliente un JSON fino con código 404 automáticamente. ¡No tenés que configurar nada en el API!


 3. El Paso a Paso para Crear tu CRUD (El Clonador)
Para armar Paquetes o Entregas, sigan este orden quirúrgico de adentro hacia afuera:

Paso A: El Dominio (src/domain/)
Entidad (domain/entities/): Creá tu clase pura en Python (ej. package.py). Meté las propiedades en el __init__ y añadí un método .validar() que lance un error hijo de DomainValidationError si mandan datos inválidos (como strings vacíos o IDs mal formados).

Contrato del Repositorio (domain/repositories/): Creá una clase abstracta que herede de ABC definiendo qué métodos va a ocupar tu lógica en la DB (save, get_by_id, get_all, delete). Aquí no se programa SQL, solo se definen las firmas de las funciones.

Paso B: La Infraestructura (src/infrastructure/persistence/)
El Repositorio Real: Creá tu archivo (ej. sqlite_package_repository.py) que implemente la interfaz abstracta que hiciste en el paso anterior.

Importá get_db_connection desde src/infrastructure/persistence/sqlite_connection.py.

Tirá tus queries de SQL puro con cursor.execute().

Usá INSERT OR REPLACE INTO... para manejar la creación y la actualización en una sola query fina.

Mapeo: Cuando saqués datos de la DB con fetchone() o fetchall(), acordate de reconstruir y retornar el objeto puro de dominio llamando a tu Entidad.

Paso C: La Aplicación (src/application/)
DTOs (application/dtos/): Creá tus esquemas de Pydantic para definir cómo entra la data en el JSON y cómo sale (PackageCreateDTO, PackageUpdateDTO, PackageResponseDTO).

Mapper (application/mappers/): Una clase con métodos estáticos (to_entity, to_response_dto) para convertir los DTOs en entidades de dominio y viceversa.

Casos de Uso (application/use_cases/): Creá las clases de ejecución de lógica de negocio (ej. CreatePackageUseCase). Estas clases reciben el Repositorio por el constructor (Inyección de Dependencias) y tienen un método .execute(). Aquí hacés las validaciones (ej. verificar si el ID ya existe antes de guardar, arrojando tus excepciones personalizadas).

Paso D: La API (src/api/)
Controlador (api/controllers/): Instanciá tu router con FastAPI (router = APIRouter(prefix="/packages", tags=["Paquetes"])).

Instanciá tu repositorio real en el archivo y pasáselo a los casos de uso.

Escribí tus endpoints (@router.post, @router.get, etc.). Tus endpoints deben ser cortitos: capturan el DTO, ejecutan el Caso de Uso y retornan la respuesta. ¡Cero try-except, socios!

Paso E: Enganchar en el Servidor
Cuando tengás listo tu controlador, andá a src/api/main.py, importá tu nuevo router y agregalo abajo del de clientes usando la línea:

Python
app.include_router(tu_nuevo_router)






 4. Comandos Útiles para el Entorno
Asegúrense de activar siempre el entorno virtual antes de levantar el changarro:

PowerShell
# 1. Activar el entorno virtual local (PowerShell)
.venv\\Scripts\\Activate.ps1

# 2. Levantar el servidor en modo desarrollo con auto-reload
uvicorn src.api.main:app --reload



---

##  5. La Base de Datos se crea Sola (Auto-sustentable)

 **NO tienen que crear ningún archivo de base de datos manualmente**, ni correr scripts de SQL en programas externos. El archivo `paqueteria.db` está en el `.gitignore` para no ensuciar el repositorio con datos de prueba de cada quien.

Cuando clonen el proyecto y ejecuten el comando `uvicorn src.api.main:app --reload`, FastAPI ejecutará un evento de `startup` que llama a la función `init_db()`. En ese preciso milisegundo, SQLite revisará si el archivo existe; si no está, **lo creará virgen en la raíz del proyecto y montará las tablas automáticamente**. Así que ustedes solo denle *play* al servidor y la base de datos se armará solita.


## 🧠 6. Reglas de Negocio del Dominio (El Estándar de Validación)

En el módulo de **Clientes** dejé sembradas reglas estrictas en la entidad de dominio (`src/domain/entities/client.py`). 

Estas son las reglas que apliqué y que sirven de ejemplo:

* **Validación de Correo:** El sistema no acepta correos falsos. Obligatoriamente comprueba de forma nativa que el string contenga un carácter `@` y un punto `.`. Si no los lleva, frena la operación.
* **Validación de Teléfono (Formato de El Salvador):** El número de teléfono se limpia de guiones (`-`) en tiempo de ejecución y se cuenta la cantidad de caracteres numéricos puros. **Debe tener un mínimo de 8 dígitos**. Si mandan un número incompleto (ej: `123-45`), el sistema lanza un error antes de tocar la base de datos.
* **Campos Obligatorios:** Tanto el `nombre` como el `apellido` y la `direccion` se limpian de espacios en blanco con `.strip()`. Si vienen vacíos o son puros espacios, el sistema los rebota inmediatamente.