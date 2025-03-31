from flask import Flask, request, jsonify, render_template
import os
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Renderuj plik index.html
    return render_template('index.html')

@app.route('/analyse_frame', methods=['POST'])
def analyse_frame():
    # Odbierz przesłane pliki i dane
    video_file = request.files.get('video')
    frame_number = int(request.form['frame_number'])  # Numer klatki

    if video_file:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
        video_file.save(video_path)

        # Otwórz wideo i przejdź do wybranej klatki
        video = cv2.VideoCapture(video_path)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video.read()

        if not ret:
            return jsonify({'error': 'Nie udało się odczytać klatki'})

        # Przykład analizy: konwersja na grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Tutaj możesz dalej analizować klatkę (np. detekcja twarzy)
        # Zwrócenie wyniku
        return jsonify({'message': 'Analiza klatki zakończona pomyślnie', 'frame': frame_number})
    return jsonify({'error': 'Nie przesłano pliku wideo'})

if __name__ == '__main__':
    app.run(debug=True)
