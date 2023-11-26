# Instrucciones de Configuración y Ejecución

Este proyecto fue desarrollado en Python 3.9. A continuación, se detallan las recomendaciones para configurar y ejecutar el proyecto de manera óptima:

## Entorno Virtual

Se recomienda encarecidamente utilizar un entorno virtual para evitar conflictos entre las dependencias de este proyecto y otras aplicaciones Python en su sistema. Puede crear un entorno virtual ejecutando el siguiente comando en la línea de comandos:

```python
python -m venv nombre_del_entorno
```

## Activación del Entorno Virtual

**En Windows:**

```bash
nombre_del_entorno\Scripts\activate
```

**En macOS y Linux:**
```bash
source nombre_del_entorno/bin/activate
```

## Instalación de Dependencias
Una vez que el entorno virtual esté activado, instale las dependencias del proyecto utilizando el archivo requirements.txt. Ejecute el siguiente comando en la línea de comandos:

```python
pip install -r requirements.txt
```
Este comando instalará todas las bibliotecas y paquetes necesarios para ejecutar la aplicación.

## Nota Importante

Asegúrese de estar utilizando Python 3.9 o una versión superior para garantizar la compatibilidad con las dependencias.

## Ejecución del Proyecto

Después de configurar el entorno virtual y haber instalado las dependencias, puede ejecutar la aplicación. Utilice el siguiente comando en la línea de comandos:

```python
python AlmacenamientoDatos.py
```
La aplicación Flask se ejecutará localmente y estará disponible en http://localhost:5000/. Puede acceder a los diferentes endpoints según la documentación proporcionada en la sección correspondiente del README.

# Endpoints de la API

## Nota Importante

Para acceder a las rutas que requieren autenticación, sigue estos pasos:

1. Inicia sesión con un usuario registrado para obtener un token de autenticación.

2. Utiliza el token generado durante el inicio de sesión para acceder a las rutas que requieren autenticación.

3. Incluye el token en el encabezado de la solicitud de la siguiente manera:

    - **Key (Clave):** `Authorization`
    - **Value (Valor):** `Bearer tokengeneradoaliniciarseccion`

Este proceso garantiza que solo los usuarios autenticados y autorizados tengan acceso a las funciones protegidas de la aplicación, proporcionando un nivel adicional de seguridad y control en el manejo de datos y recursos.

## PRODUCION

Ya la api se puede acceder a ella mediante un dominio aunque tambien se puede acceder a ella instalandola de manera local con los pasos anteriormente explicados.

- *URL:* https://aerlonieapi.shop/

## Usuarios

### Obtener lista de usuarios

- **Endpoint:** `/api/users`
- **Método:** `GET`
- **Descripción:** Retorna la lista de todos los usuarios.
- **Autenticación:**  No se requiere.

### Obtener usuario por ID

- **Endpoint:** `/api/users/<int:user_id>`
- **Método:** `GET`
- **Parámetros:**
  - `user_id`: ID único del usuario
- **Descripción:** Retorna la información de un usuario específico según su ID.
- **Autenticación:**  No se requiere.

### Registrar nuevo usuario

- **Endpoint:** `/api/users`
- **Método:** `POST`
- **Parámetros (en formato JSON):**
  - `username`: Nombre de usuario
  - `email`: Correo electrónico
  - `password`: Contraseña
- **Descripción:** Registra un nuevo usuario en el sistema.
- **Autenticación:**  No se requiere.
- **Ejemplo:**
```json
{
  "username": "user",
  "email": "user@example.com",
  "password": "user_password"
}
```

### Registrar nuevo usuario Admin

- **Endpoint:** `/api/useradmin`
- **Método:** `POST`
- **Parámetros (en formato JSON):**
  - `username`: Nombre de usuario
  - `email`: Correo electrónico
  - `password`: Contraseña
- **Descripción:** Registra un nuevo usuario con privilegios de administrador en el sistema.
- **Autenticación:**  No se requiere.
- **Ejemplo:**
```json
{
  "username": "admin_user",
  "email": "admin@example.com",
  "password": "admin_password"
}
```

### Iniciar sesión

- **Endpoint:** `/api/login`
- **Método:** `POST`
- **Parámetros (en formato JSON):**
  - `email`: Correo electrónico
  - `password`: Contraseña
- **Descripción:** Inicia sesión y retorna un token JWT para autenticación posterior.
- **Autenticación:**  No se requiere.
- **Ejemplo:**
```json
{
  "email": "user@example.com",
  "password": "user_password"
}
```
### Cerrar sesión

- **Endpoint:** `/api/logout`
- **Método:** `GET`
- **Descripción:** Cierra la sesión actual del usuario autenticado.
- **Autenticación:**  Se requiere un token JWT.

## Datos

### Obtener lista de prediction_data

- **Endpoint:** `/api/datos`
- **Método:** `GET`
- **Descripción:** Retorna la lista de datos de predicción.
- **Autenticación:**  Se requiere un token JWT.

### Registrar nuevos datos

- **Endpoint:** `/api/datos`
- **Método:** `POST`
- **Parámetros (en formato JSON):**
  - `user_id`: ID único del usuario.
  - `first_open`: Primera apertura de la aplicación.
  - `dayofweek`: Día de la semana.
  - `hour`: Hora de registro.
  - `age`: Edad del usuario.
  - `screen_list`: Lista de pantallas visualizadas.
  - `numscreens`: Número de pantallas visualizadas.
  - `minigame`: Indicador de participación en minijuegos.
  - `used_premium_feature`: Indicador de uso de funciones premium.
  - `enrolled`: Indicador de inscripción.
  - `enrolled_date`: Fecha de inscripción.
  - `liked`: Indicador de "me gusta".
- **Descripción:** Registra nuevos datos en el sistema y actualiza el archivo CSV.
- **Autenticación:** Se requiere un token JWT.
- **Ejemplo:**
```json
 {
  "user_id": 123,
  "first_open": "2013-04-26 18:22:16.013",
  "dayofweek": 1,
  "hour": "08:00:00",
  "age": 25,
  "screen_list": "Home, Profile, Settings",
  "numscreens": 3,
  "minigame": 1,
  "used_premium_feature": 0,
  "enrolled": 1,
  "enrolled_date": "2013-04-26 18:31:58.923",
  "liked": 1
}
```

## Modelos

### Obtener resultados del modelo de Árboles de Decisión

- **Endpoint:** `/api/resultado_arbolesdecicion`
- **Método:** `GET`
- **Descripción:** Retorna los resultados del modelo de Árboles de Decisión, incluyendo el reporte de clasificación y la precisión del modelo. También indica si el usuario se inscribirá o no.
- **Autenticación:**  Se requiere un token JWT.

### Obtener resultados del modelo de Redes Neuronales

- **Endpoint:** `/api/resultados_redesneuronales`
- **Método:** `GET`
- **Descripción:** Retorna los resultados del modelo de Redes Neuronales, incluyendo el reporte de clasificación y la precisión del modelo. También indica si el usuario se inscribirá o no.
- **Autenticación:**  Se requiere un token JWT.
