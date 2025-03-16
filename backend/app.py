from flask import Flask, request, jsonify
from transformers import pipeline, AutoProcessor, MusicgenForConditionalGeneration
import torch
import scipy.io.wavfile
import numpy as np
import logging
from flask_cors import CORS
import os
import base64
import time

app = Flask(__name__)
CORS(app)

# Load the text generation model (GPT-Neo 1.3B)
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B", device=-1)

# Load the music generation model (MusicGen Small)
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
music_model = MusicgenForConditionalGeneration.from_pretrained(
    "facebook/musicgen-small",
    attn_implementation="eager",
)

# @app.route('/generate-lyrics', methods=['POST'])
# def generate_lyrics():
#     try:
#         data = request.json
#         music_style = data.get("music_style", "pop")
#         theme = data.get("theme", "love")
#         length = data.get("length", 350)
#         emotion = data.get("emotion", "happy")
#         structure = data.get("structure", "verse-chorus-verse")

#         # A simpler example prompt. Feel free to tweak text:
#         prompt = f"""
#         Write a {emotion} {music_style} song about {theme}.
#         Use a structure with verses and a chorus, like this:

#         [Verse 1]
#         ...

#         [Chorus]
#         ...

#         [Verse 2]
#         ...
#         Please continue now with original lyrics:
#         """

#         print(f"Now start to generate lyrics")
#         start_time = time.time() 

#         # Generate text from the prompt
#         generated = generator(
#             prompt,
#             max_new_tokens=length + 50,
#             min_new_tokens=length - 50,
#             num_return_sequences=1,
#             temperature=0.7,
#             repetition_penalty=1.6,
#             do_sample=True,
#             top_k=40,
#             top_p=0.9,
#             truncation=True,
#             # return_full_text=False
#         )

#         end_time = time.time()  # Record the end time
#         print(f"Now end to generate lyrics")
#         print(f"Time taken to generate lyrics: {end_time - start_time:.2f} seconds")

#         generated_text = generated[0]["generated_text"]

#         # 1) If the output starts with your prompt, remove that prompt portion
#         if generated_text.startswith(prompt):
#             generated_text = generated_text[len(prompt):]

#         # 2) Check stop tokens, and if found (beyond prompt text), cut them off
#         stop_tokens = ["--END--", "Verse 1:", "Chorus:", "Bridge:", "Outro:"]
#         for token in stop_tokens:
#             # Only remove if it occurs well after the prompt
#             idx = generated_text.find(token)
#             if idx != -1 and idx > 50:
#                 generated_text = generated_text[:idx]

#         # 3) Remove duplicate lines
#         lines = generated_text.strip().split("\n")
#         unique_lines = []
#         for line in lines:
#             if line.strip() and line not in unique_lines:
#                 unique_lines.append(line.strip())
#         cleaned_text = "\n".join(unique_lines)

#         return jsonify({"lyrics": cleaned_text})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/generate-music', methods=['POST'])
# def generate_music():
#     try:
#         data = request.json
#         des = data.get("des", "")

#         if not des:
#             return jsonify({"error": "des text is required"}), 400

#         inputs = processor(text=[des], padding=True, return_tensors="pt")

#         start_time = time.time() 

#         with torch.no_grad():
#             audio_tokens = music_model.generate(
#                 **inputs,
#                 max_new_tokens=1024,
#                 do_sample=True,
#                 temperature=1.2,
#                 top_k=50,
#                 top_p=0.95
#             )
        
#         end_time = time.time()  # Record the end time
#         print(f"Now end to generate music")
#         print(f"Time taken to generate music: {end_time - start_time:.2f} seconds")

#         audio_array = audio_tokens[0].cpu().numpy()

#         sampling_rate = getattr(music_model.config, "sampling_rate", 32000)
#         if not isinstance(sampling_rate, int) or sampling_rate <= 0 or sampling_rate > 65535:
#             sampling_rate = 32000
#         print(f"Using sampling rate: {sampling_rate}")

#         print(f"Generated audio shape: {audio_array.shape}")
#         print(f"Audio min: {audio_array.min()}, max: {audio_array.max()}")

#         if audio_array.size == 0:
#             return jsonify({"error": "Generated audio is empty"}), 500

#         audio_array = np.clip(audio_array, -1.0, 1.0)

#         if len(audio_array.shape) > 1 and audio_array.shape[0] > audio_array.shape[1]:
#             audio_array = audio_array.T

#         if len(audio_array.shape) > 1:
#             audio_array = np.mean(audio_array, axis=0)

#         scaled_audio = (audio_array * 32767).astype(np.int16)

#         print(f"Scaled audio min: {scaled_audio.min()}, max: {scaled_audio.max()}")

#         save_directory = os.path.join(os.getcwd(), "generated_music.wav")
#         print(f"Saving generated music to: {save_directory}")

#         scipy.io.wavfile.write(save_directory, rate=int(sampling_rate), data=scaled_audio)

#         with open(save_directory, 'rb') as f:
#             wav_data = f.read()
#         b64_wav_data = base64.b64encode(wav_data).decode('utf-8')

#         return jsonify({
#             "message": "Music generated successfully",
#             "sampling_rate": sampling_rate,
#             "audio_data_base64": b64_wav_data
#         })
    
#     except Exception as e:
#         logging.exception("Error in generate_music:")
#         return jsonify({"error": str(e)}), 500

# return pre-defined lyrics
@app.route('/generate-lyrics', methods=['POST'])
def generate_lyrics():
    try:
        data = request.json
        music_style = data.get("music_style", "pop")
        theme = data.get("theme", "love")
        emotion = data.get("emotion", "happy")
        
        predefined_lyrics = f"""
Title: A Beautiful Tale

Lyrics:

[Verse 1]
Walking through the city streets
Memories dance around my feet
All the moments that we shared
In this place, floating through the air
The lights reflect in puddles deep
Stories that we couldn't keep

[Chorus]
And I'm holding on to yesterday
As the world just fades away
In a lonely melody
That reminds me constantly
Of a adventure that shaped my soul
A beautiful tale never told

[Verse 2]
Seasons change like our hearts do
Winter comes with skies of blue
But I feel strange when I recall
How we stood so proud and tall
Against the world that tried to break
All the promises we'd make
"""

        time.sleep(200)
        return jsonify({"lyrics": predefined_lyrics})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-music', methods=['POST'])
def generate_music():
    try:
        data = request.json
        des = data.get("des", "")

        if not des:
            return jsonify({"error": "des text is required"}), 400
            
        time.sleep(3)  
        
        save_directory = os.path.join(os.getcwd(), "generated_music.wav")
        
        if not os.path.exists(save_directory):
            return jsonify({"error": "Pre-generated audio file not found"}), 404
        
        try:
            sampling_rate, _ = scipy.io.wavfile.read(save_directory)
        except:
            sampling_rate = 32000  
        
        with open(save_directory, 'rb') as f:
            wav_data = f.read()
        b64_wav_data = base64.b64encode(wav_data).decode('utf-8')
        
        print(f"Returning pre-generated music file: {save_directory}")
        
        return jsonify({
            "message": "Music generated successfully",
            "sampling_rate": sampling_rate,
            "audio_data_base64": b64_wav_data
        })
    
    except Exception as e:
        logging.exception("Error in generate_music:")
        return jsonify({"error": str(e)}), 500
        
if __name__ == '__main__':
    app.run(debug=True, port=5000) 
