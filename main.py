import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# IMPORTANT CONSTANTS
TEST_FILE = "images/3722009-hd_1920_1080_24fps.mp4"

class VideoSource:

    @staticmethod
    def menu():
        source = input("Wybierz źródło obrazu:\n"
                       "\t[1]: Wideo\n"
                       "\t[2]: Kamera\n"
                       "\t[3]: Kamera IP\n"
                       "[Enter]: Wideo z pliku testowego\n")

        source_methods = {
            "1": lambda: VideoSource.files(),
            "2": VideoSource.camera(),
            "3": lambda: VideoSource.camera_ip(),
            "": lambda: VideoSource.files(TEST_FILE)
        }

        try:
            return source_methods[source]()
        except ValueError as e:
            print(str(e))
            return


    @staticmethod
    def files(video_path = None):
        if not video_path:
            video_path = input("Podaj ścieżkę do pliku wideo: ")
        if not video_path:
            raise ValueError("Nie podano ścieżki wideo.")
        return cv2.VideoCapture(video_path)


    @staticmethod
    def camera():
        return cv2.VideoCapture(0)


    @staticmethod
    def camera_ip(ip_url = None):
        if ip_url is None:
            ip_url = input("Podaj URL kamery IP: ")
        return cv2.VideoCapture(ip_url)


def main():
    # Wybór źródła obrazu
    cap = VideoSource.menu()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Nie można pobrać obrazu.")
            break

        # Rysowanie elementów na obrazie
        height, width, _ = frame.shape
        cv2.line(frame, (0, 0), (width, height), (0, 255, 0), 2)  # Przykład linii
        cv2.putText(frame, "Wykryty obiekt", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)  # Przykład tekstu

        # Wyświetlanie obrazu
        cv2.imshow("Podgląd kamery", frame)

        # Zakończ program po wciśnięciu klawisza 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
