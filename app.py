import sqlite3
from flask import Flask, jsonify, request
import pickle
import pandas as pd
from clases import columnDropTransform, columBinarizeTransform
from datetime import datetime

def connectBd():
    conn = sqlite3.connect('boston.db')
    c = conn.cursor()
    return conn, c


app = Flask(__name__)


# RUTA 1: Get/predict (obtener predicción) -> /api/boston/predict

@app.route('/api/boston/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if data is None:
        return jsonify({"message": "No se ha enviado ningún dato"}), 400
    elif not isinstance(data, list) or not all(isinstance(d, dict) for d in data):
        return jsonify({"message": "Los datos deben ser una lista de diccionarios"}), 400
    elif not data:
        return jsonify({"message": "La lista de datos está vacía"}), 400
    else:
        # Insertar diccionario a un dataframe
        data = pd.DataFrame(data)               # Dataframe con los datos de entrada: Cada 
        print(data)
        # Cargar el modelo pickle (modelo entrenado)
        with open('modelo_boston.pkl', 'rb') as f:
            model = pickle.load(f)

        # Predecir con el modelo
        prediction = model.predict(data) 
        # Convertir el ndarray en una lista
        prediction = prediction.tolist()      

        conexion, cursor = connectBd()

        # Insert into the table
        fecha_actual = datetime.now()
        sql = """INSERT INTO boston 
                                (CRIM, INDUS, NOX, RM, AGE, DIS, TAX, PTRATIO, LSTAT, date, target)  
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        # Insertar los datos en la tabla boston 
        for i in range(len(data)):
            cursor.execute(sql, (data.iloc[i]['CRIM'], data.iloc[i]['INDUS'], data.iloc[i]['NOX'], data.iloc[i]['RM'], 
                            data.iloc[i]['AGE'], data.iloc[i]['DIS'], data.iloc[i]['TAX'], data.iloc[i]['PTRATIO'], 
                            data.iloc[i]['LSTAT'], fecha_actual, prediction[i]))

        conexion.commit()
        conexion.close()

        return jsonify({"message": "Predicción realizada correctamente", "predicción": prediction} ), 200
    


if __name__ == "__main__":
    app.run(debug=True)
