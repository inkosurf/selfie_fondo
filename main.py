@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            archivo = request.files['imagen']
            input_image = Image.open(archivo.stream).convert("RGBA")
            output_image_data = remove(input_image)
            imagen_sin_fondo = Image.open(io.BytesIO(output_image_data)).convert("RGBA")

            output_path = "/tmp/final.png"
            imagen_sin_fondo.save(output_path)

            return send_file(output_path, as_attachment=True)
        except Exception as e:
            print(f"💥 Error: {e}", file=sys.stderr)
            return f"Error interno: {e}", 500

    return render_template("index.html")
