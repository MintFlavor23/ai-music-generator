# note taker Demo
This is to download[NoteTaker Demo for Windows](https://drive.google.com/file/d/1DMjpb8vtG0tsCZqnJEAoCJr0B6aTPV0M/view?usp=sharing)

# AI Lyrics Generator

This project consists of a Flask backend and a React frontend that generates AI-powered song lyrics based on user input.

---

## 📌 Backend Requirements

### 1️⃣Place your [app.py](backend/app.py) to your backend root directory

### 2️⃣Make sure you have the following dependencies installed:
```sh
pip install flask flask-cors transformers torch
```
### 3️⃣run flask server:
```sh
python app.py
```
>Dont forget to wait for debuger pin show up

### 4️⃣Test the API using curl:
```sh
curl -X POST "http://127.0.0.1:5000/generate-lyrics" -H "Content-Type: application/json" -d "{\"music_style\": \"rock\", \"theme\": \"adventure\", \"length\": 250, \"emotion\": \"exciting\", \"structure\": \"verse-chorus-verse\"}"
```
>[!NOTE]
>⚡Adjust the split to fill the needs:
Feel free to change ***\n*** to any symbol to suit your needs
```
lines = generated_text.strip().split("\n")
```
# Frontend Development Guide:
### 1️⃣Ensure this React useState setup:
```
const [formData, setFormData] = useState({
    music_style: "rock",
    theme: "adventure",
    length: 250,
    emotion: "exciting",
    structure: "verse-chorus-verse",
});
```
### 2️⃣Make the API request using Axios:
```
const response = await axios.post("http://127.0.0.1:5000/generate-lyrics", formData, {
    headers: { "Content-Type": "application/json" },
});
```
### 3️⃣Create an Input Field for User Input  
Allowing users to update formData dynamically:
```
<input type="text" name="music_style" value={formData.music_style} onChange={handleChange} />
```
