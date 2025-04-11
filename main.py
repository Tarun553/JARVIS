import speech_recognition as sr
import pyttsx3
import webbrowser
import music
from google import genai
from langdetect import detect


# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech and speak it out loud."""
    engine.say(text)
    engine.runAndWait()
    
def airesponse(command):
    """Your name is jarvis and you Generate a short response in English or Hindi based on user's input language."""
   
    
    # Detect the language of the user's input
    try:
        lang = detect(command)
    except:
        lang = "en"  # fallback to English

    client = genai.Client(api_key="AIzaSyBsPRW_EZTavfFM47iVsGEjJeUUZIgKNZk")

    if lang == "hi":
        prompt = f"""
Tum ek smart AI assistant ho. User ne Hindi mein poocha: "{command}"

Bas 2-3 line ka simple aur casual jawaab do Roman Hindi mein.

Answer:"""
    else:
        prompt = f"""
You are a smart AI assistant. The user asked: "{command}"

Give a short, simple, casual response in English (2-3 lines only).

Answer:"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )

    return response.text.strip()




def processcommand(command):
    if "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    elif "open stack overflow" in command:
        webbrowser.open("https://stackoverflow.com")
        speak("Opening Stack Overflow.")
    elif "open github" in command:
        webbrowser.open("https://github.com")
        speak("Opening GitHub.")
    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com")
        speak("Opening Facebook.")
    elif command.lower().startswith("play "):
        song = command.lower().split(" ")[1]
        try:
            # Attempt to access the song in the music dictionary
            url = music.music[song]
            webbrowser.open(url)  # Open the YouTube link
            speak(f"Playing {song}.")
        except KeyError:
            speak(f"Error: The song '{song}' does not exist in the music library.")
        except Exception as e:
            speak(f"An unexpected error occurred: {e}")
    else:
        response = airesponse(command)
        speak(response)
        


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    
    # Listen for the wake word "Jarvis"
    with sr.Microphone() as source:
        print("Listening for the wake word 'Jarvis'...")

        try:
            while True:  # Keep listening for the wake word
                audio = recognizer.listen(source)

                # Recognize the wake word
                print("Recognizing...")
                try:
                    command = recognizer.recognize_google(audio).lower()
                    if "jarvis" in command:
                        speak("Jarvis activated. How can I help you?")
                        while True:  # Keep listening for commands after activation
                            audio = recognizer.listen(source)
                            print("Listening for commands...")
                            try:
                                command = recognizer.recognize_google(audio).lower()
                                print(f"You said: {command}")
                                
                                processcommand(command)  # Pass the recognized command
                            except sr.UnknownValueError:
                                print("Sorry, I didn't catch that. Please try again.")
                            except sr.RequestError as e:
                                print(f"Could not request results from Google Speech Recognition service; {e}")
                except sr.UnknownValueError:
                    print("Sorry, I didn't catch that. Please try again.")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")