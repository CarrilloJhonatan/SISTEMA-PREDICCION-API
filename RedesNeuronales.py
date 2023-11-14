import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

def entrenar_y_evaluar_modelo_neuronal(dataset_path="Financial_Application_Behavior_Dataset.csv", epochs=10, batch_size=32):
    # Cargar los datos
    data = pd.read_csv(dataset_path)

    # Preprocesamiento de datos
    data['first_open'] = pd.to_datetime(data['first_open'])
    data['enrolled_date'] = pd.to_datetime(data['enrolled_date'])
    data['hour'] = pd.to_datetime(data['hour'].str.strip(), format='%H:%M:%S', errors='coerce').dt.hour
    data.dropna(inplace=True)

    # One-hot encoding para la columna 'screen_list'
    screen_list_dummies = data['screen_list'].str.get_dummies(',')
    data = pd.concat([data, screen_list_dummies], axis=1)

    # Eliminar columnas no necesarias
    columns_to_drop = ['user_id', 'first_open', 'screen_list', 'enrolled_date', 'liked']
    data.drop(columns_to_drop, axis=1, inplace=True)

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X = data.drop('enrolled', axis=1)
    y = data['enrolled']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Escalar los datos
    scaler = StandardScaler()
    X_train_scaled = torch.tensor(scaler.fit_transform(X_train.values), dtype=torch.float32)
    X_test_scaled = torch.tensor(scaler.transform(X_test.values), dtype=torch.float32)
    y_train = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)
    y_test = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)

    # Construir el modelo de red neuronal en PyTorch
    class NeuralNetwork(nn.Module):
        def __init__(self, input_size):
            super(NeuralNetwork, self).__init__()
            self.fc1 = nn.Linear(input_size, 64)
            self.dropout = nn.Dropout(0.5)
            self.fc2 = nn.Linear(64, 32)
            self.fc3 = nn.Linear(32, 1)
            self.sigmoid = nn.Sigmoid()

        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = self.dropout(x)
            x = torch.relu(self.fc2(x))
            x = self.dropout(x)
            x = self.fc3(x)
            x = self.sigmoid(x)
            return x

    # Inicializar el modelo
    input_size = X_train_scaled.shape[1]
    model = NeuralNetwork(input_size)

    # Definir la función de pérdida y el optimizador
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Entrenar el modelo
    for epoch in range(epochs):
        for i in range(0, len(X_train_scaled), batch_size):
            batch_X = X_train_scaled[i:i+batch_size]
            batch_y = y_train[i:i+batch_size]

            # Forward pass
            y_pred = model(batch_X)

            # Calcular la pérdida
            loss = criterion(y_pred, batch_y)

            # Backward pass y optimización
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    # Evaluar el modelo en el conjunto de prueba
    with torch.no_grad():
        model.eval()
        y_pred_proba = model(X_test_scaled)
        y_pred = (y_pred_proba > 0.5).float()

        # Obtener el reporte de clasificación y la precisión
        classification_rep = classification_report(y_test.numpy(), y_pred.numpy())
        accuracy = accuracy_score(y_test.numpy(), y_pred.numpy())

    # Devolver los resultados
    return classification_rep, accuracy

#     # Llamar a la función y obtener los resultados
# reporte_clasificacion, precision_modelo = entrenar_y_evaluar_modelo_neuronal()

# # Hacer lo que necesites con los resultados
# print("Reporte de Clasificación:")
# print(reporte_clasificacion)
# print(f"Precisión del modelo: {precision_modelo}")