import datetime
from inspect import indentsize
import pandas as pd
import secrets
from flask import Flask, request, jsonify, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS 
from supabase import create_client
# Crear una instancia de la aplicación Flask
app = Flask(__name__)
CORS(app) # Aplica CORS a la aplicación
# Configurar la clave secreta de la aplicación y la clave secreta para JWT
app.secret_key = secrets.token_urlsafe(32)
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)

# Configurar el sistema de gestión de tokens JWT
jwt = JWTManager(app)

# Configuración de las credenciales de Supabase
SUPABASE_URL = "https://pxgrdafxraqxgddiikvl.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB4Z3JkYWZ4cmFxeGdkZGlpa3ZsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTk5MDUyNTIsImV4cCI6MjAxNTQ4MTI1Mn0.dX604vMo1TRi5MvY_j2GAM1My3oV0MmqrSIuOWGG5Pc" 
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Ruta para obtener la lista de usuarios
@app.route('/api/users', methods=['GET'])
def obtener_usuarios():
    try:
        response = supabase.table("users").select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)})
    
# Ruta para obtener un usuario por su ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def obtener_usuario_por_id(user_id):
    try:
        response = supabase.table("users").select("*").eq('user_id', user_id).execute()
        if response.data:
            # Si se encuentra el usuario, retornar sus datos
            return jsonify(response.data[0])
        else:
            # Si no se encuentra el usuario, retornar un mensaje de error
            return jsonify({"mensaje": "Usuario no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Ruta para registrar un nuevo usuario
@app.route('/api/users', methods=['POST'])
def registrar_usuario():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Registrarse en el servicio de autenticación de Supabase
        supabase.auth.sign_up({"email": email, "password": password})

        # Crear un nuevo usuario y almacenarlo en la base de datos
        nuevo_usuario = {
            "username": username,
            "email": email,
            "password": password,
            "is_admin": False,
        }
        supabase.table("users").upsert([nuevo_usuario]).execute()

        return jsonify({"mensaje": "Usuario registrado con éxito"})
    except Exception as e:
        return jsonify({"error": str(e)})
    

# Ruta para registrar un nuevo usuario Adnin
@app.route('/api/useradmin', methods=['POST'])
def registrar_usuarioadmin():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

       # Registrarse en el servicio de autenticación de Supabase
        supabase.auth.sign_up({"email": email, "password": password})

        # Crear un nuevo usuario y almacenarlo en la base de datos
        nuevo_usuario = {
            "username": username,
            "email": email,
            "password": password,
            "is_admin": True,
        }
        supabase.table("users").upsert([nuevo_usuario]).execute()

        return jsonify({"mensaje": "Usuario Admin registrado con éxito"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
# Ruta para iniciar sesión y obtener un token JWT
@app.route('/api/login', methods=['POST'])
def iniciar_sesion():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Autenticar al usuario utilizando el servicio de autenticación de Supabase
        supabase.auth.sign_in_with_password({"email": email, "password": password})

        # Obtener la información del usuario, incluyendo el nombre y el ID
        usuario_info = supabase.table("users").select("user_id", "username", "is_admin").match({'email': email}).execute()
        usuario_data = usuario_info.data[0] if usuario_info.data else None

        # Crear un token JWT para el usuario autenticado y darle tiempo de expiración a 1 hora
        access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(seconds=3600))

        # Almacenar el token en la variable de sesión (opcional)
        session['access_token'] = access_token

        return jsonify({
            "mensaje": "Usuario autenticado con éxito",
            "access_token": access_token,
            "user_id": usuario_data['user_id'] if usuario_data else None,
            "username": usuario_data['username'] if usuario_data else None,
            "is_admin": usuario_data['is_admin'] if usuario_data else None
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    
# Ruta para cerrar sesión (requiere autenticación)
@app.route('/api/logout', methods=['GET'])
@jwt_required()
def cerrar_sesion():
    try:
        # Cerrar sesión utilizando el servicio de autenticación de Supabase
        supabase.auth.sign_out()
        return jsonify({"mensaje": "Usuario desconectado"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
# Ruta para obtener la lista de prediction_data
@app.route('/api/datos', methods=['GET'])
@jwt_required()
def obtener_datos():
    try:
        response = supabase.table("prediction_data").select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)})
    
# Ruta para registrar datos en el archivo CSV y en la tabla prediction_data
@app.route('/api/datos', methods=['POST'])
@jwt_required()
def registrar_datos():
    try:
        data = request.get_json()

        # Obtener los datos del formulario o solicitud
        user_id = data.get('user_id')
        first_open = data.get('first_open')
        dayofweek = data.get('dayofweek')
        hour = data.get('hour')
        age = data.get('age')
        screen_list = data.get('screen_list')
        numscreens = data.get('numscreens')
        minigame = data.get('minigame')
        used_premium_feature = data.get('used_premium_feature')
        enrolled = data.get('enrolled')
        enrolled_date = data.get('enrolled_date')
        liked = data.get('liked')

        # Cargar los datos existentes del archivo CSV
        csv_path = 'Financial_Application_Behavior_Dataset.csv'
        df = pd.read_csv(csv_path)

        # Crear un nuevo registro como DataFrame
        nuevo_registro = pd.DataFrame({
            'user_id': [user_id],
            'first_open': [first_open],
            'dayofweek': [dayofweek],
            'hour': [hour],
            'age': [age],
            'screen_list': [screen_list],
            'numscreens': [numscreens],
            'minigame': [minigame],
            'used_premium_feature': [used_premium_feature],
            'enrolled': [enrolled],
            'enrolled_date': [enrolled_date],
            'liked': [liked]
        })

        # Concatenar el nuevo registro al DataFrame existente
        df = pd.concat([df, nuevo_registro], ignore_index=True)

        # Guardar el DataFrame actualizado en el archivo CSV
        df.to_csv(csv_path, index=False)

        # Insertar en la tabla prediction_data
        supabase.table("prediction_data").upsert(nuevo_registro.to_dict(orient='records')).execute()

        return jsonify({"mensaje": "Datos registrados con éxito"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Iniciar la aplicación si este script es ejecutado directamente
if __name__ == "__main__":
    app.run(debug=True)