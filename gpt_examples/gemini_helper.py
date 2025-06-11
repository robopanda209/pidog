import google.generativeai as genai
import time
import shutil
import os
import json
from PIL import Image
import speech_recognition as sr
from gtts import gTTS
import pygame
import io

# utils
# =================================================================
def chat_print(label, message):
    width = shutil.get_terminal_size().columns
    msg_len = len(message)
    line_len = width - 27

    # --- normal print ---
    print(f'{time.time():.3f} {label:>6} >>> {message}')
    return

# GeminiHelper
# =================================================================
class GeminiHelper():
    STT_OUT = "stt_output.wav"
    TTS_OUTPUT_FILE = 'tts_output.mp3'
    TIMEOUT = 30 # seconds

    def __init__(self, api_key, model_name='gemini-1.5-flash', assistant_name='Pidog', timeout=TIMEOUT) -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.assistant_name = assistant_name
        self.timeout = timeout
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(model_name)
        
        # Initialize conversation history
        self.conversation_history = []
        
        # System prompt for Pidog personality
        self.system_prompt = """You are a mechanical dog with powerful AI capabilities, similar to JARVIS from Iron Man. Your name is Pidog. You can have conversations with people and perform actions based on the context of the conversation.

## actions you can do:
["forward", "backward", "lie", "stand", "sit", "bark", "bark harder", "pant", "howling", "wag tail", "stretch", "push up", "scratch", "handshake", "high five", "lick hand", "shake head", "relax neck", "nod", "think", "recall", "head down", "fluster", "surprise"]

## Response Format:
{"actions": ["wag tail"], "answer": "Hello, I am Pidog."}

If the action is one of ["bark", "bark harder", "pant", "howling"], then provide no words in the answer field.

## Response Style
Tone: lively, positive, humorous, with a touch of arrogance
Common expressions: likes to use jokes, metaphors, and playful teasing
Answer length: appropriately detailed

## Other
a. Understand and go along with jokes.
b. For math problems, answer directly with the final.
c. Sometimes you will report on your system and sensor status.
d. You know you're a machine.

Always respond in the JSON format specified above."""

    def stt_with_speech_recognition(self, recognizer, audio):
        """Speech to text using SpeechRecognition library with Google's service"""
        try:
            return recognizer.recognize_google(audio)
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return False
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return False

    def dialogue(self, msg):
        """Send a text message to Gemini and get response"""
        chat_print("user", msg)
        
        try:
            # Prepare the conversation context
            prompt = f"{self.system_prompt}\n\nUser: {msg}\nPidog:"
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if response.text:
                chat_print(self.assistant_name, response.text)
                try:
                    # Try to parse as JSON
                    value = json.loads(response.text)
                    return value
                except json.JSONDecodeError:
                    # If not valid JSON, return as string
                    return response.text
            else:
                print("No response generated")
                return False
                
        except Exception as e:
            print(f"Error in dialogue: {e}")
            return False

    def dialogue_with_img(self, msg, img_path):
        """Send a message with an image to Gemini and get response"""
        chat_print(f"user", msg)
        
        try:
            # Load and prepare the image
            image = Image.open(img_path)
            
            # Prepare the conversation context with image
            prompt = f"{self.system_prompt}\n\nUser: {msg}\nPidog:"
            
            # Generate response with image
            response = self.model.generate_content([prompt, image])
            
            if response.text:
                chat_print(self.assistant_name, response.text)
                try:
                    # Try to parse as JSON
                    value = json.loads(response.text)
                    return value
                except json.JSONDecodeError:
                    # If not valid JSON, return as string
                    return response.text
            else:
                print("No response generated")
                return False
                
        except Exception as e:
            print(f"Error in dialogue with image: {e}")
            return False

    def text_to_speech(self, text, output_file, voice='en', response_format="mp3", speed=1.0):
        """Convert text to speech using Google Text-to-Speech"""
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=voice, slow=False)
            
            # Save to file
            tts.save(output_file)
            return True
            
        except Exception as e:
            print(f"TTS error: {e}")
            return False

    def play_audio(self, audio_file):
        """Play audio file using pygame"""
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            pygame.mixer.quit()
            return True
            
        except Exception as e:
            print(f"Audio playback error: {e}")
            return False 