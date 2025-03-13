from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B", device=-1)

@app.route('/generate-lyrics', methods=['POST'])
def generate_lyrics():
    try:
        data = request.json
        music_style = data.get("music_style", "pop")
        theme = data.get("theme", "love")
        length = data.get("length", 350)
        emotion = data.get("emotion", "happy")
        structure = data.get("structure", "verse-chorus-verse")

        # Improved prompt for better structure
        prompt = f"""
        This is an {emotion} {music_style} song about {theme}.

        [Verse 1]
        The journey begins, with a fire inside,
        Wind at our backs, nowhere to hide.
        We chase the thrill, the open sky,
        No fear tonight, we’re ready to fly.

        [Chorus]
        We're running fast, we're feeling free,
        The road is ours, as wild as the sea.
        No turning back, just let it be,
        The world is calling, can't you see?

        [Verse 2]
        """

        generated = generator(
            prompt,
            max_length=length,
            min_length=length - 50,
            num_return_sequences=1,
            temperature=0.7,
            repetition_penalty=1.6,
            do_sample=True,
            top_k=40,
            top_p=0.9
        )

        generated_text = generated[0]["generated_text"]
        
        # Remove unintended tokens or extra prompts
        stop_tokens = ["--END--", "Verse 1:", "Chorus:", "Bridge:", "Outro:"]
        for token in stop_tokens:
            if token in generated_text and generated_text.index(token) > len(prompt) + 50:  
                generated_text = generated_text.split(token)[0]

        # Remove duplicate lines for better flow
        lines = generated_text.strip().split("\n")
        unique_lines = []
        for line in lines:
            if line not in unique_lines:
                unique_lines.append(line)
        cleaned_text = "\n".join(unique_lines)

        return jsonify({"lyrics": cleaned_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)