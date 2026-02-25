# TMDB Quiz Game 🎬

¡Bienvenido a **TMDB Quiz Game**! Un juego de preguntas y respuestas interactivo basado en la base de datos de películas **The Movie Database (TMDB)**. Pon a prueba tus conocimientos sobre cine, actores y directores.

## 🚀 Características

- **Preguntas Dinámicas:** Generación automática de preguntas sobre películas populares, actores y directores.
- **Apoyo Visual:** Incluye imágenes de los artistas para ayudar a identificarlos.
- **Sistema de Puntuación:** Gana 10 puntos por cada respuesta correcta.
- **Límite de Errores:** Tienes un máximo de 5 errores antes de que termine el juego. ¡Intenta conseguir la mayor puntuación posible!
- **Interfaz Moderna:** Diseño responsivo y atractivo con animaciones suaves.

## 🛠️ Tecnologías Utilizadas

- **Backend:** [Python](https://www.python.org/) con [Flask](https://flask.palletsprojects.com/).
- **Frontend:** HTML5, CSS3 (Custom Properties, Flexbox, Grid) y JavaScript (Vanilla JS).
- **API:** [The Movie Database (TMDB) API](https://www.themoviedb.org/documentation/api).
- **Librerías Python:** `requests` para las peticiones a la API.

## 📋 Requisitos Previos

Asegúrate de tener instalado:
- Python 3.x
- Una conexión a internet (para las peticiones a la API de TMDB).

## 🔧 Instalación y Configuración

1. **Clona el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd "quiz tmdb"
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuración de la API:**
   El proyecto utiliza la API de TMDB. Actualmente, el cliente tiene una clave de API configurada en `tmdb_client.py`. 
   > **Nota:** Se recomienda encarecidamente utilizar variables de entorno para manejar claves de API en producción.

4. **Ejecuta la aplicación:**
   ```bash
   python app.py
   ```

5. **¡Juega!**
   Abre tu navegador y ve a `http://127.0.0.1:5000`.

## 📂 Estructura del Proyecto

```text
├── app.py              # Servidor Flask y rutas de la API
├── tmdb_client.py      # Lógica de interacción con la API de TMDB
├── requirements.txt    # Dependencias del proyecto
├── static/
│   ├── script.js       # Lógica del juego en el cliente
│   └── style.css       # Estilos y diseño visual
├── templates/
│   └── index.html      # Estructura principal de la web
└── README.md           # Documentación del proyecto
```

## 🎮 Cómo Jugar

1. Haz clic en **"Comenzar Juego"**.
2. Lee la pregunta y observa la imagen (si está disponible).
3. Selecciona una de las opciones.
   - Si aciertas: El botón se pondrá verde y sumarás 10 puntos.
   - Si fallas: El botón se pondrá rojo, se mostrará la respuesta correcta y sumarás un error.
4. Tienes hasta 5 errores permitidos. Al llegar al límite, verás tu puntuación final y podrás reiniciar el juego.

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---
Desarrollado con ❤️ para los amantes del cine.
