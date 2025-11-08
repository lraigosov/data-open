# Descubrimiento de Datasets LATAM

Sistema de consulta a múltiples APIs para inventariar datasets de portales de datos abiertos:
- **Colombia**: Socrata Discovery API (www.datos.gov.co)
- **México**: CKAN API (datos.gob.mx)
- **Chile**: CKAN API (datos.gob.cl)
- **Ecuador**: CKAN API (datosabiertos.gob.ec)

## Requisitos
- Python 3.9+
- Dependencias: `requests>=2.31`
- Token de Socrata (recomendado) para evitar límites de tasa

## Configurar credenciales

### Opción 1: Archivo de configuración (Recomendado)
```bash
cp ../secretos.json.example ../secretos.json
# Editar con tus credenciales
```

### Opción 2: Variable de entorno
```powershell
$env:SOCRATA_APP_TOKEN = "tu_token"
```

### Detección automática
Busca credenciales en este orden:
1. Variable de entorno `SOCRATA_APP_TOKEN`
2. Archivo `../secretos.json` con llave `socrata_app_token`

## Plataformas soportadas

### Colombia (Socrata)
- API: Socrata Discovery API
- Dominio: `www.datos.gov.co`
- Autenticación: Token requerido
- Paginación: 100 registros/solicitud

### México (CKAN)  
- API: CKAN package_search
- URL: `https://datos.gob.mx`
- Autenticación: No requerida
- Paginación: 1000 registros/solicitud

### Chile (CKAN)
- API: CKAN package_search
- URL: `https://datos.gob.cl`
- Autenticación: No requerida
- Total datasets: ~2,769

### Ecuador (CKAN)
- API: CKAN package_search  
- URL: `https://datosabiertos.gob.ec`
- Autenticación: No requerida
- Total datasets: ~1,509

## Configuración

### Archivo latam_domains.json
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

### Archivo config.json
```json
{
  "published_from": "2024-01-01",
  "published_to": "2025-12-31"
}
```

## Uso

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecución básica
```bash
# Todos los países
python run_discovery.py

# País específico
python run_discovery.py --country Colombia

# Con filtros de fecha
python run_discovery.py --country México --published-from 2024-01-01 --published-to 2024-12-31

# Buscar por término
python run_discovery.py --q salud --limit 50
```

### Parámetros CLI
- `--country <País>`: Colombia, México, Chile o Ecuador
- `--q <texto>`: Término de búsqueda
- `--categories <cat1> <cat2>`: Filtrar por categorías
- `--limit <n>`: Máximo de registros (default: 1000)
- `--published-from <YYYY-MM-DD>`: Fecha inicio
- `--published-to <YYYY-MM-DD>`: Fecha fin

## Salida

Resultados en `descubrimiento/output/`:
- `<pais>_catalog.json`: Datos completos en JSON
- `<pais>_catalog.csv`: Datos completos en CSV
- `<pais>_summary.csv`: Resumen por tipo y categoría

Ejemplos: `colombia_catalog.json`, `méxico_catalog.csv`, `chile_summary.csv`