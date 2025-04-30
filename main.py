
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia
import os
import requests

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said: ", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
        return ""
    except sr.RequestError:
        print("Could not request results, please check your internet connection.")
        return ""

def open_website(site):
    webbrowser.open(site)
    speak(f"Opening {site}")

def get_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {now}")

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("Sorry, no information found.")

def get_weather(city):
    api_key = "your_openweather_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        speak(f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius.")
    else:
        speak("City not found.")

def main():
    speak("Hello, I am Jarvis. How can I assist you?")
    while True:
        command = listen()
       
        
        if "time" in command:
            get_time()
        elif "open google" in command:
            open_website("https://www.google.com")
        elif "open youtube" in command:
            open_website("https://www.youtube.com")
        elif "wikipedia" in command:
            search_query = command.replace("wikipedia", "").strip()
            search_wikipedia(search_query)
        elif "weather" in command:
            speak("Please say the city name.")
            city = listen()
            get_weather(city)
        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break
        else:
            speak("I didn't understand that. Please try again.")

if __name__ == "__main__":
    main()