# Documentación de la API

# Instrucciones de Configuración y Ejecución

Este proyecto fue desarrollado en Python 3.9. A continuación, se detallan las recomendaciones para configurar y ejecutar el proyecto de manera óptima:

## Entorno Virtual

Se recomienda encarecidamente utilizar un entorno virtual para evitar conflictos entre las dependencias de este proyecto y otras aplicaciones Python en su sistema. Puede crear un entorno virtual ejecutando el siguiente comando en la línea de comandos:

python3 -m venv nombre_del_entorno

## Activación del Entorno Virtual

**En Windows:**

`bash
nombre_del_entorno\Scripts\activate`

## Usuarios

### Obtener lista de usuarios

- **Endpoint:** `/api/users`
- **Método:** `GET`
- **Descripción:** Retorna la lista de todos los usuarios.

### Obtener usuario por ID

- **Endpoint:** `/api/users/<int:user_id>`
- **Método:** `GET`
- **Parámetros:**
  - `user_id`: ID único del usuario
- **Descripción:** Retorna la información de un usuario específico según su ID.

### Registrar nuevo usuario

- **Endpoint:** `/api/users`
- **Método:** `POST`
- **Parámetros (en formato JSON):**
  - `username`: Nombre de usuario
  - `email`: Correo electrónico
  - `password`: Contraseña
- **Descripción:** Registra un nuevo usuario en el sistema.

### Registrar nuevo usuario Admin

- **Endpoint:** `/api/useradmin`
- **Método:** `POST`
- **Parámetros (en formato JSON):**
  - `username`: Nombre de usuario
  - `email`: Correo electrónico
  - `password`: Contraseña
- **Descripción:** Registra un nuevo usuario con privilegios de administrador en el sistema.

### Iniciar sesión

- **Endpoint:** `/api/login`
- **Método:** `POST`
- **Parámetros (en formato JSON):**
  - `email`: Correo electrónico
  - `password`: Contraseña
- **Descripción:** Inicia sesión y retorna un token JWT para autenticación posterior.

### Cerrar sesión

- **Endpoint:** `/api/logout`
- **Método:** `GET`
- **Descripción:** Cierra la sesión actual del usuario autenticado.

## Datos

### Obtener lista de prediction_data

- **Endpoint:** `/api/datos`
- **Método:** `GET`
- **Descripción:** Retorna la lista de datos de predicción.

### Registrar nuevos datos

- **Endpoint:** `/api/datos`
- **Método:** `POST`
- **Parámetros (en formato JSON):**
  - Varios campos con datos específicos (ver descripción)
- **Descripción:** Registra nuevos datos en el sistema y actualiza el archivo CSV.

## Modelos

### Obtener resultados del modelo de Árboles de Decisión

- **Endpoint:** `/api/resultado_arbolesdecicion`
- **Método:** `GET`
- **Descripción:** Retorna los resultados del modelo de Árboles de Decisión, incluyendo el reporte de clasificación y la precisión del modelo. También indica si el usuario se inscribirá o no.

### Obtener resultados del modelo de Redes Neuronales

- **Endpoint:** `/api/resultados_redesneuronales`
- **Método:** `GET`
- **Descripción:** Retorna los resultados del modelo de Redes Neuronales, incluyendo el reporte de clasificación y la precisión del modelo. También indica si el usuario se inscribirá o no.
