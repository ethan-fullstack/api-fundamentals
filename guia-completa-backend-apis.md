# Guía Completa de Backend y APIs REST

## Tabla de Contenidos

1. [Conceptos Fundamentales del Backend](#1-conceptos-fundamentales-del-backend)
   - [¿Qué es el backend?](#11-qué-es-el-backend)
   - [Arquitectura cliente-servidor](#12-arquitectura-cliente-servidor)
   - [Comunicación entre aplicaciones](#13-comunicación-entre-aplicaciones)
2. [Fundamentos de las APIs](#2-fundamentos-de-las-apis)
   - [¿Qué es una API?](#21-qué-es-una-api)
   - [Tipos de APIs](#22-tipos-de-apis)
   - [Componentes clave de una API REST](#23-componentes-clave-de-una-api-rest)
3. [Métodos HTTP (Operaciones CRUD)](#3-métodos-http-operaciones-crud)
   - [Métodos principales](#31-métodos-principales)
   - [Métodos menos comunes](#32-métodos-menos-comunes)
   - [Relación entre métodos y CRUD](#33-relación-entre-métodos-y-crud)
4. [Estructura de una Respuesta HTTP](#4-estructura-de-una-respuesta-http)
   - [Partes de una respuesta](#41-partes-de-una-respuesta)
   - [Ejemplo de respuesta JSON](#42-ejemplo-de-respuesta-json)
   - [Errores comunes](#43-errores-comunes)
5. [Temas Adicionales Importantes](#5-temas-adicionales-importantes)
   - [Autenticación y Autorización](#51-autenticación-y-autorización)
   - [Rate Limiting y Throttling](#52-rate-limiting-y-throttling)
   - [Versionado de APIs](#53-versionado-de-apis)
   - [CORS](#54-cors-cross-origin-resource-sharing)
   - [Documentación de APIs](#55-documentación-de-apis)
   - [Testing de APIs](#56-testing-de-apis)
   - [Seguridad en APIs](#57-seguridad-en-apis)
6. [Fuentes de Consulta](#fuentes-de-consulta-especializadas-y-oficiales)

---

## 1. Conceptos Fundamentales del Backend

### 1.1 ¿Qué es el backend?

El backend representa la capa lógica y de procesamiento de una aplicación que opera fuera de la vista del usuario. Mientras el frontend se ocupa de lo que ves y con lo que interactúas directamente en tu pantalla, el backend es el cerebro que procesa información, toma decisiones, almacena datos y orquesta toda la lógica de negocio de una aplicación.

Para entender el rol del backend, imagina un restaurante. El comedor donde comes es el frontend: es bonito, accesible y diseñado para tu comodidad. Pero detrás de las puertas batientes está la cocina, el almacén, el sistema de inventario y el gerente coordinando todo. Esa es la función del backend: procesar pedidos, verificar ingredientes disponibles, calcular costos, coordinar con proveedores, todo sin que el cliente lo vea directamente.

#### Diferencias clave entre frontend y backend

El frontend ejecuta código en el navegador del usuario (cliente), usando principalmente HTML, CSS y JavaScript. Este código está limitado por razones de seguridad: no puede acceder directamente a bases de datos, no puede realizar operaciones sensibles como procesar pagos, y está expuesto a cualquiera que inspeccione el código fuente de la página.

El backend, por contraste, ejecuta código en servidores que controlas tú o tu organización. Puede estar escrito en múltiples lenguajes como Python, Java, Node.js, Go, Ruby, PHP o C#. Este código tiene acceso completo a recursos sensibles: puede conectarse a bases de datos, realizar cálculos complejos, comunicarse con servicios externos, procesar pagos, y mantener secretos como claves de API que nunca deberían ser visibles para los usuarios.

#### Componentes típicos del backend

Los componentes típicos del backend forman un ecosistema interconectado:

**El servidor** es el programa que escucha solicitudes entrantes y las procesa. Cuando digo "servidor", me refiero tanto al hardware físico o virtual donde corre tu aplicación, como al software servidor que maneja las conexiones HTTP (como Nginx, Apache, o servidores incorporados en frameworks como Express o Flask).

**La base de datos** es el sistema de almacenamiento persistente donde guardas información que debe sobrevivir más allá de una sesión de usuario o un reinicio del servidor. Existen bases de datos relacionales como PostgreSQL, MySQL y SQL Server que organizan datos en tablas con relaciones definidas, y bases de datos NoSQL como MongoDB, Redis y Cassandra que ofrecen modelos de datos más flexibles para casos específicos.

**Las APIs** (Application Programming Interfaces) son las interfaces que expones para que otros sistemas o tu propio frontend puedan comunicarse con tu backend. Piensa en ellas como los meseros del restaurante: toman pedidos en un formato específico, los llevan a la cocina, y traen de vuelta los resultados.

**El sistema de autenticación y autorización** verifica quién es el usuario (autenticación) y qué permisos tiene (autorización). Esto puede incluir manejo de sesiones, tokens JWT, OAuth para inicio de sesión con servicios externos, y sistemas complejos de roles y permisos.

#### Ejemplos de backends en sistemas reales

**Sistema bancario:** Cuando consultas tu saldo, el frontend envía una solicitud autenticada al backend. El backend verifica tu identidad mediante tu token de sesión, consulta la base de datos para obtener tus movimientos, calcula el saldo actual considerando débitos y créditos, aplica las reglas de negocio (como intereses o comisiones), formatea la respuesta y la envía de vuelta. Todo esto sucede en milisegundos, pero involucra múltiples capas de seguridad, validaciones y procesamiento.

**Aplicación de clima:** El backend actúa como intermediario inteligente. Cuando solicitas el clima de tu ciudad, el backend no genera esos datos por sí mismo. En cambio, consulta servicios externos especializados como OpenWeatherMap o Weather.gov, cachea los resultados para no hacer solicitudes repetitivas innecesarias, posiblemente enriquece los datos con información adicional (como índice UV o recomendaciones de vestimenta), y te devuelve una respuesta optimizada. Esto protege tus claves de API, reduce costos y mejora el rendimiento.

**Tienda online:** Tiene uno de los backends más complejos. Debe manejar catálogos de productos con inventario en tiempo real, procesar carritos de compra manteniendo consistencia cuando múltiples usuarios intentan comprar el mismo artículo limitado, integrar con pasarelas de pago de forma segura, coordinar con sistemas de envío, generar facturas, enviar notificaciones por email, manejar devoluciones, y mantener un historial completo de pedidos. Cada una de estas operaciones requiere lógica de negocio sofisticada que solo puede existir de forma segura en el backend.

### 1.2 Arquitectura cliente-servidor

La arquitectura cliente-servidor es el patrón fundamental que sustenta la web moderna. En su esencia, divide las responsabilidades en dos roles claramente definidos: el cliente solicita servicios y el servidor los proporciona.

#### El flujo de comunicación

El flujo de comunicación sigue un patrón de solicitud-respuesta. El cliente, típicamente un navegador web o una aplicación móvil, inicia la comunicación enviando una solicitud (request) al servidor. Esta solicitud viaja a través de la red usando el protocolo HTTP o HTTPS, llevando información sobre qué recurso se necesita, qué acción se quiere realizar, y cualquier dato adicional necesario.

El servidor recibe esta solicitud, la procesa ejecutando la lógica correspondiente (que puede incluir consultar bases de datos, realizar cálculos, o comunicarse con otros servicios), y construye una respuesta (response). Esta respuesta incluye un código de estado indicando si la operación fue exitosa, encabezados con metadatos, y típicamente un cuerpo con los datos solicitados, usualmente en formato JSON.

#### Ejemplo concreto del intercambio HTTP

Imagina que estás navegando una tienda online y haces clic en un producto. Tu navegador construye una solicitud HTTP GET que se ve así:

```http
GET /api/products/42 HTTP/1.1
Host: www.tienda.com
User-Agent: Mozilla/5.0
Accept: application/json
Authorization: Bearer eyJhbGc...
```

Esta solicitud viaja a través de internet hasta el servidor de la tienda. El servidor la recibe, verifica tu token de autorización, consulta la base de datos para obtener la información del producto con ID 42, y construye una respuesta:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=3600

{
  "id": 42,
  "name": "Laptop XYZ",
  "price": 899.99,
  "stock": 15
}
```

#### Puertos y protocolos

Un puerto es como el número de apartamento en un edificio: la dirección IP te lleva al edificio (el servidor), pero el puerto te dice exactamente a qué aplicación dentro de ese servidor dirigirte. Por convención, el tráfico HTTP usa el puerto 80 y HTTPS usa el puerto 443, aunque los desarrolladores pueden configurar sus aplicaciones para escuchar en cualquier puerto disponible.

**HTTP** (Hypertext Transfer Protocol) es el protocolo de comunicación que define cómo se estructuran y transmiten los mensajes entre clientes y servidores. Es un protocolo sin estado, lo que significa que cada solicitud es independiente y el servidor no mantiene información sobre solicitudes anteriores por defecto. Esto simplifica el diseño pero requiere mecanismos adicionales como cookies o tokens para mantener sesiones de usuario.

**HTTPS** es HTTP sobre una capa de seguridad (SSL/TLS). Encripta toda la comunicación entre cliente y servidor, protegiendo datos sensibles de ser interceptados. Cuando ves el candado en tu navegador, significa que estás usando HTTPS. Esto es especialmente crítico para cualquier aplicación que maneje información personal, contraseñas, o datos financieros. Hoy en día, HTTPS se considera obligatorio para prácticamente todas las aplicaciones web modernas, tanto por seguridad como porque los navegadores y motores de búsqueda penalizan sitios que no lo usan.

### 1.3 Comunicación entre aplicaciones

Cuando diferentes sistemas necesitan comunicarse, requieren un lenguaje común. Esto involucra tanto el protocolo (las reglas de comunicación) como el formato de datos (cómo se estructuran los datos intercambiados).

#### El concepto de protocolo

El concepto de protocolo es similar a las reglas de etiqueta en una conversación. Define quién habla primero, cómo se estructura cada mensaje, qué respuestas son apropiadas, y cómo se maneja una conversación fallida. HTTP es un protocolo; WebSocket (para comunicación bidireccional en tiempo real) es otro; gRPC (usado por Google para comunicación entre microservicios) es otro más. Cada protocolo tiene ventajas y desventajas para diferentes casos de uso.

#### JSON como estándar de intercambio

JSON (JavaScript Object Notation) se ha convertido en el formato estándar de facto para el intercambio de datos en aplicaciones web modernas. Su popularidad se debe a varias razones fundamentales.

Primero, es altamente legible para humanos. Si abres un archivo JSON, inmediatamente puedes entender su estructura:

```json
{
  "usuario": {
    "nombre": "Ana García",
    "edad": 28,
    "email": "ana@ejemplo.com",
    "activo": true,
    "roles": ["usuario", "editor"],
    "preferencias": {
      "idioma": "es",
      "notificaciones": true
    }
  }
}
```

Segundo, JSON es extremadamente fácil de parsear y generar en prácticamente todos los lenguajes de programación modernos. JavaScript lo soporta nativamente (de hecho, JSON viene de JavaScript), Python tiene el módulo `json` en su biblioteca estándar, Java tiene múltiples bibliotecas como Jackson y Gson, y así sucesivamente.

Tercero, JSON es ligero. No tiene la verbosidad de XML con sus etiquetas de apertura y cierre. Esto significa menos bytes transmitidos por la red, lo que se traduce en transferencias más rápidas y menor uso de ancho de banda.

#### Alternativas: XML y YAML

**XML** (eXtensible Markup Language) fue el estándar anterior y todavía se usa en sistemas empresariales heredados, servicios SOAP, y configuraciones donde la validación estricta mediante esquemas es crucial:

```xml
<usuario>
  <nombre>Ana García</nombre>
  <edad>28</edad>
  <email>ana@ejemplo.com</email>
  <activo>true</activo>
</usuario>
```

XML es más verboso. Cada elemento necesita etiquetas de apertura y cierre. Sin embargo, XML tiene ventajas: soporta namespaces para evitar conflictos de nombres, tiene un rico ecosistema de herramientas de validación (XML Schema, DTD), y puede manejar datos más complejos con atributos y contenido mixto.

**YAML** (YAML Ain't Markup Language) es popular en archivos de configuración, especialmente en herramientas DevOps como Docker Compose, Kubernetes, y Ansible. Es aún más legible que JSON porque usa indentación en lugar de llaves:

```yaml
usuario:
  nombre: Ana García
  edad: 28
  email: ana@ejemplo.com
  activo: true
  roles:
    - usuario
    - editor
```

Sin embargo, para APIs web, JSON domina porque es el formato más eficiente para la comunicación cliente-servidor en aplicaciones web, especialmente cuando JavaScript está involucrado en el frontend.

---

## 2. Fundamentos de las APIs

### 2.1 ¿Qué es una API?

Una API (Application Programming Interface) es fundamentalmente un contrato de comunicación entre diferentes piezas de software. Es una especificación que define cómo un programa puede solicitar servicios de otro programa, qué datos debe proporcionar, y qué puede esperar recibir a cambio.

#### Las APIs como contratos

Las APIs como contratos establecen expectativas claras. Cuando una API documenta que tiene un endpoint `/usuarios/{id}` que responde con un objeto JSON conteniendo nombre, email y fecha de registro, está haciendo una promesa. Los desarrolladores que usan esa API pueden confiar en esa estructura, construir su código basándose en ella, y esperar que funcione consistentemente. Si la API cambia ese contrato sin aviso, rompe todas las aplicaciones que dependen de ella.

#### APIs locales vs APIs web

Una API local es una interfaz dentro del mismo proceso o sistema. Por ejemplo, cuando usas la clase `ArrayList` en Java o el módulo `datetime` en Python, estás usando una API local. Estas APIs definen métodos y funciones que puedes llamar directamente en tu código.

Las APIs web, por contraste, operan sobre redes. Tu código hace solicitudes HTTP a un servidor remoto y recibe respuestas. Esto introduce complejidad adicional: latencia de red, posibles fallas de conexión, necesidad de autenticación, límites de tasa (rate limiting), y consideraciones de formato de datos. Sin embargo, las APIs web permiten que aplicaciones completamente separadas, escritas en diferentes lenguajes y ejecutándose en diferentes sistemas operativos, se comuniquen efectivamente.

#### Casos cotidianos de uso

**Aplicaciones de clima:** Cuando abres una aplicación de clima en tu teléfono, esa app no genera pronósticos del tiempo por sí misma. En cambio, hace una solicitud a una API de clima como la de OpenWeatherMap:

```
GET https://api.openweathermap.org/data/2.5/weather?q=Madrid&appid=TU_CLAVE
```

La API responde con datos estructurados sobre temperatura actual, humedad, velocidad del viento, y pronóstico. Tu aplicación entonces formatea estos datos de manera atractiva para mostrártelos.

**Aplicaciones de mapas:** Son maestros en el uso de APIs. Google Maps ofrece múltiples APIs: una para mostrar mapas interactivos, otra para geocodificación (convertir direcciones en coordenadas), otra para direcciones de navegación, otra para lugares cercanos. Una aplicación de delivery puede usar todas estas APIs simultáneamente: geocodifica la dirección del restaurante y del cliente, calcula la ruta óptima, muestra un mapa en tiempo real, y encuentra restaurantes cercanos a tu ubicación.

**Inicio de sesión con servicios externos (OAuth):** Es quizás el ejemplo más sofisticado de APIs trabajando juntas. Cuando haces clic en "Iniciar sesión con Google" en una aplicación, se desencadena una compleja danza de redirecciones y llamadas de API. Tu aplicación te redirige a Google, donde inicias sesión. Google te pregunta si permites que la aplicación acceda a tu información básica. Si aceptas, Google redirige de vuelta a la aplicación con un código temporal. La aplicación intercambia ese código por un token de acceso haciendo una solicitud de API segura a Google. Finalmente, la aplicación usa ese token para hacer otra llamada de API y obtener tu información de perfil. Todo esto sucede en segundos, pero involucra múltiples APIs trabajando en conjunto con protocolos de seguridad sofisticados.

### 2.2 Tipos de APIs

El ecosistema de APIs web ha evolucionado a través de diferentes paradigmas, cada uno diseñado para resolver problemas específicos.

#### REST (Representational State Transfer)

REST no es técnicamente un protocolo sino un estilo arquitectónico. Fue definido por Roy Fielding en su tesis doctoral del año 2000 y desde entonces se ha convertido en el enfoque dominante para diseñar APIs web. REST se basa en varios principios fundamentales.

El principio de recursos significa que todo en tu API es un "recurso" identificable. Un usuario es un recurso, un producto es un recurso, un pedido es un recurso. Cada recurso tiene una URL única, como `/usuarios/123` o `/productos/456`. Los recursos se manipulan usando los métodos HTTP estándar: GET para leer, POST para crear, PUT o PATCH para actualizar, DELETE para eliminar.

REST es sin estado (stateless), lo que significa que cada solicitud del cliente al servidor debe contener toda la información necesaria para entender y procesar esa solicitud. El servidor no mantiene información de sesión sobre el cliente entre solicitudes. Esto mejora la escalabilidad porque cualquier servidor puede manejar cualquier solicitud sin necesidad de compartir estado con otros servidores.

La interfaz uniforme de REST simplifica la arquitectura. Si entiendes cómo funciona un endpoint REST, entiendes cómo funcionan todos. Siempre usas los mismos métodos HTTP, los mismos códigos de estado, los mismos patrones de URL. Esta consistencia reduce la curva de aprendizaje y hace que las APIs sean más predecibles.

#### SOAP (Simple Object Access Protocol)

SOAP es un protocolo más antiguo y formal que REST. SOAP usa XML exclusivamente y define un sobre (envelope) estricto para todos los mensajes. Un mensaje SOAP tiene una estructura definida con un encabezado opcional y un cuerpo obligatorio. SOAP tiene especificaciones detalladas para seguridad (WS-Security), transacciones, y mensajería confiable.

SOAP se usa todavía en sistemas empresariales grandes, especialmente en sectores como finanzas y gobierno donde los estándares formales y la validación estricta son cruciales. Sin embargo, su complejidad y verbosidad han hecho que REST lo supere en popularidad para nuevos desarrollos web.

#### GraphQL

GraphQL es un lenguaje de consulta y tiempo de ejecución para APIs desarrollado por Facebook y liberado como código abierto en 2015. GraphQL aborda varios problemas específicos de REST. En REST, a menudo enfrentas el problema de obtener demasiados datos (over-fetching) o muy pocos (under-fetching). Si necesitas solo el nombre y email de un usuario, un endpoint REST típico podría devolverte toda la información del usuario de todas formas. Si necesitas información de un usuario y sus últimos posts, podrías tener que hacer múltiples solicitudes a diferentes endpoints.

GraphQL permite a los clientes especificar exactamente qué datos necesitan en una sola solicitud:

```graphql
query {
  usuario(id: "123") {
    nombre
    email
    posts(limite: 5) {
      titulo
      fecha
    }
  }
}
```

Esta consulta obtiene solo el nombre y email del usuario, junto con el título y fecha de sus últimos 5 posts, todo en una sola solicitud. GraphQL es particularmente poderoso para aplicaciones móviles donde minimizar el número de solicitudes y la cantidad de datos transferidos es crucial para la batería y el rendimiento.

#### Por qué REST domina el desarrollo web

REST domina el desarrollo web por varias razones pragmáticas. Es simple de entender y no requiere herramientas especiales. Puedes probar un endpoint REST directamente desde tu navegador o con herramientas simples como curl. Usa HTTP estándar, por lo que todas las herramientas y bibliotecas HTTP existentes funcionan inmediatamente. El caching HTTP funciona naturalmente con REST. Es fácil de escalar porque es sin estado. Y existe un ecosistema masivo de herramientas, documentación y experiencia comunitaria alrededor de REST.

### 2.3 Componentes clave de una API REST

Una API REST bien diseñada sigue patrones consistentes que hacen que sea intuitiva de usar.

#### Recursos

Los recursos son los sustantivos de tu API. Representan entidades en tu sistema. En una aplicación de blog, tus recursos podrían ser usuarios, posts, comentarios y categorías. En una tienda, podrían ser productos, órdenes, clientes y pagos. Los recursos se nombran usando sustantivos en plural: `/usuarios`, `/productos`, `/ordenes`.

#### Endpoints y rutas

Los endpoints son las URLs específicas que expones para interactuar con tus recursos. Un endpoint típico sigue un patrón jerárquico. `/usuarios` representa la colección completa de usuarios. `/usuarios/123` representa un usuario específico con ID 123. `/usuarios/123/pedidos` representa los pedidos de ese usuario específico. Esta jerarquía hace que las relaciones entre recursos sean claras y navegables.

Los endpoints pueden incluir parámetros de consulta para filtrar, paginar u ordenar resultados. Por ejemplo, `/productos?categoria=electronicos&orden=precio&limite=20` obtiene 20 productos electrónicos ordenados por precio. La diferencia clave es que los parámetros de ruta (como el ID en `/usuarios/123`) identifican recursos específicos, mientras que los parámetros de consulta modifican cómo se recupera o filtra un recurso.

#### Verbos o métodos HTTP

Los verbos o métodos HTTP definen qué acción quieres realizar sobre un recurso. Esta combinación de URL (recurso) y método HTTP (acción) es el corazón de REST. Algunos ejemplos ilustrativos:

- GET `/productos` obtiene una lista de todos los productos
- GET `/productos/42` obtiene el producto específico con ID 42
- POST `/productos` con un cuerpo JSON crea un nuevo producto
- PUT `/productos/42` con un cuerpo JSON actualiza completamente el producto 42
- PATCH `/productos/42` con un cuerpo JSON actualiza parcialmente el producto 42 (solo los campos enviados)
- DELETE `/productos/42` elimina el producto 42

Esta separación entre recurso y acción es poderosa porque la misma URL puede tener diferentes significados dependiendo del método HTTP usado. `/usuarios/5` con GET obtiene información del usuario, con PUT actualiza ese usuario, y con DELETE lo elimina.

#### Códigos de estado

Los códigos de estado comunican el resultado de una solicitud. Son números de tres dígitos agrupados en rangos:

- **2xx** indican éxito
- **3xx** indican redirecciones
- **4xx** indican errores del cliente (solicitud malformada, no autorizado, recurso no encontrado)
- **5xx** indican errores del servidor

Los códigos más comunes son:

- **200 OK** para solicitudes exitosas
- **201 Created** cuando se crea un nuevo recurso exitosamente
- **204 No Content** para operaciones exitosas sin contenido de respuesta (común con DELETE)
- **400 Bad Request** cuando la solicitud está malformada
- **401 Unauthorized** cuando se requiere autenticación pero no se proporcionó o es inválida
- **403 Forbidden** cuando estás autenticado pero no tienes permisos
- **404 Not Found** cuando el recurso solicitado no existe
- **500 Internal Server Error** cuando algo falla en el servidor
- **503 Service Unavailable** cuando el servidor está temporalmente no disponible

#### Headers y body

Headers y body son las dos formas principales de enviar información en solicitudes y respuestas. Los headers son metadatos sobre la solicitud o respuesta. Headers comunes incluyen:

- **Content-Type** especifica el formato del cuerpo (usualmente `application/json`)
- **Authorization** lleva credenciales (típicamente un token Bearer)
- **Accept** indica qué formatos puede procesar el cliente
- **Cache-Control** controla el comportamiento de caching
- **Content-Length** indica el tamaño del cuerpo

El body es donde van los datos reales. En una solicitud POST o PUT, el body contiene el recurso que estás creando o actualizando. En una respuesta, el body contiene los datos solicitados o información sobre el resultado de la operación.

---

## 3. Métodos HTTP (Operaciones CRUD)

### 3.1 Métodos principales

Los métodos HTTP principales mapean elegantemente a las operaciones CRUD que realizas sobre datos.

#### GET - Obtener recursos

GET es para obtener recursos sin modificarlos. GET debe ser seguro (no causar efectos secundarios) e idempotente (hacer la misma solicitud múltiples veces produce el mismo resultado). Cuando visitas una página web, tu navegador hace solicitudes GET para obtener el HTML, CSS, JavaScript e imágenes. Las solicitudes GET no deben tener body; todos los parámetros van en la URL como parámetros de consulta.

Un ejemplo de uso avanzado de GET es la paginación. Para una API que devuelve miles de productos, quieres obtenerlos en páginas:

```
GET /productos?pagina=2&limite=50
```

Obtiene productos 51-100. La respuesta típicamente incluye metadatos de paginación:

```json
{
  "productos": [...],
  "paginacion": {
    "paginaActual": 2,
    "totalPaginas": 45,
    "totalItems": 2234,
    "itemsPorPagina": 50
  }
}
```

#### POST - Crear nuevos recursos

POST es para crear nuevos recursos. POST no es idempotente porque hacer la misma solicitud múltiples veces típicamente crea múltiples recursos. Cuando haces POST a `/usuarios` con datos de un nuevo usuario, el servidor crea ese usuario, le asigna un ID único, y típicamente responde con código 201 Created e incluye el recurso recién creado en el body con su nuevo ID. El header `Location` a menudo contiene la URL del recurso recién creado: `Location: /usuarios/789`.

Un patrón importante es que POST a una colección (`/productos`) crea un nuevo item en esa colección, pero POST a un recurso específico puede tener otros significados específicos de dominio. Por ejemplo, `POST /ordenes/123/pagar` podría procesar el pago de una orden existente.

#### PUT - Actualizar completamente

PUT es para actualizar completamente un recurso existente. PUT es idempotente: hacer la misma solicitud PUT múltiples veces produce el mismo resultado. Si haces `PUT /usuarios/5` con un objeto usuario completo, estás diciendo "reemplaza el usuario 5 con exactamente este objeto". Esto significa que si omites campos, esos campos se eliminarían o establecerían en valores por defecto.

Por ejemplo, si el usuario 5 tiene `nombre`, `email`, `telefono` y `direccion`, pero tu solicitud PUT solo incluye `nombre` y `email`, después de la actualización, `telefono` y `direccion` ya no existirían (o estarían en null). Por esta razón, PUT requiere que envíes el recurso completo.

#### PATCH - Actualizar parcialmente

PATCH es para actualizaciones parciales. PATCH es más flexible que PUT porque solo necesitas enviar los campos que quieres cambiar. Si quieres cambiar solo el email de un usuario, puedes hacer `PATCH /usuarios/5` con body `{"email": "nuevo@email.com"}`, y todos los demás campos del usuario permanecen sin cambios. Esto es más eficiente y menos propenso a errores.

PATCH también es idempotente en la mayoría de implementaciones, aunque técnicamente el estándar HTTP permite operaciones PATCH no idempotentes. En la práctica, la mayoría de APIs tratan PATCH como idempotente.

#### DELETE - Eliminar recursos

DELETE es para eliminar recursos. DELETE es idempotente: eliminar un recurso que ya no existe típicamente devuelve el mismo resultado (404 Not Found o 204 No Content) que eliminarlo exitosamente por primera vez. Una solicitud DELETE exitosa típicamente devuelve 204 No Content sin body, o 200 OK con algún mensaje de confirmación.

Algunos sistemas implementan eliminación lógica (soft delete) donde el recurso no se elimina realmente de la base de datos sino que se marca como eliminado. En estos casos, GET al recurso eliminado devuelve 404, pero el recurso aún existe internamente y puede ser restaurado por administradores.

### 3.2 Métodos menos comunes

Existen métodos HTTP adicionales que se usan en situaciones específicas.

#### OPTIONS

OPTIONS se usa para descubrir qué métodos HTTP están permitidos en un endpoint. Un cliente puede hacer `OPTIONS /usuarios/5` y el servidor responde con un header `Allow: GET, PUT, PATCH, DELETE` indicando qué operaciones soporta. OPTIONS es crucial en CORS (Cross-Origin Resource Sharing) donde los navegadores hacen automáticamente una solicitud OPTIONS preflight antes de ciertos tipos de solicitudes cross-origin para verificar si el servidor permite la operación.

#### HEAD

HEAD es idéntico a GET excepto que el servidor no devuelve el body, solo los headers. Esto es útil para verificar si un recurso existe sin descargar todo su contenido, o para obtener metadatos como la fecha de última modificación sin transferir el recurso completo. Por ejemplo, para verificar si un archivo grande ha cambiado, puedes hacer HEAD y comparar el header `Last-Modified` o `ETag` con tu versión cacheada, evitando descargar el archivo completo si no ha cambiado.

#### CONNECT

CONNECT establece un túnel hacia el servidor identificado por el recurso objetivo. Se usa principalmente en proxy servers para establecer conexiones SSL/TLS (HTTPS) a través del proxy.

#### TRACE

TRACE realiza una prueba de mensaje de loop-back junto con la ruta al recurso objetivo. Se usa para debugging, pero está típicamente deshabilitado por razones de seguridad porque puede revelar información sensible.

### 3.3 Relación entre métodos y CRUD

La correspondencia entre operaciones CRUD (Create, Read, Update, Delete) y métodos HTTP es directa pero tiene matices importantes.

| CRUD   | Método HTTP | Ejemplo |
|--------|-------------|---------|
| Create | POST        | `POST /usuarios` |
| Read   | GET         | `GET /usuarios/5` |
| Update | PUT / PATCH | `PUT /usuarios/5` o `PATCH /usuarios/5` |
| Delete | DELETE      | `DELETE /usuarios/5` |

**Create** mapea a POST, pero también puede involucrar PUT. En algunos diseños de API, puedes usar PUT para crear un recurso cuando el cliente especifica el ID: `PUT /usuarios/nuevo-id-especifico`. Esto es menos común pero útil en sistemas donde los IDs son UUIDs generados por el cliente o tienen significado de negocio específico.

**Read** mapea a GET. Esta es la correspondencia más directa y simple.

**Update** mapea tanto a PUT como a PATCH, con la distinción que ya discutimos: PUT para reemplazar completamente, PATCH para actualizar parcialmente. En la práctica, PATCH es más común porque es más conveniente y menos propenso a errores.

**Delete** mapea directamente a DELETE, aunque como mencioné, la implementación subyacente podría ser eliminación física o lógica.

Es importante entender que mientras CRUD describe operaciones de datos, los métodos HTTP describen la intención semántica de una solicitud. A veces necesitas operaciones que no mapean limpiamente a CRUD. Por ejemplo, "enviar un email" o "procesar un pago" son acciones, no operaciones CRUD. Para estos casos, hay diferentes enfoques de diseño.

Un enfoque es usar POST a un endpoint que representa la acción: `POST /emails/enviar` o `POST /pagos/procesar`. Otro enfoque más RESTful es modelar la acción como un recurso: en lugar de "enviar email", creas un recurso "envío de email" con `POST /envios-email`. En lugar de "procesar pago", creas un recurso "transacción de pago" con `POST /transacciones`.

---

## 4. Estructura de una Respuesta HTTP

### 4.1 Partes de una respuesta

Cada respuesta HTTP tiene una estructura específica que transporta tanto el resultado como metadatos sobre ese resultado.

#### El código de estado

El código de estado es lo primero que examinas. Está en la primera línea de la respuesta HTTP: `HTTP/1.1 200 OK`. Este código te dice inmediatamente si necesitas procesar datos exitosos, manejar una redirección, tratar con un error del cliente, o lidiar con un fallo del servidor.

**Códigos 2xx (Éxito):**
- **200 OK:** El más común, usado para GET exitosos y otras operaciones exitosas con contenido de respuesta
- **201 Created:** Indica que se creó un nuevo recurso, típicamente en respuesta a POST
- **202 Accepted:** Indica que la solicitud fue aceptada pero el procesamiento aún no está completo, útil para operaciones asíncronas de larga duración
- **204 No Content:** Indica éxito sin cuerpo de respuesta, común con DELETE

**Códigos 3xx (Redirección):**
- **301 Moved Permanently:** Indica que el recurso se movió permanentemente a una nueva URL (incluida en el header `Location`)
- **302 Found / 307 Temporary Redirect:** Indican una redirección temporal
- **304 Not Modified:** El servidor dice "el recurso no ha cambiado desde que lo solicitaste la última vez, usa tu copia cacheada", ahorrando ancho de banda

**Códigos 4xx (Error del cliente):**
- **400 Bad Request:** La solicitud está malformada o contiene datos inválidos
- **401 Unauthorized:** Se requiere autenticación pero no se proporcionó o las credenciales son inválidas
- **403 Forbidden:** Estás autenticado pero no tienes permisos para este recurso
- **404 Not Found:** El recurso solicitado no existe
- **405 Method Not Allowed:** El método HTTP no está soportado para este endpoint
- **409 Conflict:** Un conflicto con el estado actual del recurso, común cuando intentas crear un recurso que ya existe
- **422 Unprocessable Entity:** La solicitud está bien formada pero contiene errores semánticos (como validación de negocio fallida)
- **429 Too Many Requests:** Has excedido los límites de tasa

**Códigos 5xx (Error del servidor):**
- **500 Internal Server Error:** Genérico: algo falló en el servidor pero no hay más detalles específicos
- **502 Bad Gateway:** El servidor actuando como proxy o gateway recibió una respuesta inválida del servidor upstream
- **503 Service Unavailable:** El servidor está temporalmente no disponible, típicamente por mantenimiento o sobrecarga
- **504 Gateway Timeout:** Un gateway o proxy no recibió respuesta a tiempo del servidor upstream

#### Headers importantes

Los headers transportan metadatos cruciales:

**Content-Type:** Especifica el tipo MIME del cuerpo. Para JSON es `application/json`, para HTML es `text/html`, para imágenes PNG es `image/png`. Este header le dice al cliente cómo interpretar el cuerpo de la respuesta.

**Content-Length:** Especifica el tamaño del cuerpo en bytes. Esto permite al cliente saber cuántos datos esperar y mostrar barras de progreso en descargas.

**Cache-Control:** Controla el comportamiento de caching:
- `Cache-Control: no-cache` - Los caches deben validar con el servidor antes de usar una copia cacheada
- `Cache-Control: max-age=3600` - La respuesta puede ser cacheada por 3600 segundos (1 hora)
- `Cache-Control: private` - Solo el navegador del usuario puede cachear, no caches compartidos como CDNs
- `Cache-Control: public` - Permite a cualquier cache almacenar la respuesta

**ETag:** Es un identificador único para una versión específica de un recurso. Si el contenido cambia, el ETag cambia. Los clientes pueden incluir el ETag en solicitudes futuras con el header `If-None-Match`. Si el recurso no ha cambiado, el servidor responde con 304 Not Modified en lugar de enviar el recurso completo nuevamente.

**Last-Modified:** Indica cuándo se modificó el recurso por última vez. Similar a ETag, los clientes pueden usar `If-Modified-Since` en solicitudes futuras para verificar si hay cambios.

**Location:** En respuestas 201 Created contiene la URL del recurso recién creado. En respuestas 3xx contiene la URL a la que redirigir.

**WWW-Authenticate:** Indica qué esquema de autenticación usar y qué realm protege el recurso.

Headers personalizados típicamente comienzan con `X-` aunque esta convención está en desuso. APIs modernas pueden incluir headers como:
- `X-Rate-Limit-Remaining` - Cuántas solicitudes te quedan antes de alcanzar el límite de tasa
- `X-Request-ID` - Para tracking y debugging

#### El body

El body contiene los datos reales:
- Para GET exitosos de recursos individuales, el body contiene la representación del recurso
- Para GET de colecciones, contiene un array de recursos
- Para POST, PUT, PATCH exitosos, típicamente contiene el recurso actualizado o creado
- Para DELETE, a menudo no hay body (204 No Content), aunque algunos APIs devuelven el recurso eliminado o un mensaje de confirmación

### 4.2 Ejemplo de respuesta JSON

Un ejemplo completo de respuesta HTTP te ayudará a visualizar todos estos elementos juntos:

```http
HTTP/1.1 200 OK
Date: Wed, 29 Oct 2025 15:23:45 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 342
Cache-Control: max-age=600
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
X-Rate-Limit-Limit: 100
X-Rate-Limit-Remaining: 87
X-Request-ID: f058ebd6-02f7-4d3f-942e-904344e8cde5

{
  "id": 42,
  "titulo": "Introducción a las APIs REST",
  "autor": {
    "id": 15,
    "nombre": "Ana Martínez",
    "email": "ana@ejemplo.com"
  },
  "contenido": "Las APIs REST son fundamentales...",
  "etiquetas": ["api", "rest", "backend", "tutorial"],
  "fechaCreacion": "2025-10-15T10:30:00Z",
  "fechaActualizacion": "2025-10-28T14:22:00Z",
  "estadisticas": {
    "vistas": 1547,
    "likes": 89,
    "comentarios": 23
  },
  "publicado": true,
  "_links": {
    "self": "/api/posts/42",
    "autor": "/api/usuarios/15",
    "comentarios": "/api/posts/42/comentarios"
  }
}
```

Esta respuesta incluye todos los elementos que hemos discutido. El código 200 indica éxito. Los headers proporcionan metadatos sobre el contenido, caching, rate limiting y tracking. El body JSON contiene un objeto estructurado con el recurso solicitado.

Nota el objeto `_links` al final. Esto sigue el principio **HATEOAS** (Hypermedia As The Engine Of Application State), un nivel avanzado de madurez REST donde las respuestas incluyen enlaces a recursos relacionados, permitiendo a los clientes descubrir la API navegando en lugar de requerir conocimiento previo de todas las URLs.

### 4.3 Errores comunes

El manejo correcto de errores es crítico para APIs usables y mantenibles.

#### 400 Bad Request

Indica que el servidor no puede o no procesará la solicitud debido a algo que se percibe como un error del cliente. Esto podría ser JSON malformado, campos faltantes obligatorios, o tipos de datos incorrectos. Una buena API devuelve un cuerpo de respuesta detallado explicando exactamente qué está mal:

```json
{
  "error": "ValidationError",
  "mensaje": "La solicitud contiene datos inválidos",
  "detalles": [
    {
      "campo": "email",
      "problema": "El formato del email es inválido",
      "valor": "esto-no-es-email"
    },
    {
      "campo": "edad",
      "problema": "Debe ser un número positivo",
      "valor": -5
    }
  ]
}
```

Estos errores detallados permiten a los desarrolladores frontend mostrar mensajes específicos al usuario y corregir problemas rápidamente durante el desarrollo.

#### 401 Unauthorized

(Que realmente significa "no autenticado") indica que la solicitud requiere autenticación del usuario. Esto ocurre cuando no se proporciona un token de autenticación, el token está expirado, o el token es inválido. Una respuesta 401 típicamente incluye un header `WWW-Authenticate` indicando el esquema de autenticación requerido:

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="api"
Content-Type: application/json

{
  "error": "AuthenticationRequired",
  "mensaje": "Token de autenticación faltante o inválido"
}
```

El cliente debería responder a 401 redirigiendo al usuario a una página de login o renovando su token de acceso si tiene un refresh token disponible.

#### 403 Forbidden

Es diferente de 401. Con 403, el servidor entendió la solicitud y sabe quién eres, pero te está negando el acceso. Tienes credenciales válidas pero no tienes los permisos necesarios. Por ejemplo, un usuario regular intentando acceder a un endpoint de administración:

```json
{
  "error": "InsufficientPermissions",
  "mensaje": "No tienes permisos para realizar esta acción",
  "permisosRequeridos": ["admin:write"],
  "tusPermisos": ["user:read", "user:write"]
}
```

La distinción entre 401 y 403 es importante: 401 significa "identifícate", 403 significa "te identificaste pero aún así no puedes hacer esto".

#### 404 Not Found

Indica que el servidor no encontró el recurso solicitado. Esto puede significar que el recurso nunca existió, fue eliminado, o la URL es incorrecta. Es importante distinguir entre "este tipo de recurso no existe en nuestra API" y "este tipo de recurso existe pero este ID específico no":

```json
{
  "error": "NotFound",
  "mensaje": "El producto con ID 999 no existe",
  "sugerencia": "Verifica el ID del producto e intenta nuevamente"
}
```

Algunos APIs usan 404 para ocultar la existencia de recursos sensibles. Por ejemplo, en lugar de devolver 403 para un recurso privado (revelando que existe pero no tienes acceso), devuelven 404 (no revelando si existe o no).

#### 500 Internal Server Error

Es el código de error genérico del servidor. Indica que algo falló en el servidor pero no hay un código más específico apropiado. Este error nunca debería incluir detalles técnicos sensibles como stack traces en producción:

```json
{
  "error": "InternalServerError",
  "mensaje": "Ocurrió un error al procesar tu solicitud",
  "timestamp": "2025-10-29T15:45:00Z",
  "requestId": "abc-123-def-456"
}
```

El `requestId` es crucial: permite al soporte técnico buscar logs detallados internos sin exponer información sensible al cliente. En entornos de desarrollo, puedes incluir más detalles, pero esto **nunca** debe llegar a producción por razones de seguridad.

---

## 5. Temas Adicionales Importantes

### 5.1 Autenticación y Autorización

La autenticación verifica quién eres. La autorización determina qué puedes hacer. Estos son conceptos separados que a menudo se confunden.

#### Autenticación básica HTTP

Es el método más simple. El cliente envía un header `Authorization: Basic base64(usuario:contraseña)`. El servidor decodifica y verifica. Esto es inseguro sin HTTPS porque las credenciales viajan en cada solicitud, aunque codificadas en base64 (que es fácilmente reversible, no es encriptación).

#### Autenticación basada en sesiones

Es el enfoque tradicional. Después de login exitoso, el servidor crea una sesión y envía un ID de sesión al cliente en una cookie. El cliente incluye automáticamente esta cookie en solicitudes subsecuentes. El servidor busca la sesión y verifica que esté activa. 

Este enfoque tiene desventajas para APIs:
- Requiere almacenamiento de estado en el servidor
- Complica el escalado horizontal
- Las cookies tienen limitaciones en aplicaciones móviles

#### Tokens JWT (JSON Web Tokens)

Son el estándar moderno para APIs. Un JWT es un token auto-contenido que incluye claims (afirmaciones) sobre el usuario codificadas en formato JSON y firmadas criptográficamente. Un JWT típico se ve así:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

Esto se divide en tres partes separadas por puntos:
1. **Header:** Especifica el algoritmo de firma
2. **Payload:** Contiene los claims (datos del usuario, tiempo de expiración, etc.)
3. **Signature:** Una firma criptográfica que garantiza que el token no ha sido alterado

**Flujo JWT:**
1. Usuario envía credenciales
2. Servidor verifica y genera un JWT
3. Cliente guarda el JWT y lo incluye en el header `Authorization: Bearer <token>` en solicitudes futuras
4. Servidor verifica la firma del JWT y extrae los claims sin necesidad de consultar una base de datos de sesiones

**Ventajas de JWT:**
- Sin estado (stateless)
- Escalables
- Funcionan perfectamente en arquitecturas distribuidas y microservicios

**Desafíos de JWT:**
- Una vez emitidos, no pueden ser revocados fácilmente sin mantener una lista negra (lo que reintroduce estado)
- Deben tener tiempos de expiración cortos para limitar el riesgo si son comprometidos

#### OAuth 2.0

Es un framework de autorización (no autenticación) que permite a aplicaciones de terceros obtener acceso limitado a recursos de un usuario sin obtener sus credenciales. Cuando haces "Login con Google", estás usando OAuth.

**Flujo Authorization Code (el más común):**
1. Tu app redirige al usuario a Google
2. Usuario se autentica con Google
3. Usuario autoriza a tu app a acceder a cierta información
4. Google redirige de vuelta a tu app con un código temporal
5. Tu app intercambia ese código por un token de acceso (llamada server-to-server)
6. Tu app usa el token para hacer solicitudes de API en nombre del usuario

**Flows de OAuth:**
- **Authorization Code:** Para aplicaciones web
- **Implicit Flow:** (Obsoleto) Para SPAs
- **Client Credentials:** Para comunicación máquina-a-máquina
- **Resource Owner Password Credentials:** (Desaconsejado) Cuando el cliente es completamente confiable

#### OpenID Connect (OIDC)

Es una capa de autenticación sobre OAuth 2.0. Mientras OAuth maneja autorización (acceso a recursos), OIDC maneja autenticación (identidad del usuario). OIDC añade un ID Token (un JWT) que contiene información sobre el usuario autenticado.

### 5.2 Rate Limiting y Throttling

Las APIs públicas necesitan protección contra abuso y uso excesivo. Rate limiting controla cuántas solicitudes puede hacer un cliente en un período de tiempo.

#### Estrategias de rate limiting

**Límites fijos por ventana de tiempo:** 
- Ejemplo: 100 solicitudes por hora
- Si alcanzas el límite debes esperar hasta que comience la próxima ventana

**Sliding window:**
- Más sofisticada que la ventana fija
- En lugar de reiniciar el contador cada hora exacta, mantiene un contador móvil de las últimas N solicitudes en la última hora

**Token bucket:**
- Permite ráfagas ocasionales
- Imagina un balde que se llena con tokens a una tasa constante
- Cada solicitud consume un token
- Si el balde está vacío, la solicitud es rechazada
- Esto permite que un cliente haga varias solicitudes rápidas si tiene tokens acumulados, pero previene uso sostenido excesivo

#### Comunicación de límites

Las APIs comunican límites de tasa mediante headers personalizados:

```http
X-Rate-Limit-Limit: 100
X-Rate-Limit-Remaining: 42
X-Rate-Limit-Reset: 1635524400
```

Cuando excedes el límite, el servidor responde con **429 Too Many Requests** y típicamente incluye un header `Retry-After` indicando cuántos segundos esperar antes de intentar nuevamente.

### 5.3 Versionado de APIs

Las APIs evolucionan. Necesitas agregar funcionalidades, cambiar comportamientos, o incluso eliminar features. Pero tienes clientes existentes dependiendo de la API actual. El versionado permite evolucionar tu API sin romper clientes existentes.

#### Versionado en la URL

El más común y explícito:

```
https://api.ejemplo.com/v1/usuarios
https://api.ejemplo.com/v2/usuarios
```

Cada versión major puede tener cambios incompatibles. Mantienes múltiples versiones simultáneamente por un período de transición, eventualmente deprecando versiones antiguas.

#### Versionado en headers

Mantiene URLs limpias pero es menos visible:

```http
GET /usuarios
Accept: application/vnd.ejemplo.v2+json
```

#### Versionado mediante parámetros de consulta

```
GET /usuarios?version=2
```

No existe consenso universal sobre el mejor enfoque. **URL versioning** es el más popular por su claridad y simplicidad, aunque algunos argumentan que mezcla versionado con identificación de recursos.

### 5.4 CORS (Cross-Origin Resource Sharing)

CORS es un mecanismo de seguridad del navegador que restringe cómo recursos en una página web pueden solicitar recursos de otro dominio.

#### Same-Origin Policy

Por defecto, los navegadores implementan la "same-origin policy": JavaScript en `https://sitio-a.com` no puede hacer solicitudes AJAX a `https://sitio-b.com`. Esto previene que sitios maliciosos roben datos de otros sitios.

#### Cómo funciona CORS

CORS relaja esta restricción de forma controlada. El servidor en `sitio-b.com` puede incluir headers CORS indicando qué orígenes externos están permitidos:

```http
Access-Control-Allow-Origin: https://sitio-a.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 3600
```

#### Preflight Requests

Para solicitudes "complejas" (con ciertos headers o métodos que no sean GET/POST), el navegador primero envía una solicitud OPTIONS "preflight" preguntando si la solicitud real está permitida. Si el servidor responde afirmativamente, el navegador procede con la solicitud real.

#### Configuración segura

Configurar CORS incorrectamente es una fuente común de frustración. `Access-Control-Allow-Origin: *` permite cualquier origen, lo cual está bien para APIs públicas pero es inseguro para APIs que usan autenticación basada en cookies.

### 5.5 Documentación de APIs

Una API sin documentación es prácticamente inutilizable. La documentación debe explicar cada endpoint, parámetros esperados, formato de solicitud, posibles respuestas, códigos de error, y ejemplos.

#### OpenAPI (anteriormente Swagger)

Es el estándar de facto para documentar APIs REST. Es una especificación legible por máquinas que describe tu API completa. Puedes escribir la especificación manualmente en YAML o JSON:

```yaml
openapi: 3.0.0
info:
  title: API de Productos
  version: 1.0.0
paths:
  /productos:
    get:
      summary: Listar productos
      parameters:
        - name: categoria
          in: query
          schema:
            type: string
      responses:
        '200':
          description: Lista exitosa
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Producto'
components:
  schemas:
    Producto:
      type: object
      properties:
        id:
          type: integer
        nombre:
          type: string
        precio:
          type: number
```

O mejor aún, generar la especificación automáticamente desde tu código usando anotaciones o reflexión. Herramientas como **Swagger UI** toman esta especificación y generan documentación interactiva hermosa donde puedes probar endpoints directamente en el navegador.

#### Postman

Es otra herramienta popular que permite crear colecciones de solicitudes organizadas, compartirlas con tu equipo, y generar documentación automáticamente. Puedes incluir ejemplos de solicitudes y respuestas, tests automáticos, y hasta mock servers.

#### Elementos de buena documentación

- Descripción general de la API y su propósito
- Flujo de autenticación con ejemplos
- Descripción de cada endpoint con ejemplos reales
- Esquemas de todos los objetos y tipos
- Lista completa de códigos de error con significados
- Límites de tasa y mejores prácticas
- SDKs y librerías cliente si están disponibles
- Changelog de versiones

### 5.6 Testing de APIs

Las APIs deben ser testeadas rigurosamente. Los tipos principales de tests son:

#### Tests unitarios

Verifican componentes individuales aisladamente. Para una función que valida emails, verificas que acepte emails válidos y rechace inválidos sin involucrar la base de datos o red.

#### Tests de integración

Verifican que componentes trabajen juntos correctamente. Testeas un endpoint completo, verificando que la solicitud HTTP se procese, la base de datos se actualice, y la respuesta sea correcta. Típicamente usas una base de datos de test separada.

#### Tests de contrato

Verifican que tu API cumple el contrato que publicaste. Si tu documentación dice que `/usuarios/{id}` devuelve un objeto con campos `id`, `nombre` y `email`, el test verifica que la respuesta real tenga exactamente esos campos con los tipos correctos.

#### Tests de carga

Verifican cómo se comporta tu API bajo carga pesada. Herramientas como Apache JMeter, Gatling o k6 simulan miles de usuarios concurrentes para identificar cuellos de botella y límites de capacidad.

#### Tests de seguridad

Buscan vulnerabilidades: inyección SQL, XSS, autenticación débil, exposición de datos sensibles, configuraciones inseguras. Herramientas como OWASP ZAP automatizan mucho de esto.

### 5.7 Seguridad en APIs

La seguridad es crítica. Las APIs exponen datos y funcionalidad valiosos y son objetivos frecuentes de ataques.

#### Siempre usa HTTPS

En producción, HTTPS es obligatorio. Esto encripta toda la comunicación previniendo ataques de man-in-the-middle donde un atacante intercepta y lee o modifica datos.

#### Valida toda entrada

Nunca confíes en datos del cliente. Valida tipos, rangos, formatos y contenido. Usa whitelist (permitir solo valores conocidos buenos) en lugar de blacklist (bloquear valores conocidos malos) cuando sea posible.

#### Prevén inyección SQL

Usa consultas parametrizadas o un ORM (Object-Relational Mapping). Nunca construyas consultas SQL concatenando strings con input del usuario:

```python
# ❌ VULNERABLE
query = f"SELECT * FROM usuarios WHERE email = '{email}'"

# ✅ SEGURO
query = "SELECT * FROM usuarios WHERE email = ?"
cursor.execute(query, (email,))
```

#### Autenticación y autorización robustas

- Usa tokens con expiración
- Verifica permisos en cada solicitud
- Nunca confíes en el cliente para determinar permisos

#### Protege contra CSRF

(Cross-Site Request Forgery) si usas cookies para autenticación. Usa tokens CSRF o trabaja exclusivamente con tokens en headers (que los navegadores no incluyen automáticamente en solicitudes cross-origin).

#### Limita tasa de solicitudes

Para prevenir ataques de denegación de servicio y fuerza bruta en logins.

#### Sanitiza salidas

Si devuelves contenido que se renderizará en HTML para prevenir XSS (Cross-Site Scripting).

#### Mantén dependencias actualizadas

Vulnerabilidades se descubren constantemente en bibliotecas populares. Usa herramientas como Dependabot o Snyk para monitorear y actualizar dependencias.

#### Registra y monitorea

Actividad sospechosa: múltiples intentos de login fallidos, accesos a recursos prohibidos, patrones de solicitud anormales.

---

## Fuentes de Consulta Especializadas y Oficiales

### Especificaciones y Estándares

1. **RFC 9110 - HTTP Semantics**  
   https://www.rfc-editor.org/rfc/rfc9110.html  
   Especificación oficial actualizada de HTTP/1.1 del IETF. Define métodos, códigos de estado, headers y semántica completa.

2. **RFC 9114 - HTTP/3**  
   https://www.rfc-editor.org/rfc/rfc9114.html  
   Especificación de la versión más reciente de HTTP.

3. **RFC 6749 - OAuth 2.0 Authorization Framework**  
   https://www.rfc-editor.org/rfc/rfc6749.html  
   Especificación oficial de OAuth 2.0.

4. **RFC 7519 - JSON Web Token (JWT)**  
   https://www.rfc-editor.org/rfc/rfc7519.html  
   Especificación oficial de JWT.

5. **OpenAPI Specification**  
   https://spec.openapis.org/oas/latest.html  
   Estándar para describir APIs REST.

6. **RFC 8259 - JSON Data Interchange Format**  
   https://www.rfc-editor.org/rfc/rfc8259.html  
   Especificación oficial de JSON.

### Documentación Oficial de Tecnologías

7. **MDN Web Docs - HTTP**  
   https://developer.mozilla.org/en-US/docs/Web/HTTP  
   Documentación exhaustiva de Mozilla sobre HTTP.

8. **GraphQL Official Documentation**  
   https://graphql.org/learn/  
   Documentación oficial de GraphQL.

9. **OWASP API Security Project**  
   https://owasp.org/www-project-api-security/  
   Guía de seguridad en APIs del Open Web Application Security Project.

10. **W3C CORS Specification**  
    https://www.w3.org/TR/cors/  
    Especificación oficial de CORS.

### Recursos Académicos y de Arquitectura

11. **Roy Fielding's Dissertation**  
    "Architectural Styles and the Design of Network-based Software Architectures"  
    https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm  
    Tesis doctoral original que define REST (2000).

12. **Microsoft REST API Guidelines**  
    https://github.com/microsoft/api-guidelines  
    Guías completas de diseño de APIs REST de Microsoft.

13. **Google Cloud API Design Guide**  
    https://cloud.google.com/apis/design  
    Principios de diseño de APIs de Google.

14. **AWS API Gateway Developer Guide**  
    https://docs.aws.amazon.com/apigateway/  
    Documentación técnica de AWS sobre APIs.

### Libros Técnicos Recomendados

15. **"RESTful Web APIs"**  
    Por Leonard Richardson y Mike Amundsen (O'Reilly)  
    Referencia definitiva sobre diseño REST.

16. **"API Design Patterns"**  
    Por JJ Geewax (Manning)  
    Patrones avanzados de diseño de APIs.

17. **"Building Microservices"**  
    Por Sam Newman (O'Reilly)  
    Arquitectura de microservicios y comunicación entre servicios.

---

## 6. Temas Adicionales Avanzados

### 6.1 WebSockets y Comunicación en Tiempo Real

Mientras HTTP sigue un modelo solicitud-respuesta, algunas aplicaciones requieren comunicación bidireccional en tiempo real. WebSockets proporciona un canal de comunicación full-duplex sobre una única conexión TCP.

#### ¿Cuándo usar WebSockets?

**Casos de uso ideales:**
- Aplicaciones de chat en tiempo real
- Notificaciones push instantáneas
- Juegos multijugador online
- Dashboards con datos en vivo (stock trading, analytics)
- Colaboración en tiempo real (Google Docs, Figma)

#### Diferencias con HTTP

HTTP es solicitud-respuesta: el cliente inicia, el servidor responde, la conexión se cierra (o se mantiene abierta con keep-alive pero permanece inactiva). WebSockets, por contraste, establece una conexión persistente bidireccional. Una vez establecida, tanto el cliente como el servidor pueden enviar mensajes en cualquier momento sin esperar una solicitud.

#### Establecimiento de conexión

WebSockets comienza con un "handshake" HTTP. El cliente envía una solicitud especial:

```http
GET /chat HTTP/1.1
Host: servidor.ejemplo.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

Si el servidor acepta, responde:

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

Después de este handshake, la conexión HTTP se actualiza a WebSocket y ambas partes pueden enviar mensajes libremente.

#### Alternativas modernas

**Server-Sent Events (SSE):** Para comunicación unidireccional del servidor al cliente. Más simple que WebSockets cuando no necesitas enviar datos del cliente al servidor. Usa HTTP estándar.

**HTTP/2 Server Push:** Permite al servidor enviar recursos al cliente antes de que sean solicitados, pero no es verdadera comunicación bidireccional.

**HTTP/3 y QUIC:** El futuro de comunicación web, construido sobre UDP en lugar de TCP, con mejor rendimiento en conexiones inestables.

### 6.2 Microservicios y Arquitecturas Distribuidas

A medida que las aplicaciones crecen, la arquitectura monolítica (toda la aplicación en un solo codebase y proceso) puede volverse difícil de mantener. Los microservicios ofrecen una alternativa.

#### Principios de microservicios

**Servicios pequeños y enfocados:** Cada microservicio hace una cosa y la hace bien. Por ejemplo, en un e-commerce: servicio de productos, servicio de inventario, servicio de pagos, servicio de notificaciones.

**Independencia:** Cada servicio puede ser desarrollado, desplegado y escalado independientemente. Pueden usar diferentes tecnologías, bases de datos y lenguajes según sea apropiado.

**Comunicación mediante APIs:** Los servicios se comunican exclusivamente a través de APIs bien definidas (usualmente REST o gRPC), nunca accediendo directamente a las bases de datos de otros servicios.

#### Ventajas

- **Escalabilidad:** Escala solo los servicios que lo necesitan
- **Resiliencia:** El fallo de un servicio no derriba toda la aplicación
- **Flexibilidad tecnológica:** Usa las mejores herramientas para cada trabajo
- **Desarrollo paralelo:** Equipos diferentes pueden trabajar en servicios diferentes sin conflictos

#### Desafíos

- **Complejidad operacional:** Necesitas orquestar múltiples servicios, monitorear múltiples componentes, manejar múltiples bases de datos
- **Transacciones distribuidas:** Mantener consistencia de datos a través de servicios es complejo
- **Latencia de red:** La comunicación entre servicios añade latencia
- **Debugging:** Rastrear un problema a través de múltiples servicios es más difícil que en un monolito

#### Service Mesh

Para gestionar la complejidad de microservicios, surgen tecnologías como Istio y Linkerd que proporcionan:
- Descubrimiento de servicios
- Load balancing
- Encriptación automática entre servicios
- Circuit breakers
- Observabilidad (metrics, logs, traces)

### 6.3 API Gateway

En arquitecturas de microservicios, un API Gateway actúa como punto de entrada único para todos los clientes.

#### Responsabilidades del API Gateway

**Routing:** Dirige las solicitudes al microservicio apropiado. El cliente hace una solicitud a `/api/productos` y el gateway la dirige al servicio de productos.

**Agregación:** Combina múltiples llamadas de microservicios en una sola respuesta. Por ejemplo, una página de producto podría necesitar datos del servicio de productos, inventario y reseñas. El gateway hace las tres llamadas y combina las respuestas.

**Autenticación y autorización:** Centraliza la verificación de identidad y permisos antes de permitir que las solicitudes lleguen a los microservicios.

**Rate limiting:** Aplica límites de tasa a nivel global.

**Transformación:** Convierte entre diferentes formatos o protocolos. El cliente puede comunicarse en REST mientras los microservicios internos usan gRPC.

**SSL Termination:** Maneja la encriptación HTTPS, permitiendo que la comunicación interna sea HTTP simple.

#### Ejemplos populares

- Kong
- Amazon API Gateway
- Azure API Management
- Apigee
- Nginx Plus

### 6.4 Caching Estratégico

El caching es fundamental para APIs de alto rendimiento. Almacenar resultados de operaciones costosas reduce latencia y carga del servidor.

#### Niveles de caching

**Cache del navegador:** El navegador guarda respuestas basándose en headers como `Cache-Control` y `Expires`. Completamente transparente para tu código JavaScript.

**CDN (Content Delivery Network):** Cachea respuestas en servidores distribuidos geográficamente cerca de los usuarios. Ideal para contenido estático y APIs con datos que no cambian frecuentemente.

**Cache de aplicación:** En tu backend, usando herramientas como Redis o Memcached. Almacena resultados de consultas de base de datos, cálculos complejos, o respuestas de APIs externas.

**Cache de base de datos:** Muchas bases de datos tienen caching interno, pero puedes optimizarlo con estrategias específicas.

#### Estrategias de invalidación

El problema difícil del caching es saber cuándo invalidar:

**Time-based (TTL - Time To Live):** Los datos expiran después de un período. Simple pero puede servir datos obsoletos.

**Event-based:** Invalida explícitamente cuando cambian los datos. Más complejo pero más preciso.

**Cache-aside (Lazy loading):** La aplicación verifica el cache primero. Si no encuentra el dato, lo obtiene de la fuente, lo guarda en cache, y lo devuelve.

**Write-through:** Cada escritura actualiza tanto la base de datos como el cache simultáneamente.

**Write-behind:** Las escrituras van primero al cache y se escriben a la base de datos asincrónicamente.

#### Headers HTTP para caching

```http
Cache-Control: public, max-age=3600
ETag: "686897696a7c876b7e"
Last-Modified: Wed, 29 Oct 2025 12:00:00 GMT
Vary: Accept-Encoding, Accept-Language
```

### 6.5 Diseño de APIs Idempotentes

La idempotencia es una propiedad crucial en sistemas distribuidos donde las solicitudes pueden repetirse debido a fallos de red o reintentos automáticos.

#### ¿Qué es idempotencia?

Una operación es idempotente si ejecutarla múltiples veces tiene el mismo efecto que ejecutarla una vez. En APIs, significa que puedes hacer la misma solicitud repetidamente sin efectos secundarios no deseados.

#### Métodos HTTP y idempotencia

**Idempotentes por naturaleza:**
- GET: Leer múltiples veces no cambia nada
- PUT: Reemplazar un recurso con los mismos datos produce el mismo resultado
- DELETE: Eliminar algo que ya no existe es equivalente a eliminarlo exitosamente

**No idempotentes:**
- POST: Cada POST típicamente crea un nuevo recurso

#### Haciendo POST idempotente

Usa **idempotency keys**. El cliente genera un identificador único para cada operación lógica y lo envía con la solicitud:

```http
POST /pagos HTTP/1.1
Idempotency-Key: a7b9c3d1-e2f4-4a5c-8b7d-9e8f7a6b5c4d
Content-Type: application/json

{
  "monto": 100.00,
  "moneda": "USD",
  "tarjeta": "..."
}
```

El servidor guarda este key junto con el resultado. Si recibe la misma key nuevamente, devuelve el resultado original sin procesar el pago nuevamente. Esto previene cargos duplicados en caso de reintentos.

### 6.6 Paginación Avanzada

Para colecciones grandes, la paginación simple (página 1, 2, 3...) tiene limitaciones. Existen enfoques más sofisticados.

#### Offset-based pagination

El enfoque tradicional:

```
GET /productos?limite=20&offset=40
```

Obtiene 20 productos comenzando desde el producto 41. Simple pero problemático:
- Rendimiento: `OFFSET 10000` requiere que la base de datos escanee y descarte 10000 registros
- Inconsistencias: Si se añaden/eliminan items mientras paginas, puedes ver duplicados o saltarte items

#### Cursor-based pagination

Usa un cursor (típicamente el ID del último item visto) como punto de partida:

```
GET /productos?limite=20&despues=producto_123
```

Obtiene 20 productos después del producto con ID 123. Más eficiente y consistente, pero no permite saltar a páginas arbitrarias.

#### Keyset pagination

Similar a cursor-based pero usa campos ordenables:

```
GET /productos?limite=20&despues_fecha=2025-10-15T10:30:00Z&despues_id=123
```

Ordena por fecha, usando ID como desempate. Muy eficiente con índices apropiados.

#### Respuesta con metadata

Incluye información de paginación en las respuestas:

```json
{
  "datos": [...],
  "paginacion": {
    "siguiente": "/productos?limite=20&despues=producto_140",
    "anterior": "/productos?limite=20&antes=producto_121",
    "totalAproximado": 5000
  }
}
```

### 6.7 Manejo de Errores Consistente

Un esquema de errores consistente mejora la experiencia del desarrollador.

#### Estructura estándar de error

```json
{
  "error": {
    "codigo": "VALIDATION_ERROR",
    "mensaje": "Los datos proporcionados son inválidos",
    "detalles": [
      {
        "campo": "email",
        "codigo": "INVALID_FORMAT",
        "mensaje": "El formato del email es inválido"
      }
    ],
    "timestamp": "2025-10-29T15:30:00Z",
    "requestId": "req_abc123",
    "documentacion": "https://api.ejemplo.com/docs/errores#VALIDATION_ERROR"
  }
}
```

#### Códigos de error específicos

En lugar de solo HTTP status codes, usa códigos específicos de tu aplicación:

```
AUTHENTICATION_REQUIRED
INSUFFICIENT_PERMISSIONS
RESOURCE_NOT_FOUND
INVALID_INPUT
RATE_LIMIT_EXCEEDED
SERVICE_UNAVAILABLE
```

Esto permite a los clientes manejar errores específicos programáticamente sin parsear mensajes de texto.

#### Problem Details (RFC 7807)

Un estándar para expresar errores en APIs HTTP:

```json
{
  "type": "https://api.ejemplo.com/errores/sin-fondos",
  "title": "No tienes fondos suficientes",
  "status": 400,
  "detail": "Tu cuenta tiene un balance de 30 USD pero intentaste transferir 50 USD",
  "instance": "/cuenta/12345/transferencias/67890"
}
```

### 6.8 API Versioning Strategies en Profundidad

#### Versionado semántico

Usa versionado semántico (MAJOR.MINOR.PATCH):
- MAJOR: Cambios incompatibles
- MINOR: Nueva funcionalidad compatible hacia atrás
- PATCH: Bug fixes compatibles

Ejemplo: `v2.3.1`

#### Deprecación gradual

Cuando introduces v2, mantén v1 funcionando. Comunica la deprecación:

```http
Deprecation: version="v1", date="2026-10-29"
Sunset: Tue, 29 Oct 2026 12:00:00 GMT
Link: <https://api.ejemplo.com/docs/migracion-v2>; rel="deprecation"
```

Da a los clientes tiempo suficiente (típicamente 6-12 meses) para migrar.

#### Versionado de campos

Para cambios menores, versiona campos individuales en lugar de toda la API:

```json
{
  "nombre": "Producto A",
  "precio_v1": 100.00,
  "precio_v2": {
    "monto": 100.00,
    "moneda": "USD"
  }
}
```

### 6.9 Webhooks

Los webhooks permiten que tu API notifique a aplicaciones externas cuando ocurren eventos, invirtiendo el patrón típico de polling.

#### Cómo funcionan

1. El cliente se registra proporcionando una URL de callback
2. Cuando ocurre un evento relevante, tu API hace una solicitud HTTP POST a esa URL
3. El cliente procesa el evento

```json
POST https://cliente.com/webhook
Content-Type: application/json
X-Webhook-Signature: sha256=...

{
  "evento": "pago.completado",
  "timestamp": "2025-10-29T15:30:00Z",
  "datos": {
    "pagoId": "pay_123",
    "monto": 100.00,
    "moneda": "USD"
  }
}
```

#### Seguridad de webhooks

**Firmas:** Incluye una firma HMAC del payload para que el receptor pueda verificar que el webhook realmente vino de ti.

**IPs permitidas:** Publica las IPs desde las que envías webhooks para que los clientes puedan configurar firewalls.

**Reintentos:** Si el endpoint del cliente está caído, reintenta con backoff exponencial.

**Idempotencia:** Incluye un ID único de evento para que los clientes puedan deduplicar si reciben el mismo evento múltiples veces.

### 6.10 GraphQL vs REST: Una Comparación Profunda

#### Ventajas de GraphQL

**Flexibilidad:** El cliente especifica exactamente qué datos necesita, evitando over-fetching y under-fetching.

**Un solo endpoint:** Todas las consultas van a un único endpoint (típicamente `/graphql`), simplificando el routing.

**Tipos fuertemente tipados:** GraphQL usa un schema que define todos los tipos, campos y relaciones. Esto permite validación automática, autocompletado en IDEs, y generación de código cliente.

**Introspección:** Los clientes pueden consultar el schema para descubrir qué operaciones están disponibles.

**Versionado implícito:** En lugar de versionar la API completa, evolucionas el schema añadiendo campos sin eliminar los existentes. Los clientes nuevos usan campos nuevos, los viejos siguen usando campos viejos.

#### Desventajas de GraphQL

**Complejidad:** Requiere más configuración inicial y comprensión conceptual que REST.

**Caching:** El caching HTTP estándar no funciona tan bien porque todas las solicitudes van al mismo endpoint con POST.

**Performance:** Consultas mal diseñadas pueden ser costosas. Necesitas implementar límites de profundidad, complejidad, y rate limiting a nivel de query.

**Curva de aprendizaje:** Los desarrolladores familiarizados con REST necesitan aprender nuevos conceptos.

#### Cuándo usar cada uno

**Usa REST cuando:**
- Tu API es relativamente simple y estable
- Los clientes necesitan datos en formatos predecibles
- Quieres aprovechar caching HTTP estándar
- Tu equipo está más familiarizado con REST

**Usa GraphQL cuando:**
- Tienes múltiples clientes con necesidades de datos muy diferentes (web, móvil, tablets)
- Quieres minimizar solicitudes de red desde clientes móviles
- Tu dominio de datos es complejo con muchas relaciones
- Necesitas flexibilidad para evolucionar rápidamente sin romper clientes

### 6.11 gRPC y Protocol Buffers

gRPC es un framework RPC (Remote Procedure Call) de alto rendimiento desarrollado por Google, usado principalmente para comunicación entre microservicios.

#### Características clave

**Protocol Buffers:** En lugar de JSON, gRPC usa Protocol Buffers (protobuf), un formato binario de serialización más compacto y rápido.

**HTTP/2:** Construido sobre HTTP/2, permitiendo multiplexing (múltiples solicitudes en una conexión), streaming bidireccional, y compresión de headers.

**Generación de código:** Defines tu API en un archivo `.proto` y generas código cliente y servidor automáticamente para múltiples lenguajes.

#### Ejemplo de definición

```protobuf
syntax = "proto3";

service ProductoService {
  rpc ObtenerProducto(ProductoRequest) returns (Producto);
  rpc ListarProductos(ListarRequest) returns (stream Producto);
}

message ProductoRequest {
  string id = 1;
}

message Producto {
  string id = 1;
  string nombre = 2;
  double precio = 3;
}
```

#### Cuándo usar gRPC

- Comunicación entre microservicios internos donde controlas cliente y servidor
- Necesitas máximo rendimiento y eficiencia
- Quieres streaming bidireccional
- Trabajas en un entorno multi-lenguaje

**No uses gRPC para APIs públicas web** porque los navegadores no soportan gRPC nativamente (requiere gRPC-Web como proxy).

### 6.12 Observabilidad: Logs, Metrics y Traces

En producción, necesitas entender qué está pasando en tu API. La observabilidad se compone de tres pilares.

#### Logs

Registros de eventos discretos:

```json
{
  "timestamp": "2025-10-29T15:30:45Z",
  "nivel": "error",
  "mensaje": "Fallo al conectar con la base de datos",
  "requestId": "req_abc123",
  "userId": "user_456",
  "error": "Connection timeout after 5000ms"
}
```

**Mejores prácticas:**
- Usa structured logging (JSON) en lugar de texto libre
- Incluye contextualmente relevante (request ID, user ID)
- Usa niveles apropiados (DEBUG, INFO, WARN, ERROR)
- Nunca registres información sensible (contraseñas, tokens, números de tarjeta)

#### Metrics

Mediciones numéricas agregadas:
- Tasa de solicitudes por segundo
- Latencia (p50, p95, p99)
- Tasa de errores
- Uso de CPU/memoria
- Tamaño de pool de conexiones de base de datos

Herramientas: Prometheus, Grafana, Datadog, New Relic

#### Traces

Rastrean solicitudes a través de múltiples servicios, mostrando dónde se gasta el tiempo:

```
Solicitud total: 250ms
├─ API Gateway: 5ms
├─ Servicio de Autenticación: 20ms
├─ Servicio de Productos: 180ms
│  ├─ Consulta DB: 150ms
│  └─ Procesamiento: 30ms
└─ Servicio de Inventario: 45ms
```

Herramientas: Jaeger, Zipkin, OpenTelemetry

### 6.13 Resilience Patterns

En sistemas distribuidos, los fallos son inevitables. Necesitas diseñar para la resiliencia.

#### Circuit Breaker

Previene que tu aplicación intente repetidamente operaciones que probablemente fallarán.

**Estados:**
1. **Closed:** Funcionamiento normal, las solicitudes pasan
2. **Open:** Demasiados fallos, las solicitudes fallan inmediatamente sin intentar
3. **Half-Open:** Después de un timeout, permite algunas solicitudes de prueba

Si las pruebas tienen éxito, vuelve a Closed. Si fallan, vuelve a Open.

#### Retry con Backoff Exponencial

Cuando una solicitud falla, reintenta con delays crecientes:
- 1er intento: inmediato
- 2do intento: espera 1 segundo
- 3er intento: espera 2 segundos
- 4to intento: espera 4 segundos
- 5to intento: espera 8 segundos

Añade jitter (variación aleatoria) para evitar que todos los clientes reintenten simultáneamente.

#### Timeout

Siempre configura timeouts. Una solicitud sin timeout puede bloquear recursos indefinidamente.

```python
try:
    respuesta = requests.get(url, timeout=5.0)
except requests.Timeout:
    # Manejar timeout
```

#### Bulkhead

Aísla recursos. Si tienes un pool de 100 conexiones de base de datos, no permitas que un endpoint problemático las consuma todas. Asigna pools separados a diferentes partes de tu aplicación.

#### Graceful Degradation

Cuando una dependencia falla, proporciona funcionalidad reducida en lugar de fallar completamente. Por ejemplo, si tu servicio de recomendaciones falla, muestra productos populares generales en lugar de no mostrar nada.

---

## Conclusión

Esta guía cubre los fundamentos esenciales del backend y las APIs REST, desde conceptos básicos hasta temas avanzados de seguridad, resiliencia y mejores prácticas arquitectónicas. 

### Ruta de Aprendizaje Recomendada

1. **Fundamentos (Semanas 1-2):**
   - Comprende HTTP profundamente
   - Practica con herramientas como Postman o curl
   - Construye una API REST simple con tu framework favorito

2. **Intermedio (Semanas 3-6):**
   - Implementa autenticación JWT
   - Añade validación robusta y manejo de errores
   - Implementa paginación y filtrado
   - Escribe tests para tu API

3. **Avanzado (Semanas 7-12):**
   - Diseña para escalabilidad con caching
   - Implementa rate limiting
   - Añade observabilidad (logs, metrics, traces)
   - Estudia patrones de resiliencia
   - Explora arquitecturas de microservicios

4. **Especialización (Continuo):**
   - GraphQL o gRPC según tus necesidades
   - Patrones específicos de tu dominio
   - Optimización de performance
   - Seguridad avanzada

### Recursos de Práctica

- **APIs públicas para estudiar:** GitHub API, Stripe API, Twilio API (excelentes ejemplos de diseño)
- **Proyectos prácticos:** Crea un blog API, una tienda online, un sistema de gestión de tareas
- **Code reviews:** Lee código de proyectos open source populares

### Mantente Actualizado

El campo del desarrollo backend evoluciona constantemente. Sigue:
- Blogs oficiales de tecnologías que uses
- Conferencias como API Days, QCon
- Newsletters como API Evangelist, InfoQ
- RFCs nuevos y actualizaciones de especificaciones

Las fuentes proporcionadas en este documento te dan acceso a conocimiento desde los fundamentos (especificaciones RFC) hasta implementaciones prácticas (guías de Google/Microsoft) y teoría arquitectónica (tesis de Fielding). Son recursos autoritativos mantenidos por los organismos que definen los estándares o por las empresas que operan APIs a mayor escala mundial.