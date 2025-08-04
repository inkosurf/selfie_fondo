from flask import Flask, render_template, request
from PIL import Image
from rembg import remove
import io
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'imagen' not in request.files:
            return "No se envió ninguna imagen", 400

        archivo = request.files['imagen']
        input_image = Image.open(archivo.stream).convert("RGBA")

        output_image_data = remove(input_image)

        imagen_sin_fondo = Image.open(io.BytesIO(output_image_data)).convert("RGBA")

        fondo = Image.open("static/fondo.jpg").convert("RGBA")
        fondo = fondo.resize(imagen_sin_fondo.size)

        imagen_final = Image.alpha_composite(fondo, imagen_sin_fondo)
        imagen_final.save("static/final.png")

        return render_template("index.html", link_resultado="static/final.png")

    return render_template("index.html")
    if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
