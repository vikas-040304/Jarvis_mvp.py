# jarvis_mvp.py
import os, json, queue, time, subprocess, webbrowser
import pyttsx3, speech_recognition as sr # type: ignore
import psutil # type: ignore

# ------------ TTS ------------
tts = pyttsx3.init()
tts.setProperty("rate", 180)

def speak(text: str):
    print(f"JARVIS:", text)
    tts.say(text); tts.runAndWait()

# ------------ STT ------------
# If Vosk model is installed, SpeechRecognition can use it via recognizer.recognize_vosk
# Install a small model and set VOSK_MODEL_PATH env var if needed.
r = sr.Recognizer()
r.energy_threshold = 300

def listen_once(timeout=6, phrase_time_limit=8):
    with sr.Microphone() as source:
        print("🎙️  Listening...")
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    try:
        # Try offline Vosk first
        if "VOSK_MODEL_PATH" in os.environ:
            txt = r.recognize_vosk(audio)
            # Vosk returns JSON string with "text"
            data = json.loads(txt) if txt.startswith("{") else {"text": txt}
            return data.get("text", "").strip()
        # fallback: Google (requires internet)
        return r.recognize_google(audio).strip()
    except Exception as e:
        return ""

# ------------ Skills (Plugins) ------------
def skill_time(_):
    return time.strftime("It's %I:%M %p")

def skill_open_youtube(query):
    webbrowser.open("https://www.youtube.com/results?search_query=" + query.replace(" ", "+"))
    return f"Opening YouTube for {query}"

def skill_search_web(query):
    webbrowser.open("https://www.google.com/search?q=" + query.replace(" ", "+"))
    return f"Searching the web for {query}"

def skill_system(command):
    try:
        if os.name == "nt":
            if command == "open notepad": subprocess.Popen(["notepad"])
            elif command == "lock screen": subprocess.Popen(["rundll32.exe","user32.dll,LockWorkStation"])
            elif command == "unlock screen": return "Unlocking screen is not supported for security reasons."
            elif command == "shutdown system": subprocess.Popen(["shutdown", "/s", "/t", "0"])
            elif command == "open calculator": subprocess.Popen(["calc"])
            elif command == "open command prompt": subprocess.Popen(["cmd"])
            elif command == "open explorer": subprocess.Popen(["explorer"])
            else: return "I don't have that system command yet."
        else:
            if command == "open text editor": subprocess.Popen(["xed" if shutil.which("xed") else "gedit"])
            elif command == "lock screen": subprocess.Popen(["loginctl","lock-session"])
            elif command == "unlock screen": return "Unlocking screen is not supported for security reasons."
            elif command == "shutdown system": subprocess.Popen(["shutdown", "now"])
            else: return "I don't have that system command yet."
        return "Done."
    except Exception as e:
        return "I couldn't execute that."

def skill_media(command):
    if command == "play music":
        webbrowser.open("https://www.youtube.com/results?search_query=lofi+music")
        return "Playing music on YouTube."
    elif command == "play video":
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube for videos."
    elif command == "pause music":
        subprocess.Popen(["nircmd.exe", "sendkeypress", "space"])
        return "Paused music (if supported)."
    elif command == "resume music":
        subprocess.Popen(["nircmd.exe", "sendkeypress", "space"])
        return "Resumed music (if supported)."
    else:
        return "I can't do that yet."

def skill_battery(_):
    battery = psutil.sensors_battery()
    if battery and battery.percent < 20 and not battery.power_plugged:
        return "Battery is low. Please plug in the charger."
    elif battery and battery.power_plugged:
        return "Laptop is charging."
    else:
        return "Battery status not available."

def skill_social(command):
    if command == "open telegram":
        webbrowser.open("https://web.telegram.org/")
        return "Opening Telegram."
    elif command == "open whatsapp":
        webbrowser.open("https://web.whatsapp.com/")
        return "Opening WhatsApp."
    elif command == "open instagram":
        webbrowser.open("https://www.instagram.com/")
        return "Opening Instagram."
    elif command == "close telegram":
        return "Please close the browser tab manually."
    elif command == "close whatsapp":
        return "Please close the browser tab manually."
    elif command == "close instagram":
        return "Please close the browser tab manually."
    else:
        return "I can't do that yet."

SKILLS = {
    "time": skill_time,
    "youtube": skill_open_youtube,
    "search": skill_search_web,
    "system": skill_system,
    "media": skill_media,
    "battery": skill_battery,
    "social": skill_social,
}

# ------------ NLU (Simple Intent Rules) ------------
def parse_intent(text: str):
    t = text.lower()
    if not t: return ("smalltalk", "I didn't catch that.")
    if any(k in t for k in ["time", "what time", "current time"]):
        return ("time", None)
    if t.startswith("play music") or t.startswith("play video") or t.startswith("pause music") or t.startswith("resume music"):
        return ("media", t)
    if "battery" in t or "charge" in t:
        return ("battery", None)
    if any(k in t for k in [
        "open telegram", "open whatsapp", "open instagram",
        "close telegram", "close whatsapp", "close instagram"
    ]):
        return ("social", t)
    if t.startswith("open youtube") or t.startswith("play on youtube"):
        q = t.replace("open youtube", "").replace("play on youtube", "").strip()
        return ("youtube", q if q else "lofi music")
    if t.startswith("search") or t.startswith("google"):
        q = t.replace("search", "").replace("google", "").strip()
        return ("search", q if q else "latest tech news")
    if any(k in t for k in [
        "open notepad", "lock screen", "open text editor",
        "unlock screen", "shutdown system", "open calculator",
        "open command prompt", "open explorer"
    ]):
        return ("system", t)
    if any(k in t for k in ["who are you", "jarvis"]):
        return ("smalltalk", "I am JARVIS, your AI assistant.")
    return ("search", t)  # fallback: web search

# ------------ Main Loop ------------
def main():
    speak("Online and ready.")
    while True:
        text = listen_once()
        if not text:
            continue
        print("You:", text)
        if text.lower() in ["exit", "quit", "shutdown jarvis", "sleep"]:
            speak("Powering down. Goodbye.")
            break
        intent, payload = parse_intent(text)
        if intent in SKILLS:
            result = SKILLS[intent](payload)
        else:
            result = payload if isinstance(payload, str) else "Okay."
        speak(result)

if __name__ == "__main__":
    main()
