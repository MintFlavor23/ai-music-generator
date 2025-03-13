# note taker Demo
This is to download[NoteTaker Demo for Windows](https://drive.google.com/file/d/1DMjpb8vtG0tsCZqnJEAoCJr0B6aTPV0M/view?usp=sharing)

# AI Lyrics Generator

This project consists of a Flask backend and a React frontend that generates AI-powered song lyrics based on user input.

---

## 📌 Backend Requirements

Place your [app.py](backend/app.py) to your backend root directory
> [!IMPORTANT]
> Make sure you have the following dependencies installed:
```sh
pip install flask flask-cors transformers torch
```
run server:
```sh
python app.py
```
> [!NOTE]
> dont forget to wait for debuger pin show up

Test the API using curl:
```sh
curl -X POST "http://127.0.0.1:5000/generate-lyrics" -H "Content-Type: application/json" -d "{\"music_style\": \"rock\", \"theme\": \"adventure\", \"length\": 250, \"emotion\": \"exciting\", \"structure\": \"verse-chorus-verse\"}"
```

# Frontend Development Guide:
Ensure this React useState setup:
```
const [formData, setFormData] = useState({
    music_style: "rock",
    theme: "adventure",
    length: 250,
    emotion: "exciting",
    structure: "verse-chorus-verse",
});
```
Make the API request using Axios:
```
const response = await axios.post("http://127.0.0.1:5000/generate-lyrics", formData, {
    headers: { "Content-Type": "application/json" },
});
```
Then request input to change the formData:
```
<input type="text" name="music_style" value={formData.music_style} onChange={handleChange} />
```
