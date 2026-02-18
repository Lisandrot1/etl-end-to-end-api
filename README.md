# ETL End-to-End Dos API

## 📋 Descripción del Proyecto

Este proyecto extrae diariamente datos del clima de múltiples ciudades desde una API externa, los transforma aplicando la arquitectura Medallion (Bronze → Silver → Gold) y los visualiza en un dashboard interactivo.

El proyecto está dividido en tres etapas bien definidas, cada una con su responsabilidad dentro del pipeline.

---

## 🏗️ Arquitectura
```
API del Clima
     │
     ▼
┌─────────────┐     ┌────────────────────────────────┐     ┌────────────────┐
│  Extracción │────▶│        MinIO (Data Lake)        │────▶│   Dashboard    │
│   Bronze    │     │  Bronze  │  Silver  │   Gold    │     │   Streamlit    │
└─────────────┘     └────────────────────────────────┘     │   + Plotly     │
                                                             │   + DuckDB     │
                                                             └────────────────┘
```

---

## 🗂️ Etapas del Proyecto

### Parte 1 — Planeación, Extracción y Carga a Bronze

En esta etapa se define la arquitectura del proyecto y se implementa la extracción de datos. Se consume una API del clima para obtener datos diarios de múltiples ciudades y se almacenan en la capa **Bronze** de MinIO en su formato crudo, sin transformaciones.

### Parte 2 — Transformación, Modelado y Carga a Silver/Gold

Se leen los datos crudos desde Bronze y se aplican transformaciones y limpiezas para cargarlos en la capa **Silver**. Luego se diseña e implementa un **modelo estrella** con tablas de hechos y dimensiones, y la data modelada se persiste en la capa **Gold**, lista para el consumo analítico.

### Parte 3 — Consumo y Visualización

Se utiliza **DuckDB** como motor SQL para consultar directamente los archivos de la capa Gold en MinIO, sin necesidad de mover los datos. Los resultados se visualizan en un dashboard construido con **Streamlit** y **Plotly**, mostrando la data del clima diaria con gráficos interactivos.

---

## 🔧 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

### 1. Docker Desktop
Docker Desktop es necesario para ejecutar los contenedores del proyecto.

- **¿No lo tienes instalado?** Descárgalo desde: [https://www.docker.com/get-started/](https://www.docker.com/get-started/)
- Sigue las instrucciones de instalación según tu sistema operativo

### 2. Git Bash (Windows)
Git Bash es necesario para clonar el repositorio y ejecutar comandos.

- **¿No lo tienes instalado?** Descárgalo desde: [https://git-scm.com/download/windows](https://git-scm.com/download/windows)
- En macOS y Linux, Git suele venir preinstalado

---

## 📥 Instalación

### Paso 1: Clonar el Repositorio

Abre tu terminal (Git Bash en Windows, Terminal en macOS/Linux) y ejecuta:
```bash
# Clona el repositorio
git clone https://github.com/Lisandrot1/etl-end-to-end-api.git

# Ingresa a la carpeta del proyecto
cd etl-end-to-end-api
```

### Paso 2: Levantar los Contenedores

Desde la carpeta del proyecto, ejecuta el siguiente comando:
```bash
docker compose up -d --build
```

Este comando:
- `docker compose up`: Levanta los servicios definidos en el archivo `docker-compose.yml`
- `-d`: Ejecuta los contenedores en segundo plano (modo detached)
- `--build`: Construye las imágenes antes de levantar los contenedores

---

## 🚀 Uso

### Acceder a MinIO

MinIO es el destino de almacenamiento de datos del ETL. Para acceder:

1. Abre tu navegador favorito
2. Navega a: [http://localhost:9001](http://localhost:9001)
3. Ingresa las credenciales:
   - **Usuario:** `admin`
   - **Contraseña:** `admin12345`

---

## 🚀 Cómo Ejecutar el ETL

### Ejecutar el Pipeline

Una vez que los contenedores estén levantados, ejecuta el siguiente comando en tu terminal:
```bash
docker compose run --rm etl
```

Este comando:
- `docker compose run`: Ejecuta un comando en un nuevo contenedor
- `--rm`: Elimina el contenedor automáticamente después de que termine la ejecución
- `etl`: Nombre del servicio a ejecutar

### Opciones para Monitorear la Ejecución

Tienes **dos formas** de verificar que el ETL se está ejecutando:

#### Opción 1: Ver los Logs en la Terminal
Observa directamente en la terminal los logs del proceso ETL mientras se ejecuta. Esto te permitirá:
- Ver el progreso en tiempo real
- Identificar cualquier error durante la ejecución
- Confirmar cuando el proceso finalice exitosamente

#### Opción 2: Verificar en MinIO
1. Dirígete a MinIO en tu navegador: [http://localhost:9001](http://localhost:9001)
2. Espera unos minutos (el tiempo depende del volumen de datos)
3. Refresca la página
4. Verifica que los datos se hayan cargado correctamente

---

## ✅ Verificar que el ETL se Ejecutó Correctamente

### Método 1: Verificar la Fecha de Ingreso de Datos

1. Accede a MinIO ([http://localhost:9001](http://localhost:9001))
2. Navega al bucket correspondiente
3. Verifica la hora de subida de los datos
4. Compara con la hora actual de tu PC

Si las horas coinciden (o son muy cercanas), significa que los datos se cargaron recientemente.

### Método 2: Revisar los Logs

1. Observa los logs en la terminal donde ejecutaste el comando
2. Espera a que el proceso termine completamente
3. Verifica que **no haya errores** en los logs
4. Una vez confirmado, dirígete a MinIO
5. Refresca la página para ver los cambios

---

## 📊 Ver el Dashboard

Una vez que el ETL haya finalizado correctamente, sigue estos pasos para visualizar los datos:

1. Abre tu navegador y navega a [http://localhost:8501](http://localhost:8501)
2. Si el ETL todavía está en ejecución, espera a que termine y luego **refresca la página**
3. El dashboard mostrará automáticamente la data del clima del día actual

> 💡 **Tip:** Puedes consultar datos de días anteriores usando el **filtro de fecha** disponible en el dashboard. Simplemente cambia la fecha a cualquier día previo para explorar el historial de datos cargados.

---

## 📝 Comandos Útiles
```bash
# Ver el estado de los contenedores
docker compose ps

# Ver los logs de los contenedores
docker compose logs -f

# Detener los contenedores
docker compose down

# Detener y eliminar volúmenes
docker compose down -v
```

---

## ⚠️ Solución de Problemas

### El puerto 9001 ya está en uso
Si recibes un error indicando que el puerto ya está ocupado:
```bash
# Verifica qué proceso está usando el puerto
netstat -ano | findstr :9001  # Windows
lsof -i :9001                  # macOS/Linux

# Detén el proceso o cambia el puerto en docker-compose.yml
```

### El dashboard no muestra datos
Asegúrate de haber ejecutado el pipeline al menos una vez. Si el bucket Gold está vacío, corre primero:
```bash
docker compose run --rm etl
```

Luego refresca el dashboard en [http://localhost:8501](http://localhost:8501).

### Docker Desktop no está ejecutándose
Asegúrate de que Docker Desktop esté abierto y corriendo antes de ejecutar los comandos.