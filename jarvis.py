import pyttsx3
import datetime
import speech_recognition as sr 
import wikipedia
import webbrowser 
import os
import smtplib
import requests
import google.generativeai as genai 
import tempfile
import pygame
from gtts import gTTS


# Initialize the text-to-speech engine
# pip install pyttsx3       
# pip install pyaudio
# pip install SpeechRecognition
# pip install wikipedia
# pip install webbrowser`
# pip install smtplib`

engine = pyttsx3.init('sapi5')  # sapi5 is the Windows inbuilt voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)  # Set the speech rate (words per minute)
# newsapi = "f2e280f0265a40678a97cc7f3d041df0"  # Replace with your actual News API key

def speak_elevenlaps(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        print("GOOD MORNING")
        speak_elevenlabs("GOOD MORNING")
    elif 12 <= hour < 18:
        print("GOOD AFTERNOON")
        speak_elevenlabs("GOOD AFTERNOON")
    else:
        print("GOOD EVENING")
        speak_elevenlabs("GOOD EVENING")
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    print(strTime)
    print("My name is ANAND BABY, your personal assistant. How can I help you!")
    speak_elevenlabs("My name is ANAND BABY , your personal assistant. How can I help you!")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1.5  # Increase pause threshold for longer sentences
        r.energy_threshold = 250  # Lower for better sensitivity
        try:
            # Increase phrase_time_limit and timeout for longer input
            audio = r.listen(source, timeout=10, phrase_time_limit=60)
        except sr.WaitTimeoutError:
            print("Listening timed out, please speak again.")
            speak_elevenlabs("Listening timed out, please speak again.")
            return "None"
    try:
        print("Recognizing....")
        # Use Google recognizer for better accuracy and reliability
        query = r.recognize_google(audio, language='en-in', show_all=False)
        print(f"User said: {query}\n")
        if query.lower() == "mia":
            speak_elevenlabs("Hello, how are you doing today? How can I help you?")
    except sr.UnknownValueError:
        print("Sorry, I did not catch that. Please say that again.")
        speak_elevenlabs("Sorry, I did not catch that. Please say that again.")
        return "None"
    except sr.RequestError:
        print("Sorry, I am unable to connect to the speech recognition service.")
        speak_elevenlabs("Sorry, I am unable to connect to the speech recognition service.")
        return "None"
    return query

# OpenAI integration

# Process the command using OpenAI's GPT model

def google_gemini(prompt):
    try:
        api_key = "AIzaSyC8CszH0b5cEQyYkA9pGlQXTexMQRqcJU4"
        if not api_key:
            speak_elevenlabs("Google Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
            print("Google Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
            return "Google Gemini API key not found."
        genai.configure(api_key= "AIzaSyC8CszH0b5cEQyYkA9pGlQXTexMQRqcJU4")
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        # Try to extract the text from the response
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif hasattr(response, "candidates") and response.candidates:
            # Try to extract from candidates if available
            candidate = response.candidates[0]
            if hasattr(candidate, "content") and hasattr(candidate.content, "parts") and candidate.content.parts:
                part = candidate.content.parts[0]
                if hasattr(part, "text"):
                    return part.text.strip()
        speak_elevenlabs("Sorry, I did not receive a valid response from Google Gemini.")
        print("No valid response from Google Gemini.")
        return "Sorry, I did not receive a valid response from Google Gemini."
    except Exception as e:
        speak_elevenlabs("Sorry, there was an error processing your request with Google Gemini.")
        print(f"Google Gemini API error: {e}")
        return "Sorry, there was an error processing your request with Google Gemini."
   

def speak_elevenlabs(text):
    try:
        tts = gTTS(text=text, lang='en', tld='co.in', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
        tts.save(temp_path)
        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.quit()
        os.remove(temp_path)
    except Exception as e:
        print(f"gTTS error: {e}")
        engine.say(text)
        engine.runAndWait()



def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('thakralanmol17@gmail.com', 'cnen basq awua jcli')
    server.sendmail('thakralanmol2006@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishme()
    # while True:
    
    while (True):
         query = takecommand()  # Convert the query to lowercase for easier matching
         if 'hello' in query.lower() or 'hi' in query.lower():
                speak_elevenlabs("Hello, how can I assist you today?")
                print("Hello, how can I assist you today?")
        
         if 'wikipedia' in query.lower():
             speak_elevenlabs('Searching wikipedia...')
             query = query.replace("wikipedia", "")       
             results = wikipedia.summary(query , sentences=10)
             speak_elevenlabs("Accourding to wikipedia") 
             print(results)
             speak_elevenlabs(results) 
        
         elif 'open youtube' in query.lower():
             speak_elevenlabs("opening youtube......")
             print("opening youtube......")
             webbrowser.open("youtube.com")

         elif 'open facebook' in query.lower():
                speak_elevenlabs("opening facebook.....")
                print("opening facebook.....")
                webbrowser.open("facebook.com")

         elif 'what is battery ' in query.lower():
             battery = psutil.sensors_battery() # type: ignore
             percent = battery.percent
             speak_elevenlabs(f"Battery percentage is {percent} percent")
             print(f"Battery percentage is {percent} percent")              

         elif 'open whatsapp' in query.lower():
             speak_elevenlabs("opening whatsapp.....")
             print("opening whatsapp.....")
             webbrowser.open("whatsapp.com")
         elif 'open google' in query.lower():
             speak_elevenlabs("opening google....")
             print("opening google....")
             
             google = "C:\\Users\\Public\\Desktop\\Google Chrome.lnk"
             os.startfile(google)

         elif 'open jio hotstar' in query.lower():
             speak_elevenlabs("opening jio hotstar....")
             print("opening jio hotstar....")
             webbrowser.open("https://www.jiohotstar.com/")

         elif 'open gmail' in query.lower():
             speak_elevenlabs("opening gmail....")
             print("opening gmail....")
             webbrowser.open("gmail.com")
         elif 'news' in query.lower():
             
             speak_elevenlabs("Here are the top news headlines for today.")
             print("Here are the top news headlines for today.")
        
             r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey=f2e280f0265a40678a97cc7f3d041df0")
             if r.status_code == 200:
                news_data = r.json()
                if news_data.get("status") != "ok":
                    speak_elevenlabs("There was a problem with the News API request. Please check your API key.")
                    print("There was a problem with the News API request. Please check your API key.")
                else:
                    articles = news_data.get('articles', [])
                    if articles:
                        for i, article in enumerate(articles[:5], start=1):
                            title = article.get('title', 'No title available')
                            description = article.get('description', 'No description available')
                            speak_elevenlabs(f"News {i}: {title}")
                            print(f"News {i}: {title}")
                            if description and description != 'No description available':
                                speak_elevenlabs(f"Description: {description}")
                                print(f"Description: {description}")
                    else:
                        speak_elevenlabs("No news articles found. Please check if your API key is correct or try again later.")
                        print("No news articles found. Please check if your API key is correct or try again later.")
             else:
                print("Sorry, I couldn't fetch the news at the moment.")
                speak_elevenlabs("Sorry, I couldn't fetch the news at the moment.")
               

         
    
        
         elif 'open instagram' in query.lower():
             speak_elevenlabs("opening instagram.....")
             print("opening instagram.....")
             instagram = "C:\\Users\\thakr\\OneDrive\\Desktop\\Instagram.lnk"
             os.startfile(instagram)
         elif 'open snapchat' in query.lower():
             speak_elevenlabs("opening snapchat....")
             print("opening snapchat....")
             webbrowser.open("snapchat.com")
         elif 'open linkedin' in query.lower():
             speak_elevenlabs("opening linkedin....")
             print("opening linkedin....")
             webbrowser.open("https://linkedin.com")
         elif ' open netflix' in query.lower():
             webbrowser.open("https://netmirror.vip//get-app-free/")

         elif 'open roblox' in query.lower():
             speak_elevenlabs("opening roblox....")
             print("opening roblox....")
             roblox = "C:\\Users\\thakr\\AppData\\Local\\Roblox\\Versions\\version-2a06298afe3947ab\\RobloxPlayerBeta.exe"
             os.startfile(roblox)
         elif 'play pc games' in query.lower():
             speak_elevenlabs("opening pc games....")
             print("opening pc games....")
             webbrowser.open("https://www.crazygames.com/")

         elif 'play music' in query.lower():
             music_dir = 'C:\\Users\\thakr\\OneDrive\\Music'
             songs = os.listdir(music_dir)
             print(songs)
             if songs:
                 speak_elevenlabs("Please tell me the name of the song you want to play.")
                 print("Please tell me the name of the song you want to play.")
                 song_name = takecommand().lower()
                 found = False
                 for song in songs:
                     if song_name in song.lower():
                         os.startfile(os.path.join(music_dir, song))
                         speak_elevenlabs(f"Playing {song}")
                         print(f"Playing {song}")
                         found = True
                         break
                 if not found:
                     speak_elevenlabs("Sorry, I could not find that song in your music directory.")
                     print("Sorry, I could not find that song in your music directory.")
             else:
                 speak_elevenlabs("No music files found in your music directory.")
                 print("No music files found in your music directory.")

         elif 'the time' in query.lower():
             strTime = datetime.datetime.now().strftime("%H:%M:%S") 
             speak_elevenlabs(strTime)
             print(strTime) 
         elif 'shut down' in query.lower():
             speak_elevenlabs("Shutting down the computer in 10 seconds. Please save your work.")
             print("Shutting down the computer in 10 seconds. Please save your work.")
             os.system("shutdown /s /f /t 10")
         elif 'restart' in query.lower():
              speak_elevenlabs("Restarting the computer in 10 seconds. Please save your work.")
              print("Restarting the computer in 10 seconds. Please save your work.")
              os.system("shutdown/r/t/10")

         elif 'open command prompt' in query.lower():
                speak_elevenlabs("Opening command prompt...")
                print("Opening command prompt...")
                os.system("start cmd")

         elif 'open calculator' in query.lower():
             speak_elevenlabs("Opening calculator...")
             print("Opening calculator...")
             os.system("start calc")

         elif 'open notepad' in query.lower():
                speak_elevenlabs("Opening notepad...")
                print("Opening notepad...")
                os.system("start notepad")

         elif 'open file explorer' in query.lower():
                speak_elevenlabs("Opening file explorer...")    
                print("Opening file explorer...")
                os.system("explorer")

         elif 'open microsoft edge' in query.lower():
                speak_elevenlabs("Opening Microsoft Edge...")
                print("Opening Microsoft Edge...")
                edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
                os.startfile(edge_path)

         elif 'open google chrome' in query.lower():
             speak_elevenlabs("Opening Google Chrome...")
             print("Opening Google Chrome...")
             chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
             os.startfile(chrome_path)

        

         elif 'open vs code' in query.lower () or 'open visual studio code' in query.lower():
             codepath = "C:\\Users\\thakr\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
             os.startfile(codepath)

         elif 'open my favorite photo' in query.lower():
             photo = "C:\\Users\\thakr\\CrossDevice\\realme narzo 60x 5G\\storage\\DCIM\\Snapchat\\Snapchat-157455161.jpg"
             os.startfile(photo)

         elif 'play my favorite music'in query.lower():
             music = "C:\\Users\\thakr\\OneDrive\\Music\\Pal Pal Dil Ke Paas (From Blackmail).mp3"
             os.startfile(music)

         elif 'open my favorite video' in query.lower():
                video = "C:\\Users\\thakr\\CrossDevice\\realme narzo 60x 5G\\storage\\DCIM\\Snapchat\\Snapchat-204965002.mp4"
                os.startfile(video)
         
         
         elif 'email to anmol' in query.lower():
             try:
                 speak_elevenlabs("What should I say?")
                 content = takecommand()
                 to = "thakralanmol2006@gmail.com"
                 sendEmail(to, content)
                 speak_elevenlabs("Email has been sent!")
             except Exception as e:
                 print(e)
                 speak_elevenlabs("Sorry my friend Anmol chote bhai. I am not able to send this email")

         elif 'exit' in query.lower() or 'quit' in query.lower():
             speak_elevenlabs("Thank you for using me, have a nice day!")
             print("Thank you for using me, have a nice day!")
             break
         
         else:
             # Try Google Gemini as a fallback if ElevenLabs is not used
             prompt = query
             output = google_gemini(prompt)
             speak_elevenlabs(output)
             print(output)
            
        # To use ElevenLabs for all responses, uncomment the next line:
         speak = speak_elevenlabs



        
        

        

        
    
