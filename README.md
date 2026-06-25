# Sistema de Información NovaFit Premium

Este repositorio contiene el código fuente para la gestión operativa de **NovaFit Premium**, un sistema diseñado bajo los principios de la Ingeniería de Software para la gestión de membresías, disciplinas, entrenamientos, seguimiento físico y administración financiera del gimnasio.

---

## 🛠️ Stack Tecnológico

El proyecto está estructurado como una aplicación desacoplada de alto rendimiento:
* **Backend:** Python (Django + Django REST Framework)
* **Frontend:** Vue 3 (Vite + Pinia + Vue Router)
* **Base de Datos:**
  * **Local:** SQLite (para agilidad de desarrollo)
  * **Producción:** PostgreSQL (desplegado en la nube)
* **Servidor de Producción:** Render.com (configurado vía `render.yaml`)

---

## 💻 Ejecución en el Entorno Local

Para ejecutar el frontend y el backend al mismo tiempo en tu máquina local, utiliza el lanzador automático de Windows:

1. Asegúrate de tener instalado Python 3.11+ y Node.js.
2. Abre una consola en la raíz del proyecto.
3. Ejecuta el archivo:
   ```bash
   run-local.bat
   ```
   *Alternativamente con npm:*
   ```bash
   npm run dev:local
   ```
4. El script abrirá automáticamente dos ventanas separadas:
   * **Backend API:** corriendo en `http://127.0.0.1:8000/api/`
   * **Frontend Web:** corriendo en `http://localhost:5173/`

---

## 🚀 Despliegue a Producción en un Solo Paso

El sistema está configurado para desplegarse automáticamente cuando se suben cambios a la rama `produccion` en GitHub.

Para empaquetar, confirmar tus cambios y publicarlos con un solo comando:

1. Ejecuta el script de despliegue en la raíz del proyecto:
   ```bash
   deploy.bat
   ```
   *Alternativamente con npm:*
   ```bash
   npm run deploy:prod
   ```
2. El script te solicitará un mensaje de commit.
3. Añadirá de forma automática tus archivos al área de preparación, creará el commit y los enviará (`git push origin HEAD:produccion`).
4. La plataforma Render.com detectará la actualización y desplegará la nueva versión de manera automática en segundo plano sin interrumpir el funcionamiento actual.

---

## 📂 Estructura del Código Fuente

* `/backend/`: Contiene la lógica del servidor estructurada en aplicaciones Django (`core`, `finanzas`, `actividades`, `api`).
* `/frontend/`: Contiene la aplicación cliente construida en Vue 3 con componentes y vistas dinámicas.
* `/documentacion/`: Contiene los planos de diseño del sistema, diagramas relacionales, diagramas de robustez (PlantUML) y la documentación de la arquitectura del proyecto.
