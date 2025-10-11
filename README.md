# Data Open - Herramientas para Datos Abiertos LATAM

Este repositorio contiene herramientas y documentación para trabajar con portales de datos abiertos de Latinoamérica.

## 📁 Estructura del proyecto

```
data-open/
├── README.md                    # Este archivo
├── .gitignore                   # Archivos ignorados por Git  
├── secretos.json.example        # Plantilla de configuración
├── secretos.json               # Credenciales (ignorado por Git)
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

# Consultar país específico con filtro de fecha
python run_discovery.py --country COL --published-from 2024-01-01

# Ver todas las opciones
python run_discovery.py --help
```

## 🌎 Países soportados

| País | Código | Plataforma | Portal | Estado |
|------|--------|------------|---------|--------|
| 🇨🇴 Colombia | COL | Socrata | www.datos.gov.co | ✅ Funcional |
| 🇲🇽 México | MEX | CKAN | datos.gob.mx | ✅ Funcional |
| 🇨🇱 Chile | CHL | CKAN | datos.gob.cl | ✅ Funcional |
| 🇪🇨 Ecuador | ECU | CKAN | datosabiertos.gob.ec | ✅ Funcional |
| 🇵🇪 Perú | PER | DKAN/Custom | datosabiertos.gob.pe | ⚠️ Requiere desarrollo |
| 🇧🇷 Brasil | BRA | Custom | dados.gov.br | ⚠️ Requiere desarrollo |

## 📚 Documentación

- **[Descubrimiento LATAM](descubrimiento/README.md)**: Sistema multi-país para inventario de datasets
- **[Socrata API](data_socrata.md)**: Documentación técnica de Socrata
- **[Uso Socrata](uso_api_socrata.md)**: Guía práctica de uso

## 🔧 Configuración avanzada

### Credenciales (secretos.json)
```json
{
  "socrata_app_token": "tu_token_aqui",
  "socrata_username": "opcional@example.com", 
  "socrata_password": "opcional_para_consultas_publicas"
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
2. Crear rama de feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit de cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para detalles.

## 🏗️ Roadmap

- [ ] Integración con Perú (DKAN)
- [ ] Integración con Brasil (plataforma custom)
- [ ] Dashboard web para visualización
- [ ] API REST para consultas
- [ ] Integración con más países LATAM