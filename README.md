# Note Taker Demo
This is to download[NoteTaker Demo for Windows](https://drive.google.com/file/d/1DMjpb8vtG0tsCZqnJEAoCJr0B6aTPV0M/view?usp=sharing)

# AI Lyrics Generator

This project features a Flask backend and a React frontend that generates AI-powered song lyrics based on user input. Users can customize the lyrics by specifying parameters such as music style, theme, length, and structure. Additionally, they can edit the generated lyrics in an integrated editor, copy the text, or export it as a PDF.


## Developers

- xx
- xx
- xx
- **Yifei Shang**
Contact: https://www.linkedin.com/in/yifei-s-b3b013221
- **Sinian Liu**  
Contact: https://www.linkedin.com/in/sinian-liu/

## Requirements

- Python 
- Flask
- React
- Tailwind
- Pytorch
- Other dependencies (see requirements.txt)

## Preview
![image](https://github.com/user-attachments/assets/266e2205-b35d-43d9-afed-f543e32839e6)

## 📌 Backend Requirements

### 1️⃣ Place your [app.py](backend/app.py) to your backend root directory

### 2️⃣ Make sure you have the following dependencies installed:
```sh
pip install flask flask-cors transformers torch scipy
```
### 3️⃣ run flask server:
```sh
python app.py
```
>Dont forget to wait for debuger pin show up

### 4️⃣ Test the API using curl:
```sh
curl -X POST "http://127.0.0.1:5000/generate-lyrics" -H "Content-Type: application/json" -d "{\"music_style\": \"rock\", \"theme\": \"adventure\", \"length\": 250, \"emotion\": \"exciting\", \"structure\": \"verse-chorus-verse\"}"
```
### 4️⃣ Test the API using curl for music:
```sh
curl -X POST "http://127.0.0.1:5000/generate-music" -H "Content-Type: application/json" -d "{\"des\": \"Upbeat pop track with a driving beat and bright, uplifting chords. Inspired by modern synth-pop.\"}"
```
>[!NOTE]
>⚡Adjust the split to fill the needs:  
Feel free to change ***\n*** to any symbol to suit your needs
```
lines = generated_text.strip().split("\n")
```
## Frontend Development Guide:
### 1️⃣ Ensure this React useState setup:
```
const [formData, setFormData] = useState({
    music_style: "rock",
    theme: "adventure",
    length: 250,
    emotion: "exciting",
    structure: "verse-chorus-verse",
});
```
### 2️⃣ Make the API request using Axios:
```
const response = await axios.post("http://127.0.0.1:5000/generate-lyrics", formData, {
    headers: { "Content-Type": "application/json" },
});
```
### 3️⃣ Create an Input Field for User Input  
Allowing users to update formData dynamically:
```
<input type="text" name="music_style" value={formData.music_style} onChange={handleChange} />
```

## Installation
1. Clone the repository:
```sh
git clone https://github.com/MintFlavor23/ai-music-generator.git
```
2. Run the frontend:
```sh
cd ai-music-frontend
npm install
npm start
```
3. Open your browser and go to  http://localhost:3000

3. Run the backend:
```sh
cd backend
pip install flask flask-cors transformers torch
python app.py
```


## App Usage
1. Enter your desired parameters in the input box, or leave them blank if not needed.
2. Click "Generate Lyrics" to display the output editor on the right.
3. Once the AI finishes generating the lyrics, you can edit them directly in the editor.
4. Use the first button in the bottom-right corner to copy the text and the second button to export it as a PDF.

## License
[MIT License](./LICENSE)
