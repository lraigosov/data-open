# Uso de la API de Socrata (SODA)

Guía para consumir datos desde la Socrata Open Data API (SODA) utilizada en portales de datos abiertos de Colombia y Latinoamérica.

## 1. Localizar el Dataset

- **Portal**: Visitar el portal de datos abiertos (ej: datos.bogota.gov.co)
- **Explorar**: Agregar `/browse` a la URL del dominio
- **API Endpoint**: Buscar el botón "API" o menú "Export"
- **Identificador**: Obtener el ID único (8 caracteres con guión, ej: `ydr8-5enu`)

## 2. Construir el Endpoint

```
https://<dominio>/api/v3/views/<ID>/query.json  # Consultas
https://<dominio>/api/v3/views/<ID>/export.csv  # Exportar
https://<dominio>/resource/<ID>.json            # API v2 (legacy)
```

**Ejemplo**: `https://data.cityofnewyork.us/api/v3/views/erm2-nwe9/query.json`

## 3. Filtrar con SoQL

**SoQL** (Socrata Query Language) es similar a SQL para filtrar, ordenar y agrupar datos.

- **Parámetros**: `query` en POST (JSON) o query string en GET
- **Paginación**: `$limit` y `$offset`
- **API v3**: Objeto `page` con `pageNumber` y `pageSize`

### Ejemplo de consulta

```bash
curl --header 'X-App-Token: TU_TOKEN' \
     --json '{
        "query": "SELECT *",
        "page": { "pageNumber": 1, "pageSize": 100 }
      }' \
     https://soda.demo.socrata.com/api/v3/views/4tka-6guv/query.json
```

## 4. Tokens y Límites

- **Sin token**: Límites estrictos, pool compartido
- **Con token**: Hasta 1000 consultas/hora
- **Obtener token**: Registro gratuito en dev.socrata.com
- **Uso**: Cabecera `X-App-Token: tu_token`

## 5. Autenticación (Opcional)

Requerida solo para escritura/modificación:

- **HTTP Basic**: Usuario/contraseña o API key/secret
- **OAuth 2.0**: Token en cabecera `Authorization: OAuth <token>`

Para consultas públicas, solo se necesita el token de aplicación.

## 6. Ejemplo con Python (sodapy)

```bash
pip install sodapy
```

```python
from sodapy import Socrata

# Con token
client = Socrata("sandbox.demo.socrata.com", "TuAppToken")

# Sin token (límites estrictos)
client = Socrata("sandbox.demo.socrata.com", None)

# Consulta con filtros
results = client.get("nimj-3ivp", 
                     where="depth > 300", 
                     order="magnitude DESC", 
                     limit=5)
```

## Resumen

1. **Identificar** el dataset y obtener su ID
2. **Construir** la URL de la API
3. **Consultar** con SoQL para filtrar datos
4. **Usar token** para evitar límites
5. **Paginar** para grandes conjuntos de datos