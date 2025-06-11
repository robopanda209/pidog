from gemini_helper import GeminiHelper
from gemini_keys import GEMINI_API_KEY, GEMINI_MODEL
from action_flow import ActionFlow
from utils import *

import readline # optimize keyboard input, only need to import

import speech_recognition as sr
from pidog import Pidog

import time
import threading
import random

import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_path)

input_mode = None
with_img = True
args = sys.argv[1:]
if '--keyboard' in args:
    input_mode = 'keyboard'
else:
    input_mode = 'voice'

if '--no-img' in args:
    with_img = False
else:
    with_img = True

# Gemini assistant init
# =================================================================
gemini_helper = GeminiHelper(GEMINI_API_KEY, GEMINI_MODEL, 'PiDog')

LANGUAGE = 'en'  # Language for speech recognition and TTS
# Supported TTS languages: 'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh', etc.

# VOLUME_DB = 5
VOLUME_DB = 3

VOICE_ACTIONS = ["bark", "bark harder", "pant", "howling"]

# dog init 
# =================================================================
try:
    my_dog = Pidog()
    time.sleep(1)
except Exception as e:
    raise RuntimeError(e)

action_flow = ActionFlow(my_dog)

# Vilib start
# =================================================================
if with_img:
    from vilib import Vilib
    import cv2

    Vilib.camera_start(vflip=False,hflip=False)
    Vilib.display(local=False,web=True)

    while True:
        if Vilib.flask_start:
            break
        time.sleep(0.01)

    time.sleep(.5)
    print('\n')

# speech_recognition init
# =================================================================
recognizer = sr.Recognizer()
recognizer.dynamic_energy_adjustment_damping = 0.16
recognizer.dynamic_energy_ratio = 1.6
recognizer.pause_threshold = 1.0

# speak_handler
# =================================================================
speech_loaded = False
speech_lock = threading.Lock()
tts_file = None

def speak_handler():
    global speech_loaded, tts_file
    while True:
        with speech_lock:
            _isloaded = speech_loaded
        if _isloaded:
            gray_print('speak start')
            my_dog.speak_block(tts_file)
            gray_print('speak done')
            with speech_lock:
                speech_loaded = False
        time.sleep(0.05)

speak_thread = threading.Thread(target=speak_handler)
speak_thread.daemon = True

# actions thread
# =================================================================
action_status = 'standby' # 'standby', 'think', 'actions', 'actions_done'
actions_to_be_done = []
action_lock = threading.Lock()

def action_handler():
    global action_status, actions_to_be_done

    standby_actions = ['waiting', 'feet_left_right']
    standby_weights = [1, 0.3]

    action_interval = 5 # seconds
    last_action_time = time.time()

    while True:
        with action_lock:
            _state = action_status
        if _state == 'standby':
            if time.time() - last_action_time > action_interval:
                choice = random.choices(standby_actions, standby_weights)[0]
                action_flow.run(choice)
                last_action_time = time.time()
                action_interval = random.randint(2, 6)
        elif _state == 'think':
            pass
        elif _state == 'actions':
            with action_lock:
                _actions = actions_to_be_done
            for _action in _actions:
                try:
                    action_flow.run(_action)
                except Exception as e:
                    print(f'action error: {e}')
                time.sleep(0.5)

            with action_lock:
                action_status = 'actions_done'
            last_action_time = time.time()

        time.sleep(0.01)

action_thread = threading.Thread(target=action_handler)
action_thread.daemon = True

# main
# =================================================================
def main():
    global speech_loaded
    global action_status, actions_to_be_done
    global tts_file

    my_dog.rgb_strip.close()
    action_flow.change_status(action_flow.STATUS_SIT)

    speak_thread.start()
    action_thread.start()

    while True:
        if input_mode == 'voice':
            # listen
            # ----------------------------------------------------------------
            gray_print("listening ...")

            with action_lock:
                action_status = 'standby'
            my_dog.rgb_strip.set_mode('listen', 'cyan', 1)

            _stderr_back = redirect_error_2_null() # ignore error print to ignore ALSA errors
            # If the chunk_size is set too small (default_size=1024), it may cause the program to freeze
            with sr.Microphone(chunk_size=8192) as source:
                cancel_redirect_error(_stderr_back) # restore error print
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            # stt
            # ----------------------------------------------------------------
            my_dog.rgb_strip.set_mode('boom', 'yellow', 0.5)

            st = time.time()
            _result = gemini_helper.stt_with_speech_recognition(recognizer, audio)
            gray_print(f"stt takes: {time.time() - st:.3f} s")

            if _result == False or _result == "":
                print() # new line
                continue

        elif input_mode == 'keyboard':
            with action_lock:
                action_status = 'standby'
            my_dog.rgb_strip.set_mode('listen', 'cyan', 1)

            _result = input(f'\033[1;30m{"input: "}\033[0m').encode(sys.stdin.encoding).decode('utf-8')

            if _result == False or _result == "":
                print() # new line
                continue

            my_dog.rgb_strip.set_mode('boom', 'yellow', 0.5)

        else:
            raise ValueError("Invalid input mode")

        # Gemini
        # ---------------------------------------------------------------- 
        response = {}
        st = time.time()

        with action_lock:
            action_status = 'think'

        if with_img:
            img_path = './img_input.jpg'
            cv2.imwrite(img_path, Vilib.img)
            response = gemini_helper.dialogue_with_img(_result, img_path)
        else:
            response = gemini_helper.dialogue(_result)

        gray_print(f'chat takes: {time.time() - st:.3f} s')

        # actions & TTS
        # ---------------------------------------------------------------- 
        try:
            if isinstance(response, dict):
                if 'actions' in response:
                    actions = list(response['actions'])
                else:
                    actions = ['stop']

                if 'answer' in response:
                    answer = response['answer']
                else:
                    answer = ''

                if len(answer) > 0:
                    _actions = list.copy(actions)
                    for _action in _actions:
                        if _action in VOICE_ACTIONS:
                            actions.remove(_action)
            else:
                response = str(response)
                if len(response) > 0:
                    actions = ['stop']
                    answer = response

        except:
            actions = ['stop']
            answer = ''
    
        try:
            # ---- tts ----
            _status = False
            if answer != '':
                st = time.time()
                _time = time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())
                _tts_f = f"./tts/{_time}_raw.mp3"
                _status = gemini_helper.text_to_speech(answer, _tts_f, voice=LANGUAGE)
                if _status:
                    tts_file = f"./tts/{_time}_{VOLUME_DB}dB.wav"
                    # Convert mp3 to wav and adjust volume
                    _status = sox_volume_mp3_to_wav(_tts_f, tts_file, VOLUME_DB)
                gray_print(f'tts takes: {time.time() - st:.3f} s')

                if _status:
                    with speech_lock:
                        speech_loaded = True
                    my_dog.rgb_strip.set_mode('speak', 'pink', 1)
            else:
                my_dog.rgb_strip.set_mode('breath', 'blue', 1)

            # ---- actions ----
            with action_lock:
                actions_to_be_done = actions
                gray_print(f'actions: {actions_to_be_done}')
                action_status = 'actions'

            # ---- wait speak done ----
            if _status:
                while True:
                    with speech_lock:
                        if not speech_loaded:
                            break
                    time.sleep(.01)

            # ---- wait actions done ----
            while True:
                with action_lock:
                    if action_status != 'actions':
                        break
                time.sleep(.01)

            ##
            print() # new line

        except Exception as e:
            print(f'actions or TTS error: {e}')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\033[31mERROR: {e}\033[m")
    finally:
        if with_img:
            Vilib.camera_close()
        my_dog.close() 