# Reportes Power BI - Gitflow

Este repositorio es un ejemplo del proceso estándar de desarrollo y liberación de reportes Power BI, usando GitFlow, GitHub Actions y automatizaciones para mejores prácticas y despliegues.

---

## Tabla de Contenidos

- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura de Carpetas](#estructura-de-carpetas-dev-environment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Requisitos](#requisitos)
- [Notas importantes](#notas-importantes)

---

## Instalación

1. **Clona el repositorio se recomienda utilizar SSH:**

   ```bash
   git@github.com:github_user/repositorio.git
   ```

2. **Verifica disponibilidad:**

   ```bash
      - Power BI Desktop (versión igual o superior mayo 2025)
      - Power BI Service (https://app.powerbi.com/)
      ```

   ---

## Configuración

1. **Actualiza el archivo de configuración del proyecto:**  
   Edita el archivo `config/config.json` con los siguientes datos:
   - src_name = nombre del proyecto (nombre del archivo Power BI)
   - capacity = capcidad Fabric (Si aplica)
   - development > workspace = espacio de trabajo `desarrollo`
   - production > workspace = espacio de trabajo `productivo`
   - semanticModelsParameters = conexión y parámetros del modelo semantico (Si aplica)

---

## Estructura de carpetas [nombre-proyecto]

```bash
nombre-proyecto/
├── .github/                     # Workflows de GitHub Actions
│   └── workflow/
│      └── CICD.yaml
├── config/                      # Configuración del proyecto (config.json)
├── docs/                        # Documentación
├── scripts/                     # Scripts de automatización
│   ├── bpa-report-rules.ps1         
│   ├── bpa-semantic-rules.ps1          
│   ├── deploy.py
│   └── utils.py
├── src/                         # Código fuente [.pbip]
│   ├── <nombre-proyecto>.Report
│   └── <nombre-proyecto>.SemanticModel
├── tests/                       # Pruebas automatizadas
│   ├── bpa-report-rules.json
│   └── bpa-semantic-rules.json
└── requirements.txt             # Dependencias Python
└── README.md                    # Instrucciones
```

---

## CI/CD Pipeline

- Los proyectos de Power BI se guardan en la carpeta `src` con las extensiones `.Report` y `.SemanticModel`.
- La implementación de nuevas funciones se realiza en la rama `develop`.
- Por cada Pull Request a la rama `develop`, se ejecuta el Pipeline:
   - Setup Configuration.
   - Power BI Best Pratices Analysis ([PBI-Inspector](https://github.com/NatVanG/PBI-InspectorV2)).
   - Deploy to Develoment.
- Completada las pruebas y aprobado el merge, el pipeline despliega nuevamente los artefactos en el workspace `*_Test`.
- Una vez confirmada la versión definitiva (Release) se crea un Pull Request en la rama `main`, se el ejecuta el Pipeline para desplegar al workspace `Productivo`.

---
## Notas importantes

- Los scripts `bpa-report-rules.ps1` & `bpa-semantic-rules.ps1`) automatizan la  validación de mejores prácticas de los artefactos .Report & .SemanticModel.
- El script `deploy.py` automatiza el despliegue a los workspaces en Power BI Service.
- Consulta la documentación en `docs/` para detalles del reporte: tablas, medidas, modelo y lógica del negocio.

---

¿Tienes sugerencias o preguntas? Abre un issue o contacta a los responsable del repositorio.
