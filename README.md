# Data Open - Herramientas para Datos Abiertos LATAM

Herramientas y documentación para descubrir, consultar y exportar catálogos de datos abiertos en Latinoamérica usando APIs Socrata y CKAN.

## Problema que resuelve

En la práctica, cada país publica datos en plataformas distintas y con estructuras de API diferentes.
Eso dificulta crear un inventario regional consistente para análisis, transparencia, periodismo de datos o monitoreo de políticas públicas.

Este repositorio unifica ese acceso en un flujo único que:

1. Consulta portales multi-país (Socrata y CKAN) con una interfaz común.
2. Normaliza metadatos clave de datasets en una estructura homogénea.
3. Exporta resultados en formatos listos para análisis (JSON y CSV).
4. Genera un resumen agregado por tipo y categoría para exploración rápida.

## Ámbitos de aplicación

- Gobierno abierto y transparencia.
- Investigación académica y análisis de políticas públicas.
- Periodismo de datos.
- Observatorios ciudadanos y ONGs.
- Equipos de analítica que construyen pipelines sobre fuentes públicas.
- Integración de catálogos de datos en productos de inteligencia de negocio.

## Casos de uso

1. Inventariar datasets públicos por país para una línea base regional.
2. Filtrar datasets por periodo de publicación para análisis longitudinal.
3. Buscar catálogos por palabra clave (por ejemplo, salud, educación, seguridad).
4. Extraer datos normalizados para alimentar notebooks, ETL o dashboards.
5. Comparar cobertura temática entre países por categorías y tipo de dataset.
6. Construir monitoreo periódico de nuevos datasets abiertos.

## 📁 Estructura del proyecto

```
data-open/
├── README.md                    # Este archivo
├── secretos.json.example        # Plantilla de configuración
├── data_socrata.md             # Documentación de Socrata API
├── uso_api_socrata.md          # Guía de uso de Socrata
└── descubrimiento/             # Sistema de descubrimiento multi-país
    ├── README.md               # Documentación del módulo
    ├── requirements.txt        # Dependencias Python
    ├── config.json            # Configuración de fechas
    ├── latam_domains.json     # Configuración de países
    ├── run_discovery.py       # CLI principal
    ├── socrata_discovery.py   # Cliente Socrata
    └── ckan_client.py         # Cliente CKAN
```

## 🚀 Inicio rápido

### 1. Configurar entorno
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
cd descubrimiento
pip install -r requirements.txt
```

### 2. Configurar credenciales
```bash
# Copiar plantilla de configuración
cp secretos.json.example secretos.json

# Editar secretos.json con tus credenciales
# Solo necesitas el token de Socrata para Colombia
```

### 3. Ejecutar descubrimiento
```bash
# Consultar todos los países con límite de 10 registros
python run_discovery.py --limit 10

# Consultar país específico
python run_discovery.py --country COL --published-from 2024-01-01

# Ver todas las opciones
python run_discovery.py --help
```

La salida del CLI ahora incluye métricas por país:

1. Tiempo de ejecución por país (segundos).
2. Número de requests HTTP realizados.
3. Número de reintentos HTTP observados.
4. Registros filtrados y tasa porcentual de filtrado.

### 4. Ejecutar pruebas básicas
```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Cómo funciona la arquitectura

1. [descubrimiento/run_discovery.py](descubrimiento/run_discovery.py) orquesta ejecución, filtros y exportación.
2. [descubrimiento/socrata_discovery.py](descubrimiento/socrata_discovery.py) consulta Discovery API de Socrata.
3. [descubrimiento/ckan_client.py](descubrimiento/ckan_client.py) consulta package_search de CKAN.
4. [descubrimiento/latam_domains.json](descubrimiento/latam_domains.json) define países, plataforma y endpoints.
5. [descubrimiento/config.json](descubrimiento/config.json) permite parametrizar fechas por defecto.

## 🌎 Países soportados

| País | Código | Plataforma | Portal | Estado |
|------|--------|------------|---------|--------|
| 🇨🇴 Colombia | COL | Socrata | www.datos.gov.co | ✅ Funcional |
| 🇲🇽 México | MEX | CKAN | datos.gob.mx | ✅ Funcional |
| 🇨🇱 Chile | CHL | CKAN | datos.gob.cl | ✅ Funcional |
| 🇪🇨 Ecuador | ECU | CKAN | datosabiertos.gob.ec | ✅ Funcional |

## 📚 Documentación

- **[Descubrimiento LATAM](descubrimiento/README.md)**: Sistema multi-país para inventario de datasets
- **[Socrata API](data_socrata.md)**: Documentación técnica de Socrata
- **[Uso Socrata](uso_api_socrata.md)**: Guía práctica de uso

## Mejoras y optimizaciones implementadas

1. Robustez HTTP: se incorporó reutilización de sesión y reintentos automáticos para reducir fallos transitorios (429/5xx) en Socrata y CKAN.
2. Rendimiento de red: se evita abrir conexiones nuevas por cada request, mejorando tiempos de ejecución en paginación extensa.
3. Consistencia de credenciales: se corrigió la lectura del token para soportar la clave socrata_app_token del archivo [secretos.json.example](secretos.json.example).
4. Calidad de datos: se agregó deduplicación de resultados por identificador y enlace permanente antes de exportar.
5. Portabilidad de archivos: los nombres de salida se normalizan a ASCII para evitar problemas entre sistemas de archivos.

## Limitaciones actuales

1. El modelo de metadatos es una normalización mínima y no cubre todos los campos nativos de cada portal.
2. El filtro por fecha depende de la disponibilidad y formato de publication_date en cada API.
3. No incluye aún un pipeline incremental (delta) ni programación automática por cron.

## 🔧 Configuración

### Credenciales (secretos.json)
```json
{
  "socrata_app_token": "tu_token_aqui"
}
```

### Filtros de fecha (config.json)
```json
{
  "published_from": "2024-01-01",
  "published_to": "2025-12-31"
}
```

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

**Nota**: La rama `master` está protegida y requiere aprobación de @lraigosov.