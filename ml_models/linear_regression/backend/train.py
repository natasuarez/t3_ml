import joblib
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

#Predecir precios de viviendas segun la superficie en m2

#Datos de entrenamiento
x = np.array([[70], [80], [90], [100], [110], [120], [130], [140], [150]])
y = np.array([42000000, 80000000, 90000000, 150000000, 180000000, 200000000, 22000000, 25000000, 30000000])

#Entrenar el modelo de regresion lineal
model = LinearRegression()
model.fit(x,y)

#predicciones de prueba
# y_pred = model.predict(x)

# #Imprimir los coeficientes del modelo 
# print("Coeficiente de regresion:", model.coef_[0])
# print("Término independiente:", model.intercept_)

# #Graficar datos reales 
# plt.scatter(x, y, color='red', label='Datos reales')

# #graficar la linea de regresion
# plt.plot(x, y_pred, color='blue', label='Linea de regresion')

# #Agregar etiquetas y titulo
# plt.xlabel('Superficie (m2)')
# plt.ylabel('Precio (COP)')
# plt.title('Regresion Lineal - Precio de Viviendas')
# plt.legend()
# plt.grid(True)

# #Graficar la grafica
# plt.show()


#Guardar (Serializarlo) el modelo entrenando en un archivo 
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "linear_model.joblib"

joblib.dump(model, MODEL_PATH)