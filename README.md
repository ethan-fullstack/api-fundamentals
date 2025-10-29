# api_fundamentals

Descripción

- Proyecto de ejemplo / plantilla para desarrollar APIs y practicar fundamentos de diseño, pruebas y despliegue.
- Incluye estructura modular para código de aplicación, pruebas automatizadas, configuración de linting/formatting y soporte para contenedores/CI.

Estado

- En desarrollo. Componentes principales y convenciones definidos; implementación de endpoints y pruebas pendientes según carpetas.

Requisitos

- Git
- Docker (opcional)
- pip / virtualenv

Versiones de Python soportadas

- Probado y soportado en Python 3.13.
- Se recomienda usar la versión más reciente disponible dentro de la serie 3.13+.

Estructura sugerida

- src/ — código fuente de la aplicación
- tests/ — pruebas unitarias e integración
- docs/ — documentación adicional
- Dockerfile — imagen para despliegue
- pyproject.toml / requirements.txt — dependencias y configuración de herramientas
- README.md — este archivo

Instalación (local)

1. Crear entorno virtual:
   - `python -m venv .venv`
   - `source .venv/bin/activate` (Linux/macOS) o `.venv\Scripts\activate` (Windows)
2. Instalar dependencias:
   - `pip install -r requirements.txt` o `pip install .` si está empaquetado

Pruebas y calidad

- Ejecutar pruebas:
  - `pytest`
- Linting / formateo sugerido:
  - `ruff`, `flake8`, `black`, `isort`
- Formato automático:
  - `black .` / `isort .`

CI / CD

- Añadir pipelines para:
  - ejecutar tests
  - chequeo de linting y formateo
  - construcción de imagen Docker y despliegue

Contribuciones

- Abrir issues y pull requests.
- Seguir convenciones de git commit y agregar pruebas para nuevas funcionalidades.

Licencia

- Añadir una licencia en función de la política del proyecto (por ejemplo MIT, Apache-2.0).

Notas

- Ajustar versiones y comandos según frameworks y dependencias concretas que se integren en el proyecto.
- Mantener README sincronizado con la estructura real del repositorio.
