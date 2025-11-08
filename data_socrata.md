# Datos Disponibles en Socrata

Socrata permite acceder a datasets públicos estructurados que organizaciones gubernamentales, ONGs y otros organismos publican en portales de datos abiertos.

## Tipos de Datos Publicados

| Categoría | Tipos de datos | Ejemplos |
|-----------|----------------|----------|
| **Gobierno & transparencia** | Contratos públicos, ejecutorias presupuestales, subvenciones, salarios | Portales gubernamentales con contratos y gastos públicos |
| **Transporte y movilidad** | Accidentes de tránsito, rutas de transporte público, geolocalización | Motor Vehicle Collisions (NYC Open Data) |
| **Seguridad pública** | Índices de criminalidad, llamadas de emergencia, reportes de delitos | Reportes policiales con ubicación y hora |
| **Medio ambiente** | Calidad del aire, niveles de contaminación, mediciones climáticas | Mapas de puntos geográficos con lat/long |
| **Salud pública** | Casos de enfermedades, vigilancia epidemiológica, indicadores clínicos | Datos de notificación obligatoria |
| **Educación** | Matrícula, resultados de evaluaciones, información por escuela | Datos por institución y resultados |
| **Datos geoespaciales** | Direcciones, coordenadas, límites administrativos, uso de suelo | GeoJSON y datos espaciales |
| **Economía y finanzas** | Indicadores macroeconómicos, comercio, tasas, precios | Impuestos locales, valuaciones catastrales |
| **Planeación urbana** | Permisos de construcción, uso del suelo, proyectos de obra pública | Edificaciones, zonas de desarrollo |
| **Catastro** | Avalúos catastrales, valores fiscales, identificación de predios | Consulta ciudadana y valuación |

## Características Técnicas

- **Estructura de tabla**: Filas y columnas con esquema definido (texto, número, fecha, geográfico)
- **Metadatos**: Nombre, descripción, fecha de actualización, licencias, columnas
- **Columnas geográficas**: Tipos `location`, `geo_point`, `geo_shape` para mapas
- **SoQL**: Query language similar a SQL para filtrar, ordenar y agrupar
- **Paginación**: `$limit`, `$offset` o parámetros `page`
- **Exportación**: JSON, CSV, GeoJSON, Excel
- **Versiones de API**: v2 (`/resource`) y v3 (`/api/v3/views`)
- **Acceso**: Público sin credenciales, token recomendado para evitar límites
- **Discovery API**: Búsqueda de datasets entre múltiples portales

## Ejemplos de Datasets

- **NYC Open Data**: Motor Vehicle Collisions – choques vehiculares con ubicación
- **Transporte USA**: Rutas, paradas, horarios GTFS
- **BTS**: Datos de transporte nacional con dashboards
- **Gobiernos locales**: Ingresos, gastos, permisos, licencias

## Aplicaciones

- Aplicaciones web y móviles
- Dashboards y visualizaciones
- Pipelines de análisis de datos
- Sistemas de monitoreo
- Servicios inteligentes