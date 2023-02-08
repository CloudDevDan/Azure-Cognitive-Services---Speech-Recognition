import os
import time
import azure.cognitiveservices.speech as speechsdk

def speech_recognize_continuous():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language="en-GB"
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False
    all_results = []

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    def handle_final_result(evt):
        all_results.append(evt.result.text)

    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING:{}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED:{}'.format(evt)))
    speech_recognizer.recognized.connect(handle_final_result)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED:{}'.format(evt)))
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        print('type "stop" then enter when done')
        stop = input()
        if (stop.lower() == "stop"):
            print('Stopping async recognition.')
            print(all_results)
            with open("output.txt", "w") as txt_file:
                for line in all_results:
                    txt_file.write(line + "\n")
            break

speech_recognize_continuous()