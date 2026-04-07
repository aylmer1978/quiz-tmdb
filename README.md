# TMDB Quiz Game 🎬

¡Bienvenido a **TMDB Quiz Game**! Un juego de preguntas y respuestas interactivo basado en la base de datos de películas **The Movie Database (TMDB)**. Pon a prueba tus conocimientos sobre cine, actores y directores.

## 🚀 Características

- **Preguntas Dinámicas:** Generación automática de preguntas sobre películas populares, actores y directores.
- **Apoyo Visual:** Incluye imágenes de los artistas para ayudar a identificarlos en preguntas sobre sus carreras.
- **Variedad de Retos:** Preguntas sobre fechas de estreno, valoraciones, presupuestos y filmografías.
- **Sistema de Puntuación:** Gana 10 puntos por cada respuesta correcta.
- **Límite de Errores:** Tienes un máximo de 5 errores antes de que termine el juego. ¡Intenta conseguir la mayor puntuación posible!
- **Interfaz Moderna:** Diseño responsivo y atractivo con animaciones suaves y modo oscuro integrado.

## 🛠️ Tecnologías Utilizadas

- **Backend:** [Python](https://www.python.org/) con [Flask](https://flask.palletsprojects.com/).
- **Frontend:** HTML5, CSS3 (Custom Properties, Flexbox, Grid) y JavaScript (Vanilla JS).
- **API:** [The Movie Database (TMDB) API](https://www.themoviedb.org/documentation/api).
- **Librerías Python:** `requests` para las peticiones a la API.

## 📋 Requisitos Previos

Asegúrate de tener instalado:
- Python 3.x
- Una conexión a internet (para las peticiones a la API de TMDB).
- Una clave de API de TMDB (opcional, pero recomendada para desarrollo propio).

## 🔧 Instalación y Configuración

1. **Clona el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd quiz-tmdb
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuración de la API:**
   El proyecto utiliza la API de TMDB. Actualmente, el cliente tiene una clave de prueba en `tmdb_client.py`.
   
   **Recomendación de Seguridad:** Para usar tu propia clave, puedes configurar una variable de entorno:
   ```bash
   # En Linux/macOS
   export TMDB_API_KEY="tu_clave_aqui"
   
   # En Windows (PowerShell)
   $env:TMDB_API_KEY="tu_clave_aqui"
   ```

4. **Ejecuta la aplicación:**
   ```bash
   python app.py
   ```

5. **¡Juega!**
   Abre tu navegador y ve a `http://127.0.0.1:5000`.

## 📂 Estructura del Proyecto

```text
├── app.py              # Servidor Flask y rutas de la API
├── tmdb_client.py      # Lógica de interacción con la API de TMDB y generación de preguntas
├── requirements.txt    # Dependencias del proyecto
├── static/
│   ├── script.js       # Lógica del juego y gestión del estado en el cliente
│   └── style.css       # Estilos, variables CSS y diseño visual
├── templates/
│   └── index.html      # Estructura principal de la aplicación web
└── README.md           # Documentación del proyecto
```

## ⚙️ Cómo Funciona

El backend selecciona aleatoriamente entre 5 tipos de preguntas:
1. **Estrenos:** ¿En qué año se estrenó [Película]?
2. **Valoraciones:** ¿Cuál es la puntuación de [Película] en TMDB?
3. **Actores:** ¿En qué película aparece [Actor]? (Incluye foto del actor).
4. **Directores:** ¿Qué película ha dirigido [Director]? (Incluye foto del director).
5. **Presupuesto:** ¿Qué película tuvo un presupuesto de [Monto]?

Las opciones incorrectas se generan dinámicamente basándose en otras películas populares para asegurar que el reto sea interesante.

## 🔮 Próximas Mejoras

- [ ] Soporte para múltiples idiomas (actualmente en Español).
- [ ] Tabla de clasificación (Leaderboard) local o global.
- [ ] Temporizador por pregunta para aumentar la dificultad.
- [ ] Categorías seleccionables (solo terror, clásicos, etc.).

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---
Desarrollado con ❤️ para los amantes del cine.
