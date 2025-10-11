# Datos disponibles en Socrata

Con Socrata puedes acceder a datasets públicos estructurados que organizaciones gubernamentales, ONGs y otros organismos ya han publicado en portales de datos abiertos. A continuación detallo qué tipo de datos suelen estar disponibles, ejemplos concretos y las características que hacen que esos datos sean consumibles.

## ¿Qué tipo de datos se publican en Socrata?

Socrata es una plataforma de catálogo de datos abiertos (Open Data) que permite a entidades públicas subir datos, exponerlos con APIs y construir visualizaciones; los datos públicos pueden incluir:

| Categoría | Tipos de datos frecuentes | Ejemplos específicos |
|-----------|---------------------------|---------------------|
| **Gobierno & transparencia** | Contratos públicos, ejecutorias presupuestales, subvenciones, salarios de funcionarios | Los portales de gobierno estatal o municipal suelen usar Socrata para mostrar contratos o gastos públicos. |
| **Transporte y movilidad** | Accidentes de tránsito, rutas de transporte público, tiempos de llegada, geolocalización de vehículos | Ejemplo: el dataset "Motor Vehicle Collisions – Crashes" del portal de Nueva York, actualizado continuamente via Socrata, permite mapear choques vehiculares recientes. |
| **Seguridad pública** | Índices de criminalidad, llamadas de emergencia, reportes de delitos por ubicación | Muchos portales de ciudades en EE. UU. exponen reportes policiales con ubicación y hora. |
| **Medio ambiente y salud ambiental** | Calidad del aire, niveles de contaminación, mediciones climáticas, estaciones meteorológicas | Socrata permite mapas de puntos geográficos si el dataset incluye campos de latitud/longitud. |
| **Salud pública y epidemiología** | Casos de enfermedades, vigilancia epidemiológica, indicadores clínicos agregados | Entidades de salud pueden exponer datos de notificación obligatoria. |
| **Educación** | Matrícula, resultados de evaluaciones estandarizadas, información por escuela | Las entidades educativas pueden publicar datos por institución, localización y resultados por materia. |
| **Datos geoespaciales / GIS** | Direcciones, coordenadas geográficas, límites administrativos, mapas de uso de suelo | Soporta formatos geo (GeoJSON y datos espaciales) en visualizaciones de mapas. |
| **Economía y finanzas** | Indicadores macroeconómicos, estadísticas de comercio, tasas de interés locales, precios de bienes | Algunas ciudades exponen datos de impuestos locales, valuaciones catastrales, ingresos y gastos. |
| **Planeación urbana / infraestructura** | Permisos de construcción, uso del suelo, proyectos de obra pública, planeamiento territorial | Los datos de edificaciones, zonas de desarrollo y autorizaciones están entre los más comunes. |
| **Catastro y propiedades** | Avalúos catastrales, valores fiscales, identificación de predios | Datos públicos catastrales pueden exponerse para consulta ciudadana o aplicaciones de valuación. |

## Características técnicas que definen los datos accesibles

Para que los datos sean consumibles vía Socrata, deben cumplir características específicas:

- **Estructura de tabla**: Filas y columnas. Cada dataset es una tabla con un esquema de columnas (tipo de campo: texto, número, fecha, geográfico, etc.). La API de Socrata interpreta esos campos.

- **Metadatos**: Cada dataset acompaña metadatos como nombre, descripción, fecha de última actualización, licencias, columnas, etc. La API también permite consultarlos.

- **Columnas geográficas**: Para permitir mapas, muchas tablas incluyen columnas tipo `location` (latitud/longitud), `geo_point` o `geo_shape`. Sin eso, no se pueden visualizar como mapas automáticamente.

- **SoQL (Socrata Query Language)**: Permite filtrar, ordenar, agrupar, sumarizar datos directamente desde la API, como si se tratara de SQL adaptado a datasets públicos.

- **Paginación / límites**: Los datos se entregan en bloques (`$limit`, `$offset` o usando parámetros de paginación tipo `page`) para evitar respuestas masivas en una sola petición.

- **Opciones de exportación**: Además de JSON, muchos portales permiten exportar CSV, GeoJSON, Excel, etc.

- **Versiones de API / endpoints**: Socrata tiene versiones como "v2" o "v3" (por ejemplo endpoints `/resource` o `/api/v3/views/.../query`) dependiendo de la configuración del portal.

- **Acceso público vs. autenticado**: La mayoría de los datasets son públicos y no requieren credenciales, aunque para evitar límites de tasa se recomienda usar un "app token". Para acciones de escritura o modificación se requiere autenticación con permisos especiales.

- **Descubrimiento global**: Socrata ofrece APIs de descubrimiento (Discovery API) para buscar catálogos de datasets entre múltiples portales. También alimenta el Open Data Network que centraliza búsquedas de datasets entre muchos catálogos que usan Socrata.

## Ejemplos concretos de datasets Socrata accesibles públicamente

- **Motor Vehicle Collisions – Crashes (NYC Open Data)**: Dataset que informa choques vehiculares recientes con ubicación, fecha, tipo de colisión. Usado para mapas interactivos.

- **Portal de transporte público de EE. UU.**: Muchos sistemas usan Socrata para exponer rutas, paradas, horarios (GTFS) o datos dinámicos de llegadas.

- **Plataforma del Bureau of Transportation Statistics (BTS)**: Usa Socrata para publicar datos de transporte nacional con API pública y dashboards; datos actualizados continuamente.

- **Catálogos estatales y municipales**: Muchos gobiernos estatales (EE. UU.) usan Socrata para exponer datos de ingresos, gastos, permisos, licencias y obras públicas.

## En resumen

Con Socrata puedes acceder a una amplia variedad de datos abiertos estructurados en temas como:

- **Gobierno** y transparencia
- **Transporte** y movilidad  
- **Medio ambiente** y salud
- **Educación** y servicios públicos
- **Catastro** e infraestructura

Los datasets típicamente tienen columnas de tipo numérico, texto, fecha y geoespacial, lo que permite consultas sofisticadas mediante **SoQL**. Gracias a la compatibilidad con exportación en múltiples formatos y la capacidad de filtrado/agrupamiento desde la API, estos datos pueden integrarse en:

- Aplicaciones web y móviles
- Dashboards y visualizaciones
- Pipelines de datos para análisis
- Sistemas de monitoreo
- Servicios inteligentes

---

> **Nota**: Para obtener un listado actualizado de los datasets disponibles en Socrata para Colombia o Latinoamérica, incluyendo URLs específicas y tipos de datos por región, se puede consultar directamente el portal de datos abiertos de cada país o utilizar la Discovery API de Socrata.