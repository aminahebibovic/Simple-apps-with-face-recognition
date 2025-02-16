import tkinter as tk
import random
import string
import cv2
from tkinter import filedialog

# Password Generator
def generate_password(length):
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password

def on_generate_click():
    try:
        length = int(entry_length.get())
        if length < 1:
            raise ValueError("Length must be a positive number.")
        password = generate_password(length)
        label_result.config(text=f"Generated password: {password}")
    except ValueError as e:
        label_result.config(text=f"Error: {e}")

# Text Counter
def count_text():
    text = text_entry.get("1.0", "end-1c")
    words = text.split()
    paragraphs = text.split("\n")
    
    num_words = len(words)
    num_characters = len("".join(words))
    num_paragraphs = len(paragraphs)
    
    result_label.config(text=f"Number of characters: {num_characters}\nNumber of words: {num_words}\nNumber of paragraphs: {num_paragraphs}")

# File Search
def search_file():
    keyword = search_entry.get()
    if not keyword:
        result_search.config(text="Please enter a keyword to search.")
        return
    
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        with open(filepath, "r") as file:
            content = file.read()
            occurrences = content.lower().count(keyword.lower())
            result_search.config(text=f"Keyword '{keyword}' found {occurrences} times.")
    else:
        result_search.config(text="No file selected.")

# Face Recognition
def detect_face():
    # Učitaj trenirani model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    # Haar Cascade za detekciju lica
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Pokreni kameru
    cap = cv2.VideoCapture(0)

    recognized = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = gray[y:y + h, x:x + w]

            # Pokušaj prepoznavanja lica
            label, confidence = recognizer.predict(face_roi)

            if confidence < 50:  # Prag sigurnosti, manja vrednost znači bolje prepoznavanje
                text = "Person recognized"
                recognized = True
            else:
                text = "Didn't recognnize person"

            # Prikaz poruke na ekranu
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if recognized:
            break

    cap.release()
    cv2.destroyAllWindows()

    if recognized:
        go_to_app_screen()  # Ako je lice prepoznato, otvori aplikaciju
    else:
        print("Pristup odbijen - lice nije prepoznato!")

# Navigacija između ekrana
def go_to_app_screen():
    first_screen.pack_forget()
    app_screen.pack(fill='both', expand=True)

def go_back_to_main():
    app_screen.pack_forget()
    first_screen.pack(fill='both', expand=True)

def go_to_password_generator():
    app_screen.pack_forget()
    password_generator_screen.pack(fill='both', expand=True)

def go_back_from_password_generator():
    password_generator_screen.pack_forget()
    app_screen.pack(fill='both', expand=True)

def go_to_text_counter():
    app_screen.pack_forget()
    text_counter_screen.pack(fill='both', expand=True)

def go_back_from_text_counter():
    text_counter_screen.pack_forget()
    app_screen.pack(fill='both', expand=True)

def go_to_file_search():
    app_screen.pack_forget()
    file_search_screen.pack(fill='both', expand=True)

def go_back_from_file_search():
    file_search_screen.pack_forget()
    app_screen.pack(fill='both', expand=True)

# Main window
root = tk.Tk()
root.title("Password Generator, Text Counter, and File Search")
root.geometry("800x600")

# Fonts
font_large = ("Helvetica", 16, "bold")
font_medium = ("Helvetica", 14)
font_small = ("Helvetica", 12)

# First screen (Face Recognition)
first_screen = tk.Frame(root)
first_screen.pack(fill='both', expand=True)

button_start_face_recognition = tk.Button(first_screen, text="Start Face Recognition", command=detect_face, font=font_large, bg="#4CAF50", fg="white", relief="flat", padx=20, pady=10)
button_start_face_recognition.pack(pady=50)

# Second screen (App selection)
app_screen = tk.Frame(root)

button_password_generator = tk.Button(app_screen, text="Open Password Generator", command=go_to_password_generator, font=font_large, bg="#4CAF50", fg="white", relief="flat", padx=20, pady=10)
button_password_generator.pack(pady=20)

button_text_counter = tk.Button(app_screen, text="Open Text Counter", command=go_to_text_counter, font=font_large, bg="#FF9800", fg="white", relief="flat", padx=20, pady=10)
button_text_counter.pack(pady=20)

button_file_search = tk.Button(app_screen, text="Open File Search", command=go_to_file_search, font=font_large, bg="#2196F3", fg="white", relief="flat", padx=20, pady=10)
button_file_search.pack(pady=20)

# Password Generator Screen
password_generator_screen = tk.Frame(root)
label_instruction = tk.Label(password_generator_screen, text="Enter password length:", font=font_medium)
label_instruction.pack(pady=10)

entry_length = tk.Entry(password_generator_screen, font=font_medium, relief="solid", bd=2, width=20)
entry_length.pack(pady=5)

button_generate = tk.Button(password_generator_screen, text="Generate Password", command=on_generate_click, font=font_medium, bg="#2196F3", fg="white", relief="flat", padx=20, pady=10)
button_generate.pack(pady=10)

label_result = tk.Label(password_generator_screen, text="Generated password will appear here.", font=font_medium)
label_result.pack(pady=20)

button_back = tk.Button(password_generator_screen, text="Back", command=go_back_from_password_generator, font=font_medium, bg="#FF5722", fg="white", relief="flat", padx=20, pady=10)
button_back.pack(pady=20)

# Text Counter Screen
text_counter_screen = tk.Frame(root)
label_text_instruction = tk.Label(text_counter_screen, text="Enter text:", font=font_medium)
label_text_instruction.pack(pady=10)

text_entry = tk.Text(text_counter_screen, font=font_medium, height=10, width=40)
text_entry.pack(pady=10)

button_count = tk.Button(text_counter_screen, text="Count Characters, Words, and Paragraphs", command=count_text, font=font_medium, bg="#4CAF50", fg="white", relief="flat", padx=20, pady=10)
button_count.pack(pady=10)

result_label = tk.Label(text_counter_screen, text="Results will appear here.", font=font_medium)
result_label.pack(pady=20)

button_back_to_main = tk.Button(text_counter_screen, text="Back", command=go_back_from_text_counter, font=font_medium, bg="#FF5722", fg="white", relief="flat", padx=20, pady=10)
button_back_to_main.pack(pady=20)

# File Search Screen
file_search_screen = tk.Frame(root)
label_search_instruction = tk.Label(file_search_screen, text="Enter keyword to search in a file:", font=font_medium)
label_search_instruction.pack(pady=10)

search_entry = tk.Entry(file_search_screen, font=font_medium, relief="solid", bd=2, width=20)
search_entry.pack(pady=10)

button_search = tk.Button(file_search_screen, text="Search File", command=search_file, font=font_medium, bg="#2196F3", fg="white", relief="flat", padx=20, pady=10)
button_search.pack(pady=10)

result_search = tk.Label(file_search_screen, text="Search result will appear here.", font=font_medium)
result_search.pack(pady=20)

button_back_to_main_from_search = tk.Button(file_search_screen, text="Back", command=go_back_from_file_search, font=font_medium, bg="#FF5722", fg="white", relief="flat", padx=20, pady=10)
button_back_to_main_from_search.pack(pady=20)

# Close the window with the top right button
root.protocol("WM_DELETE_WINDOW", root.quit)

# Run the application
root.mainloop()
