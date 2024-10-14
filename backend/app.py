from flask import Flask, request, jsonify, send_from_directory
from image_processor import compress_and_convert_to_webp
import os
import shutil
import time

static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
app = Flask(__name__, static_folder=static_folder_path, static_url_path='')


@app.route('/')
def serve_gui():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/compress', methods=['POST'])
def compress_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    max_size = int(request.form.get('max_size', 2000))
    quality = int(request.form.get('quality', 80))

    try:
        # Assicurati che la cartella temporanea esista
        if not os.path.exists("temp"):
            os.makedirs("temp")

        # Salva l'immagine in un percorso temporaneo
        temp_input_path = os.path.join("temp", image_file.filename)
        image_file.save(temp_input_path)

        # Definisci il percorso di output
        temp_output_path = os.path.join("temp", os.path.splitext(image_file.filename)[0] + ".webp")

        # Comprimi e converte in WebP
        compress_and_convert_to_webp(temp_input_path, temp_output_path, max_size, quality)

        # Restituisci l'immagine compressa come file scaricabile
        return send_from_directory(os.path.abspath("temp"), os.path.basename(temp_output_path), as_attachment=True)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


# Temporaneamente disabilita la pulizia automatica
# @app.route('/cleanup', methods=['POST'])
# def cleanup_temp():
#     try:
#         temp_dir = os.path.abspath("temp")
#         if os.path.exists(temp_dir):
#             print(f"Cleaning up temp directory: {temp_dir}")
#             shutil.rmtree(temp_dir)
#         os.makedirs(temp_dir)  # Ricrea la cartella temp per future operazioni
#         return jsonify({'message': 'Cleanup successful'}), 200
#     except Exception as e:
#         print(f"Error during cleanup: {e}")
#         return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists("temp"):
        os.makedirs("temp")
    app.run(debug=False, use_reloader=False, port=5000)