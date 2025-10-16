from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/guardar', methods=['POST'])
def guardar():
    datos = request.get_json()
    if not datos:
        return jsonify({'error': 'Datos no recibidos'}), 400
    try:
        # Read existing data if file exists
        if os.path.exists('datos_personales.json'):
            with open('datos_personales.json', 'r', encoding='utf-8') as f:
                try:
                    datos_existentes = json.load(f)
                    # Ensure it's a list
                    if not isinstance(datos_existentes, list):
                        datos_existentes = [datos_existentes]
                except json.JSONDecodeError:
                    datos_existentes = []
        else:
            datos_existentes = []
        
        # Append new data
        datos_existentes.append(datos)
        
        # Save updated data
        with open('datos_personales.json', 'w', encoding='utf-8') as f:
            json.dump(datos_existentes, f, ensure_ascii=False, indent=2)
        return jsonify({'mensaje': 'Datos guardados correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
