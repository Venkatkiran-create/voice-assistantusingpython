import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            query = recognizer.recognize_google(audio)
            query = query.lower()
            print(f"User said: {query}")
            return query
    except Exception as e:
        print("Could not understand your voice.")
        return None

# Basic tasks
def tell_time():
    time_now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {time_now}")

def tell_date():
    date_today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today is {date_today}")

def search_web(query):
    pywhatkit.search(query)
    speak(f"Here are the search results for {query}")

# Advanced tasks
def send_email(recipient_email, subject, body):
    sender_email = "your-email@example.com"  # Replace with your email
    sender_password = "your-password"         # Replace with your password

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        speak("Email sent successfully!")
    except Exception as e:
        print(e)
        speak("Failed to send the email.")

def get_weather(city):
    api_key = "YOUR_OPENWEATHER_API_KEY"  # Replace with your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        weather_data = response.json()
        if weather_data["cod"] == 200:
            temp = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp} degrees Celsius with {description}.")
        else:
            speak("Sorry, I couldn't find the weather information for that location.")
    except Exception as e:
        print(e)
        speak("Failed to retrieve weather data.")

def set_reminder(reminder_text, reminder_time):
    speak(f"Reminder set for {reminder_time}")
    current_time = datetime.datetime.now()
    target_time = datetime.datetime.strptime(reminder_time, "%I:%M %p")

    while datetime.datetime.now() < target_time:
        time.sleep(10)
    
    speak(f"Reminder: {reminder_text}")

def run_voice_assistant():
    speak("Hello! How can I assist you today?")
    while True:
        query = listen()

        if query:
            if "time" in query:
                tell_time()
            elif "date" in query:
                tell_date()
            elif "search for" in query:
                search_query = query.replace("search for", "").strip()
                search_web(search_query)
            elif "email" in query:
                speak("Who is the recipient?")
                recipient = listen()
                if recipient:
                    recipient_email = f"{recipient}@example.com"  # Replace with actual email fetching logic
                    speak("What is the subject?")
                    subject = listen()
                    speak("What should I write in the email?")
                    body = listen()
                    send_email(recipient_email, subject, body)
            elif "weather" in query:
                speak("Please tell me the city name.")
                city = listen()
                if city:
                    get_weather(city)
            elif "remind me" in query:
                speak("What should I remind you about?")
                reminder_text = listen()
                speak("At what time? Please say in the format 'hour minute am or pm'")
                reminder_time = listen()
                if reminder_text and reminder_time:
                    set_reminder(reminder_text, reminder_time)
            elif "exit" in query or "quit" in query or "stop" in query:
                speak("Goodbye!")
                break
            else:
                speak("I'm sorry, I didn't understand that command.")

if __name__ == "__main__":
    run_voice_assistant()
