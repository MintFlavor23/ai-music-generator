from flask import Flask, request, jsonify
from transformers import pipeline, AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile
import numpy as np
import logging
from flask_cors import CORS
import os
import base64
import time
import requests
import torch

app = Flask(__name__)
CORS(app)

# Integrate local 'Anything LLM' tool
api_key = "5R2QZJF-ZMZ42BB-PKKFSQX-TCDB0TX"
workspace_id = "genm"
baseurl = "http://localhost:3001/api/v1"
chat_url = f"{baseurl}/workspace/{workspace_id}/chat" 

# Load the music generation model (MusicGen Small)
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
music_model = MusicgenForConditionalGeneration.from_pretrained(
    "facebook/musicgen-small",
    attn_implementation="eager",
)

@app.route('/generate-lyrics', methods=['POST'])
def generate_lyrics():
    try:
        data = request.json
        music_style = data.get("music_style", "pop")
        theme = data.get("theme", "love")
        length = data.get("length", 350)
        emotion = data.get("emotion", "happy")
        structure = data.get("structure", "verse-chorus-verse")

        # A simpler example prompt. Feel free to tweak text:
        prompt = f"""
        Write a {emotion} {music_style} song about this topic:{theme}.
        Important: The number of lyric words should be around {length}!

        Use the structure of {structure}. Below is the reference output format:

        Title: [Title of the song]

        Lyrics:

        [Verse 1]
        ...[Lyrics]...

        [Chorus]
        ...

        [Verse 2]
        ...

        You can now modify the structure and content of the song.
        """

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key
        }

        payload = {
            "message": prompt,
            "mode": "chat",
            "sessionId": "lyrics_generation",
            "attachments": []
        }

        print(f"Now start to generate lyrics")
        
        # Make request to the AI service
        response = requests.post(chat_url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Get the full response data
        response_data = response.json()
        
        # Print for debugging
        print("Full API response:", response_data)
        
        # Extract the actual lyrics text from the textResponse field
        lyrics_text = response_data.get('textResponse', 'No lyrics generated')
        
        # Return proper JSON response with the lyrics
        return jsonify({
            "lyrics": lyrics_text,
            "status": "success"
        })
    
    except requests.exceptions.RequestException as e:
        print(f"Error in calling chat API: {e}")
        return jsonify({"error": f"Error in calling chat API: {str(e)}"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route('/generate-music', methods=['POST'])
def generate_music():
    try:
        data = request.json
        des = data.get("des", "")

        if not des:
            return jsonify({"error": "des text is required"}), 400

        inputs = processor(text=[des], padding=True, return_tensors="pt")

        start_time = time.time() 

        with torch.no_grad():
            audio_tokens = music_model.generate(
                **inputs,
                max_new_tokens=1024,
                do_sample=True,
                temperature=1.2,
                top_k=50,
                top_p=0.95
            )
        
        end_time = time.time()  # Record the end time
        print(f"Now end to generate music")
        print(f"Time taken to generate music: {end_time - start_time:.2f} seconds")

        audio_array = audio_tokens[0].cpu().numpy()

        sampling_rate = getattr(music_model.config, "sampling_rate", 32000)
        if not isinstance(sampling_rate, int) or sampling_rate <= 0 or sampling_rate > 65535:
            sampling_rate = 32000
        print(f"Using sampling rate: {sampling_rate}")

        print(f"Generated audio shape: {audio_array.shape}")
        print(f"Audio min: {audio_array.min()}, max: {audio_array.max()}")

        if audio_array.size == 0:
            return jsonify({"error": "Generated audio is empty"}), 500

        audio_array = np.clip(audio_array, -1.0, 1.0)

        if len(audio_array.shape) > 1 and audio_array.shape[0] > audio_array.shape[1]:
            audio_array = audio_array.T

        if len(audio_array.shape) > 1:
            audio_array = np.mean(audio_array, axis=0)

        scaled_audio = (audio_array * 32767).astype(np.int16)

        print(f"Scaled audio min: {scaled_audio.min()}, max: {scaled_audio.max()}")

        save_directory = os.path.join(os.getcwd(), "generated_music.wav")
        print(f"Saving generated music to: {save_directory}")

        scipy.io.wavfile.write(save_directory, rate=int(sampling_rate), data=scaled_audio)

        with open(save_directory, 'rb') as f:
            wav_data = f.read()
        b64_wav_data = base64.b64encode(wav_data).decode('utf-8')

        return jsonify({
            "message": "Music generated successfully",
            "sampling_rate": sampling_rate,
            "audio_data_base64": b64_wav_data
        })
    
    except Exception as e:
        logging.exception("Error in generate_music:")
        return jsonify({"error": str(e)}), 500


# @app.route('/generate-music', methods=['POST'])
# def generate_music():
#     try:
#         data = request.json
#         des = data.get("des", "")

#         if not des:
#             return jsonify({"error": "des text is required"}), 400
            
#         time.sleep(3)  
        
#         save_directory = os.path.join(os.getcwd(), "generated_music.wav")
        
#         if not os.path.exists(save_directory):
#             return jsonify({"error": "Pre-generated audio file not found"}), 404
        
#         try:
#             sampling_rate, _ = scipy.io.wavfile.read(save_directory)
#         except:
#             sampling_rate = 32000  
        
#         with open(save_directory, 'rb') as f:
#             wav_data = f.read()
#         b64_wav_data = base64.b64encode(wav_data).decode('utf-8')
        
#         print(f"Returning pre-generated music file: {save_directory}")
        
#         return jsonify({
#             "message": "Music generated successfully",
#             "sampling_rate": sampling_rate,
#             "audio_data_base64": b64_wav_data
#         })
    
#     except Exception as e:
#         logging.exception("Error in generate_music:")
#         return jsonify({"error": str(e)}), 500
        
if __name__ == '__main__':
    app.run(debug=True, port=5000) 
