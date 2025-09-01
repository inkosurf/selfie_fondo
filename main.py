from flask import Flask, render_template, request, send_file
from PIL import Image
import io
import os
import sys

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            archivo = request.files['imagen']
            print(f"📂 Recibido: {archivo.filename}", file=sys.stderr)

            # Abrir y procesar imagen
            img = Image.open(archivo.stream)

            # Convertir a escala de grises
            img = img.convert("L")

            # Redimensionar a 500x500
            img = img.resize((500, 500))

            # Guardar resultado en carpeta temporal
            output_path = "/tmp/procesada.png"
            img.save(output_path)

            print(f"✅ Imagen procesada y guardada en {output_path}", file=sys.stderr)

            return send_file(output_path, as_attachment=True)

        except Exception as e:
            print(f"💥 Error: {e}", file=sys.stderr)
            return f"Error interno: {e}", 500

    return render_template("index.html")


