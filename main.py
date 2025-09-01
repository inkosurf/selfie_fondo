from flask import Flask, render_template, request, send_file
from PIL import Image
from rembg import remove
import io
import os
import sys

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("➡️ POST recibido", file=sys.stderr)

        if 'imagen' not in request.files:
            print("❌ No se recibió archivo", file=sys.stderr)
            return "No se envió ninguna imagen", 400

        archivo = request.files['imagen']
        print(f"📂 Nombre archivo: {archivo.filename}", file=sys.stderr)

        try:
            input_image = Image.open(archivo.stream).convert("RGBA")
            print("✅ Imagen cargada con PIL", file=sys.stderr)

            output_image_data = remove(input_image)
            print("✅ Fondo removido", file=sys.stderr)

            imagen_sin_fondo = Image.open(io.BytesIO(output_image_data)).convert("RGBA")
            print("✅ Imagen sin fondo lista", file=sys.stderr)

            fondo = Image.open(os.path.join(app.root_path, "static", "fondo.jpg")).convert("RGBA")
            print("✅ Fondo cargado", file=sys.stderr)

            fondo = fondo.resize(imagen_sin_fondo.size)
            imagen_final = Image.alpha_composite(fondo, imagen_sin_fondo)

            # Guardar en carpeta temporal
            output_path = "/tmp/final.png"
            imagen_final.save(output_path)
            print(f"✅ Imagen final guardada en {output_path}", file=sys.stderr)

            # Enviar descarga directa al usuario
            return send_file(output_path, as_attachment=True)

        except Exception as e:
            print(f"💥 Error procesando imagen: {e}", file=sys.stderr)
            return f"Error interno: {e}", 500

    # GET normal: carga la página
    return render_template("index.html")
