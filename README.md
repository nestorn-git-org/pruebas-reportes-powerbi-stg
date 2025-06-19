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

1. **Clona este repositorio utilizando SSH:**

   ```bash
   git@github.com:github_user/repositorio.git
   ```

2. **Instala las dependencias Python:**

   Se recomienda usar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

   El único requerimiento obligatorio es:
   ```
   ms-fabric-cli
   ```

3. **Verifica que tienes instalado Power BI Desktop** y acceso a una cuenta de Power BI Service.

---

## Configuración

1. **Actualiza el archivo de configuración del proyecto:**  
   Edita el archivo `config/config.json` con los siguientes datos:
   - src_name = Nombre del proyecto (nombre del archivo Power BI)
   - capacity = Capcidad Fabric (Si aplica)
   - develoment > workspace = espacio de trabajo `desarrollo`
   - production > workspace = espacio de trabajo `productivo`
   - semanticModelsParameters = conexión y parámetros del modelo semantico

---

## Estructura de carpetas [nombre-proyecto]

```bash
nombre-proyecto/
├── .github/                     # Workflows de GitHub Actions
│   └── workflow/
│      ├── bpa.yml
│      └── deploy.yml
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
- Por cada Pull Request o Push a la rama `develop`, se activa un pipeline en GitHub Actions que valida reglas de mejores prácticas usando la herramienta [PBI-Inspector](https://github.com/NatVanG/PBI-InspectorV2).
- Si pasan las pruebas y se hace merge, el pipeline despliega los artefactos en el workspace `*_Test` usando los parámetros de `config.json`.
- Una vez aprobado, se crea un Pull Request a la rama `main` y el pipeline despliega la versión final al workspace `Productivo`.

---

## Requisitos

- Acceso a Power BI Desktop y Power BI Service.
- Python 3.10+ y pip.
- SSH Authentication keys & Signing keys asociadas a tu cuenta de Github Enterprise.
- Opcional: Conocimientos básicos de GitFlow.

---

## Notas importantes

- Los scripts `bpa-report-rules.ps1` & `bpa-semantic-rules.ps1`) automatizan la  validación de mejores prácticas de los artefactos .Report & .SemanticModel.
- El script `deploy.py` automatiza el despliegue a los workspaces en Power BI Service.
- Consulta la documentación en `docs/` para detalles del reporte: tablas, medidas, modelo y lógica del negocio.

---

¿Tienes sugerencias o preguntas? Abre un issue o contacta a los responsable del repoitorio.