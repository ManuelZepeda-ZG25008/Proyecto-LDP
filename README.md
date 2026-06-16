# Sistema de Control de Paquetería  
API REST para la gestión de clientes, paquetes y entregas de una empresa de envíos. Desarrollada en Python con FastAPI, siguiendo los principios de Domain-Driven Design (DDD) y SOLID.
 

## Integrantes
| Nombre | Carnet |
|--------|-------|
| Edwin Gerardo Vasquez Guerrero | VG23031 |
| Manuel Alexander Zepeda Grijalba | ZG25008 |
| Catherine Andre Argumedo | AB25013 |


---

## Objetivo
 El sistema centraliza el control de las operaciones básicas de una empresa de paquetería, permitiendo registrar clientes, administrar la información de los paquetes y dar seguimiento al estado de cada entrega desde que se programa hasta que se completa, su propósito es resolver la inconsistencia que surge cuando esta información se maneja de forma manual o dispersa, ofreciendo en su lugar una única fuente de verdad accesible mediante una API estandarizada.
<br>
Automatización: Reemplazar el registro manual de paquetes por un flujo digital controlado.
Trazabilidad: Permitir la búsqueda y actualización del estado logístico de cualquier paquete a través de un identificador único (ID).
Integridad de Datos: Prevenir errores de digitación por parte de los usuarios (como ingresar pesos negativos o caracteres inválidos) mediante la implementación de bloqueos lógicos.
<br>

## Tecnologías
| Herramienta | Uso |
|---|---|
| Python | Lenguaje principal |
| FastAPI | Framework HTTP |
| SQLite | Base de datos |
| Pytest | Pruebas unitarias |
| GitHub Actions | CI automatizado |
 
<br>

## Manejo de errores
 
El middleware global en `src/api/middleware/error_handler.py` captura todas las excepciones de dominio automáticamente. Los controladores no usan `try-except`.
 
| Excepción base | Código HTTP |
|---|---|
| `DomainValidationError` | 400 Bad Request |
| `ResourceNotFoundError` | 404 Not Found |
| `ResourceAlreadyExistsError` | 409 Conflict |
 
 <br>
 
## Instalación y ejecución
```bash
# 1. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate        # Linux / macOS
 
# 2. Instalar dependencias
pip install -r requirements.txt
 
# 3. Levantar el servidor
python -m uvicorn src.api.main:app --reload
```
 
La base de datos `paqueteria.db` se crea automáticamente al iniciar el servidor. No requiere configuración manual.
 
 
---
 
## Interfaz de pruebas (Swagger UI)
 
FastAPI genera automáticamente una interfaz de documentación interactiva basada en la especificación OpenAPI, accesible en `/docs` mientras el servidor está en ejecución. No requiere instalación ni configuración adicional.
 
Desde esta interfaz es posible:
 
✿ Visualizar todos los endpoints disponibles, agrupados por módulo (Clientes, Paquetes, Entregas)  
✿ Consultar el esquema exacto de cada DTO: qué campos requiere y qué formato devuelve  
✿ Ejecutar peticiones HTTP reales contra el servidor (crear, consultar, actualizar y eliminar registros) sin necesidad de herramientas externas como Postman  
✿ Observar en tiempo real los códigos de respuesta HTTP y los mensajes de error generados por el middleware ante datos inválidos, recursos no encontrados o duplicados  
*Para usarla: abrir el endpoint deseado, presionar **Try it out**, completar o pegar el cuerpo de la petición en formato JSON, y presionar **Execute**.*
 
<br>
 
## Pruebas
 
```bash
# Ejecutar todos los tests
python -m pytest tests/ -v
 
# Con reporte de cobertura
python -m pytest tests/ -v --cov=src
```
 
Las pruebas están organizadas por capa:
 
```
tests/
├── domain/       # Validaciones de entidades
├── application/  # Casos de uso y mappers
└── api/          # Endpoints HTTP
```
 
El pipeline de CI en `.github/workflows/pytest.yml` ejecuta las pruebas automáticamente en cada push a `main`.

