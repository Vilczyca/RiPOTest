from flask import Flask, request, render_template, make_response, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "some_secret_key"  # Klucz do obsługi sesji

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/clear_cookies", methods=["POST"])
def clear_cookies():
    session.clear()
    response = make_response("Ciasteczka wyczyszczone")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return redirect(url_for("index"))





# Obsługa głównego widoku
@app.route("/", methods=["GET", "POST"])
def index():
    # Sprawdź, czy dane kroków A i B są w sesji
    step_a_completed = "image_base" in session
    step_b_completed = "video" in session or "webcam_url" in session
    print("index()")
    print("image_base", "image_base" in session)
    print("video", "video" in session)
    print("webcam_url", "webcam_url" in session)

    return render_template("index.html", step_a_completed=step_a_completed, step_b_completed=step_b_completed)

# Obsługa przesyłania danych dla Kroku A
@app.route("/upload_step_a", methods=["POST"])
def upload_step_a():
    print("A")
    image_base = request.files.getlist("image_base")
    if not image_base:
        return "Musisz przesłać bazę zdjęć", 400

    # Zapisz pliki do folderu uploads i zapisz stan w sesji
    session["image_base"] = []
    for file in image_base:
        print(file.filename)
        session["image_base"].append(file.filename)

    return redirect(url_for("index"))

# Obsługa przesyłania danych dla Kroku B
@app.route("/upload_step_b", methods=["POST"])
def upload_step_b():
    print("B")
    video = request.files.get("video")
    webcam_url = request.form.get("webcam_url")

    # Obsługa pliku wideo
    if video:
        video_path = os.path.join(UPLOAD_FOLDER, video.filename)
        video.save(video_path)
        session["video"] = video_path
        print("Przesłano plik:", video_path)

    # Obsługa URL kamery
    elif webcam_url:
        session["webcam_url"] = webcam_url
        print("Przesłano link:", webcam_url)

    else:
        return "Musisz przesłać źródło obrazu: plik wideo lub URL kamery", 400

    return redirect(url_for("index"))

# Obsługa finalizacji i przejścia do player.html
@app.route("/process", methods=["POST"])
def process():
    print("process()")
    print("image_base", "image_base" in session)
    print("video", "video" in session)
    print("webcam_url", "webcam_url" in session)

    if "image_base" not in session or ("video" not in session and "webcam_url" not in session):
        return "Musisz przesłać zarówno bazę zdjęć, jak i źródło obrazu", 400

    image_base = session["image_base"]
    video_path = session.get("video")
    webcam_url = session.get("webcam_url")

    # Przekaż dane do player.html
    if video_path:
        session.clear()  # Wyczyszczenie danych sesji
        return render_template("player.html", source_type="video", video_path=video_path, message="Załadowano bazę zdjęć")
    elif webcam_url:
        session.clear()  # Wyczyszczenie danych sesji
        return render_template("player.html", source_type="webcam", webcam_url=webcam_url, message="Załadowano bazę zdjęć")
    session.clear()  # Wyczyszczenie danych sesji
    return "Coś poszło nie tak", 400


if __name__ == "__main__":
    app.run(debug=True)
