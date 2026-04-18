Sistema de Control de Paquetería 

Este proyecto es un software de consola diseñado para simular la gestión y el rastreo logístico de una empresa de paquetería. El propósito principal del sistema es digitalizar el ciclo de vida de un paquete desde el momento en que ingresa a la bodega, su tránsito en ruta, hasta su entrega final al destinatario.

El sistema garantiza la integridad de la información mediante validaciones estrictas y proporciona una interfaz interactiva para que los operadores puedan registrar envíos y consultar el estado (tracking) de los mismos en tiempo real.

Objetivos del Proyecto

Automatización: Reemplazar el registro manual de paquetes por un flujo digital controlado.
Trazabilidad: Permitir la búsqueda y actualización del estado logístico de cualquier paquete a través de un identificador único (ID).
Integridad de Datos: Prevenir errores de digitación por parte de los usuarios (como ingresar pesos negativos o caracteres inválidos) mediante la implementación de bloqueos lógicos.

Descripción del Proyecto

Este proyecto es una implementación en pseudocódigo desarrollada para la materia de Lógica de Programación.
Consiste en un sistema transaccional básico para el registro, actualización y seguimiento de paquetería, 
utilizando estructuras de datos estáticas (arreglos paralelos) para simular el almacenamiento en memoria.

Características y Lógica Implementada

El sistema opera a través de un menú interactivo en consola y cuenta con las siguientes funcionalidades y validaciones:
Registro de Envíos (Create): Ingreso de nuevos paquetes con generación automática de un Tracking ID autoincremental.
Validación de Entradas: Bloqueos lógicos (Repetir... Hasta Que) para evitar datos erróneos, como pesos negativos o nulos,
y opciones de menú inválidas.

Actualización de Estados (Update): Modificación del estado logístico del paquete (Bodega, Tránsito, Entregado) 
mediante un algoritmo de búsqueda lineal.
Consulta de Tracking (Read): Recuperación y visualización de los datos del paquete a partir de su ID.
Manejo de Excepciones: Prevención de errores lógicos como el desbordamiento de memoria (límite de MAX_PAQUETES)
 y notificaciones controladas cuando se busca un ID inexistente.

Herramientas Utilizadas

Lenguaje: Pseudocódigo estructurado.
Entorno de Desarrollo: PSeInt.

Instrucciones de Ejecución

Abrir el archivo .psc proporcionado en el entorno de PSeInt.
Iniciar la ejecución del algoritmo (botón verde de "Ejecutar" o tecla F9).
Utilizar el teclado numérico para navegar por las opciones del menú principal y seguir las instrucciones en pantalla.

Estructura de Datos

Para solventar la ausencia de bases de datos relacionales, la persistencia temporal se maneja a través de tres arreglos paralelos principales:
idPaquete[]: Almacena el identificador único (entero).
pesoPaquete[]: Almacena el peso físico del paquete (real).
estadoPaquete[]: Almacena el código de estado actual (1, 2 o 3).