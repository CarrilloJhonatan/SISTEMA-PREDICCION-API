import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score

# Cargar los datos
data = pd.read_csv("Financial_Application_Behavior_Dataset.csv")

# Preprocesamiento de datos
data['first_open'] = pd.to_datetime(data['first_open'])
data['enrolled_date'] = pd.to_datetime(data['enrolled_date'])
data['hour'] = pd.to_datetime(data['hour'].str.strip(), format='%H:%M:%S', errors='coerce').dt.hour
data.dropna(inplace=True)

# One-hot encoding para la columna 'screen_list'
screen_list_dummies = data['screen_list'].str.get_dummies(',')

# Concatenar los datos procesados
data = pd.concat([data, screen_list_dummies], axis=1)

# Eliminar columnas no necesarias
columns_to_drop = ['user_id', 'first_open', 'screen_list', 'enrolled_date', 'liked']
data.drop(columns_to_drop, axis=1, inplace=True)

# Dividir los datos en conjuntos de entrenamiento y prueba
X = data.drop('enrolled', axis=1)
y = data['enrolled']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inicializar el modelo de árbol de decisión
model = DecisionTreeClassifier(random_state=42)

# Entrenar el modelo
model.fit(X_train, y_train)

# Realizar predicciones en el conjunto de prueba
y_pred = model.predict(X_test)

# Imprimir reporte de clasificación junto con las predicciones
classification_rep = classification_report(y_test, y_pred)
print("Reporte de Clasificación:")
print(classification_rep)

# Calcular la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {accuracy}")