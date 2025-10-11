# Descubrimiento datasets LATAM

Este módulo consulta múltiples APIs para inventariar datasets de portales de datos abiertos:
- **Colombia**: Socrata Discovery API (www.datos.gov.co)
- **México**: CKAN API (datos.gob.mx)
- **Chile**: CKAN API (datos.gob.cl)
- **Ecuador**: CKAN API (datosabiertos.gob.ec)

## Requisitos
- Python 3.9+
- Dependencias: ver `requirements.txt`
- App Token (recomendado) para cabecera `X-App-Token` para evitar límites de tasa

## Configurar credenciales

### Opción 1: Archivo de configuración (Recomendado)
1. Copia el archivo de ejemplo: `cp ../secretos.json.example ../secretos.json`
2. Edita `../secretos.json` con tus credenciales reales
3. El archivo `secretos.json` está protegido por `.gitignore`

### Opción 2: Variable de entorno
En PowerShell (Windows):
```powershell
$env:SOCRATA_APP_TOKEN = "<tu_token>"
```

### Detección automática
El sistema busca credenciales en este orden:
1. Variable de entorno `SOCRATA_APP_TOKEN`
2. Archivo `../secretos.json` con llaves `socrata_app_token`, `AppToken` o `APIKeyID`

## Plataformas soportadas
El proyecto maneja múltiples tecnologías:

### Colombia (Socrata)
- Plataforma: Socrata Discovery API
- Dominio: `www.datos.gov.co`
- Filtros: por dominio, categorías, términos de búsqueda

### México (CKAN)  
- Plataforma: CKAN API (Sistema Ajolote)
- URL base: `https://datos.gob.mx`
- Filtros: por grupos/categorías, organización, términos de búsqueda

### Chile (CKAN)
- Plataforma: CKAN API
- URL base: `https://datos.gob.cl`
- Filtros: por grupos/categorías, organización, términos de búsqueda
- Total datasets: ~2,769

### Ecuador (CKAN)
- Plataforma: CKAN API  
- URL base: `https://datosabiertos.gob.ec`
- Filtros: por grupos/categorías, organización, términos de búsqueda
- Total datasets: ~1,509

### Limitaciones conocidas
- **Perú**: Usa DKAN/plataforma custom, API CKAN no disponible
- **Brasil**: Usa plataforma custom, API CKAN no disponible

Configuración en `latam_domains.json`:
```json
{
  "Colombia": {
    "platform": "socrata",
    "domains": ["www.datos.gov.co"]
  },
  "México": {
    "platform": "ckan", 
    "base_url": "https://datos.gob.mx"
  },
  "Chile": {
    "platform": "ckan",
    "base_url": "https://datos.gob.cl"
  },
  "Ecuador": {
    "platform": "ckan",
    "base_url": "https://datosabiertos.gob.ec"
  }
}
```

## Configuración de fechas
Puedes definir un rango de publicación en `config.json`:

```
{
	"published_from": "2023-01-01",
	"published_to": "2025-12-31"
}
```

Además, puedes sobrescribirlo por CLI:

```powershell
python .\descubrimiento\run_discovery.py --country Colombia --published-from 2024-01-01 --published-to 2024-12-31
```

## Uso rápido
Instala dependencias y ejecuta el script principal:

```powershell
# Desde la carpeta del repo
python -m pip install -r .\descubrimiento\requirements.txt
python .\descubrimiento\run_discovery.py
```

Parámetros útiles:
- `--country <País>`: procesa un país específico como Colombia, México, Chile o Ecuador (por defecto procesa todos los países configurados).
- `--q <texto>`: término de búsqueda global.
- `--categories <cat1> <cat2>`: filtrar por categorías del catálogo.
- `--limit <n>`: máximo de items por dominio (por defecto 1000).

## Salida
Los resultados se guardan en `descubrimiento/output/` con nombre:
- `<pais>_catalog.json` y `<pais>_catalog.csv`: registros normalizados del catálogo.
- `<pais>_summary.csv`: métricas agregadas por tipo y categoría.

Ejemplos: `colombia_catalog.json`, `méxico_catalog.csv`, `chile_catalog.json`, `ecuador_summary.csv`

## Notas técnicas
- **Socrata (Colombia)**: Paginación hasta 100 registros por solicitud; requiere token para evitar rate limiting.
- **CKAN (México, Chile, Ecuador)**: Paginación hasta 1000 registros por solicitud; no requiere autenticación.
- Todos los clientes normalizan campos clave para generar outputs compatibles.
- El filtro por fecha se aplica localmente tras obtener los datos (las APIs no siempre soportan filtros de fecha nativos).