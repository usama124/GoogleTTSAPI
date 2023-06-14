#!/usr/bin/env python3
# IMPORTS
import json
import os.path
from pathlib import Path

from google.cloud import texttospeech
from google.cloud import texttospeech_v1beta1 as tts

# GLOBALS
carpeta = ''
comprimido = ''
fichero = ''
tono = 0
velocidad_voz = 1.07

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'boston-wolf-8fb4a41f2cb7.json'

configuracion_ssml = tts.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    pitch=tono,
    speaking_rate=velocidad_voz

)


def go_ssml(basename: Path, ssml):
    client = tts.TextToSpeechClient()
    voice = tts.VoiceSelectionParams(
        language_code="es-US",
        name="es-US-Neural2-B",
        ssml_gender=tts.SsmlVoiceGender.MALE,
    )

    response = client.synthesize_speech(
        request=tts.SynthesizeSpeechRequest(
            input=tts.SynthesisInput(ssml=ssml),
            voice=voice,
            # audio_config=tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16),
            audio_config=configuracion_ssml,
            enable_time_pointing=[
                tts.SynthesizeSpeechRequest.TimepointType.SSML_MARK]
        )
    )

    # cheesy conversion of array of Timepoint proto.Message objects into plain-old data
    marks = [dict(sec=t.time_seconds, name=t.mark_name)
             for t in response.timepoints]

    name = basename.with_suffix('.txt')
    with name.open('w') as out:
        json.dump(marks, out)
        print(f'Marks content written to file: {name}')

    name = basename.with_suffix('.mp3')
    with name.open('wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file: {name}')

    return name
