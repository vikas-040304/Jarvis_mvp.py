# Jarvis_mvp.py
JARVIS is a Python-based voice assistant that listens to your commands, speaks responses, and performs tasks like telling the time, searching the web, opening apps, playing music, checking battery status, and more. It uses SpeechRecognition, pyttsx3, and psutil, with optional offline mode via Vosk.


# JARVIS MVP (Python Voice Assistant)

A minimal, modular Python voice assistant inspired by JARVIS from Iron Man.  
This MVP (Minimum Viable Product) can recognize voice commands, respond with speech, and execute tasks like opening apps, searching the web, playing media, and checking battery status.

---

## 🚀 Features
- **Speech Recognition** (Google API or offline with Vosk)
- **Text-to-Speech** with `pyttsx3`
- **System Commands** (Open Notepad, Calculator, Explorer, Lock/Shutdown system, etc.)
- **Web Search & YouTube Search**
- **Play/Pause Music or Videos**
- **Check Battery Status**
- **Open Social Media (Telegram, WhatsApp, Instagram)**
- **Simple Intent Parsing (Rule-based)**

---

## 📦 Requirements

Python 3.8 or higher recommended.

Install dependencies:
```bash
pip install pyttsx3 SpeechRecognition psutil
Optional:

For offline recognition:

bash
Copy
Edit
pip install vosk
Download a Vosk model and set the VOSK_MODEL_PATH environment variable.

🛠 How to Run
Clone the repository:

bash
Copy
Edit
git clone https://github.com/<your-username>/jarvis-mvp.git
cd jarvis-mvp
Run the script:

bash
Copy
Edit
python jarvis_mvp.py
Speak a command when prompted:

Copy
Edit
🎙️  Listening...
Example commands:

"What's the time?"

"Open YouTube lofi music"

"Search Python tutorials"

"Play music"

"Battery status"

"Open Telegram"

"Shutdown system"

📂 Project Structure
bash
Copy
Edit
jarvis_mvp.py   # Main script
README.md       # Project documentation
⚙ Customization
You can add more skills by:

Creating a new skill_* function.

Adding it to the SKILLS dictionary.

Updating the parse_intent() function to detect your new commands.

⚠ Notes
Windows: Some system commands rely on nircmd.exe for media key simulation.
Download from: https://www.nirsoft.net/utils/nircmd.html and add to PATH.

Linux: System command names are different (e.g., gedit or xed for text editor).

Unlocking the screen is not supported for security reasons.

🖤 Credits
Built by [Your Name] as a learning project.

📜 License
This project is licensed under the MIT License.

yaml

---

If you want, I can also make a **`requirements.txt`** so GitHub users can install everything in one command. That will make your project look cleaner and easier to run.


---

If you want, I can also make a **`requirements.txt`** so GitHub users can install everyt
