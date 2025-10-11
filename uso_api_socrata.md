# Uso de la API de Socrata (SODA)

Para consumir datos desde la Socrata Open Data API (SODA) —la tecnología utilizada por numerosos portales de datos abiertos en Colombia y Latinoamérica— es necesario seguir una serie de pasos que incluyen localizar el conjunto de datos, obtener el identificador del dataset y consultar el endpoint mediante consultas SoQL. A continuación se describe el procedimiento utilizando información oficial de la documentación de Socrata.

## 1. Localizar el conjunto de datos y obtener su identificador

- **Buscar el portal correcto**: Socrata aloja catálogos de datos para gobiernos locales, entidades no lucrativas y organismos internacionales ([dev.socrata.com](https://dev.socrata.com)). Se recomienda visitar la página de datos abiertos de su municipalidad o utilizar el Open Data Network para encontrar datasets relevantes.

- **Encontrar el dataset**: Una vez en el portal, añada la ruta `/browse` al dominio (por ejemplo `https://datos.bogota.gov.co/browse`) para explorar y filtrar los datasets.

- **Ubicar el botón "API"**: Socrata muestra un botón "API" en los DataLens y un menú "Export" con la opción API en las tablas tradicionales. Allí se muestra la "API Access Endpoint" y el identificador único del conjunto de datos (ocho caracteres separados por un guion); por ejemplo, el dataset de permisos de construcción de Chicago tiene el ID `ydr8-5enu`.

**Ejemplo**: En el portal de Nueva York, el dataset de solicitudes de servicio 311 está disponible en `https://data.cityofnewyork.us/resource/erm2-nwe9.json`. El identificador `erm2-nwe9` se utilizará en las consultas.

## 2. Construir el endpoint de la API

Todos los recursos de SODA se acceden mediante una URL común:

```
https://<dominio>/api/v3/views/<IDENTIFICADOR>/query.json  # para consultas
https://<dominio>/api/v3/views/<IDENTIFICADOR>/export.csv  # para exportar
```

El identificador del dataset se inserta en la URL; por ejemplo: `https://data.cityofnewyork.us/api/v3/views/erm2-nwe9/query.json`.

- **Versiones anteriores (2.x)**: Algunos portales siguen usando la forma `https://<dominio>/resource/<IDENTIFICADOR>.json`. Compruebe en la documentación del dataset cuál versión soporta.

- **Versión 3.0**: Separa las rutas en dos funciones: `/query` para realizar consultas parametrizadas y `/export` para descargar archivos completos. Socrata recomienda utilizar POST al invocar `/query`, ya que permite consultas más largas y claras.

## 3. Filtrar datos usando SoQL

**SoQL** (Socrata Query Language) es un lenguaje similar a SQL diseñado para filtrar, ordenar y agrupar datos.

- Las consultas se especifican mediante el parámetro `query` en el cuerpo JSON de una solicitud POST o como parámetros de consulta en solicitudes GET.

- **Paginación**: Utilice `$limit` y `$offset`. Por ejemplo, `$limit=100` devuelve 100 filas y `$offset=100` omite las 100 primeras.

- **Versión 3.0**: Se puede suministrar un objeto `page` con `pageNumber` y `pageSize`.

### Ejemplo de consulta

Recuperar las primeras 100 filas de un dataset con aplicación de token:

```bash
curl --header 'X-App-Token: SU_TOKEN_DE_APP' \
     --json '{
        "query": "SELECT *",
        "page": { "pageNumber": 1, "pageSize": 100 },
        "includeSynthetic": false
      }' \
     https://soda.demo.socrata.com/api/v3/views/4tka-6guv/query.json
```


Este ejemplo, tomado de la documentación oficial, muestra cómo enviar un JSON mediante curl.

## 4. Gestionar límites y tokens de aplicación

- **Límites anónimos**: Socrata limita el número de llamadas anónimas. Sin token, las peticiones provienen de un pool compartido y se cortan tras un número reducido de solicitudes.

- **Token de aplicación**: Para disponer de hasta 1000 consultas por hora, cree una cuenta gratuita y registre un token de aplicación. La documentación oficial explica cómo obtenerlo.

- **Uso del token**: Los tokens se incluyen en la cabecera `X-App-Token` de cada solicitud. Se aconseja usar un token incluso para consultas de lectura, ya que las solicitudes sin token están sujetas a un throttling más estricto.

## 5. Autenticación avanzada (opcional)

HTTP Basic y OAuth 2.0 son los dos métodos de autenticación soportados:

- **HTTP Basic**: Se usa en scripts o herramientas ETL; se envían usuario y contraseña o un par de clave/secret del API en cabeceras HTTP sobre conexión segura. Socrata recomienda usar llaves de API para evitar exponer contraseñas.

- **OAuth 2.0**: Es preferible en aplicaciones interactivas. Se registra la aplicación, se obtiene un `access_token` y se envía en la cabecera `Authorization: OAuth <token>`.

> **Nota**: Para la mayoría de consultas públicas, basta con un token de aplicación; la autenticación solo es necesaria al escribir o modificar datos.

## 6. Ejemplo en Python con sodapy (opcional)

La librería `sodapy` (Python) simplifica la interacción with SODA. Puede instalarla con:

```bash
pip install sodapy
```

Según la documentación de PyPI, un cliente básico se crea así:

```python
from sodapy import Socrata

# Con token de aplicación
client = Socrata("sandbox.demo.socrata.com", "TuAppToken")

# Cliente sin token (sujeto a límites de uso estrictos)
client = Socrata("sandbox.demo.socrata.com", None)
```


La librería señala que el token de aplicación no es obligatorio para leer datos, pero las consultas sin él estarán sujetas a un throttling estricto. Para obtener datos, use `client.get(identificador, limit=...)` y filtre con parámetros SoQL; por ejemplo:

```python
results = client.get("nimj-3ivp", where="depth > 300", order="magnitude DESC", limit=5)
```

## Conclusión

Consumir datos desde la Socrata Open Data API implica:

1. **Identificar** el conjunto de datos deseado
2. **Extraer** su identificador
3. **Construir** la URL de la API (`/api/v3/views/<ID>/query.json` o `/resource/<ID>.json`)
4. **Realizar consultas** mediante SoQL

La documentación oficial destaca la necesidad de:
- **Paginación** para manejar grandes conjuntos de datos
- **Tokens de aplicación** para evitar límites estrictos
- **Autenticación** (HTTP Basic u OAuth) en casos especiales

Con estos pasos y la flexibilidad de SoQL, es posible integrar de forma eficiente los datos abiertos de gobiernos y organizaciones en proyectos de análisis, aplicaciones web o procesos ETL.