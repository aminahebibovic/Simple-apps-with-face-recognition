import cv2
import os
import numpy as np

# Kreiraj folder za slike ako ne postoji
if not os.path.exists("faces"):
    os.makedirs("faces")

# Pokreni kameru
cap = cv2.VideoCapture(0)

# Inicijalizuj Haar Cascade Classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inicijalizuj LBPH recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# ID korisnika (samo tvoje lice)
USER_ID = 1

# Prebroji već postojeće slike i nastavi numeraciju
existing_images = [img for img in os.listdir("faces") if img.startswith(f"user_{USER_ID}_")]
img_count = len(existing_images)

print(f"There are already {img_count} of images. Adding more...")

# Ciljani broj slika
TARGET_IMAGES = 500

while img_count < TARGET_IMAGES:
    ret, frame = cap.read()
    if not ret:
        break

    # Pretvori sliku u grayscale (bolja detekcija lica)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detektuj lice
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Iscrtavanje pravougaonika oko prepoznatog lica
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Sačuvaj sliku lica
        img_count += 1
        face_image = gray[y:y + h, x:x + w]
        cv2.imwrite(f"faces/user_{USER_ID}_{img_count}.jpg", face_image)

    # Prikazivanje slike u realnom vremenu
    cv2.imshow("Face Capture", frame)

    # Ako je sakupio dovoljno slika, prekini
    if img_count >= TARGET_IMAGES:
        break

    # Pritisni 'q' za izlaz iz kamere
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Očisti kameru
cap.release()
cv2.destroyAllWindows()

print(f"Totally saved images: {img_count}")

# Treniraj model sa svim prikupljenim slikama
faces = []
labels = []

for img_name in os.listdir("faces"):
    if img_name.startswith(f"user_{USER_ID}_"):  # Samo tvoje slike
        img_path = os.path.join("faces", img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        faces.append(img)
        labels.append(USER_ID)  # Oznaka za tvoje lice

# Proveri da li ima dovoljno slika za treniranje
if len(faces) > 0:
    recognizer.train(faces, np.array(labels))
    recognizer.save("trainer.yml")
    print("Model saved successfuly.")
else:
    print("Error: There isn't enough images!")