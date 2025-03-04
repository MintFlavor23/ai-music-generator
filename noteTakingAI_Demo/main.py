import os
import json
import wave
import re
import threading
import queue
import time
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
import pyaudio
from vosk import Model, KaldiRecognizer
import spacy
from transformers import pipeline
import wikipedia
Window.size = (900, 700)

KV = """
BoxLayout:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)

    MDRectangleFlatButton:
        text: "Start Recording"
        pos_hint: {"center_x": 0.5}
        on_release: app.start_recording()

    MDRectangleFlatButton:
        text: "Stop Recording"
        pos_hint: {"center_x": 0.5}
        on_release: app.stop_recording()

    MDLabel:
        text: "Live Transcript:"
        bold: True
        halign: "left"
        size_hint_y: None
        height: self.texture_size[1]

    ScrollView:
        MDLabel:
            id: transcript_label
            text: ""
            halign: "left"
            valign: "top"
            size_hint_y: None
            text_size: self.width, None
            height: self.texture_size[1]
            padding: dp(10), dp(10)

    MDRectangleFlatButton:
        text: "Summarize"
        pos_hint: {"center_x": 0.5}
        on_release: app.summarize_transcript()

    MDLabel:
        text: "Summary:"
        bold: True
        halign: "left"
        size_hint_y: None
        height: self.texture_size[1]

    ScrollView:
        MDLabel:
            id: summary_label
            text: ""
            halign: "left"
            valign: "top"
            size_hint_y: None
            text_size: self.width, None
            height: self.texture_size[1]
            padding: dp(10), dp(10)
            markup: True

    MDLabel:
        text: "Wikipedia Keywords (internet required):"
        bold: True
        halign: "left"
        size_hint_y: None
        height: self.texture_size[1]

    ScrollView:
        MDLabel:
            id: wiki_label
            text: ""
            halign: "left"
            valign: "top"
            size_hint_y: None
            text_size: self.width, None
            height: self.texture_size[1]
            padding: dp(10), dp(10)
"""

class MainLayout(MDBoxLayout):
    pass

class MyNoteTakerApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vosk_model_path = "vosk-model-small-en-us-0.15"
        if not os.path.exists(self.vosk_model_path):
            print("[Warning] Vosk model folder not found!")
        self.nlp = spacy.load("en_core_web_sm")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.audio_queue = queue.Queue()
        self.transcript_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.recording_thread = None
        self.full_transcript = ""
        self.partial_transcript = ""

    def start_recording(self):
        """Start the background thread for microphone capture + Vosk recognition."""
        self.stop_event.clear()
        self.full_transcript = ""
        self.partial_transcript = ""
        self.root.ids.summary_label.text = ""
        self.root.ids.wiki_label.text = ""
        self.root.ids.transcript_label.text = "[Recording in progress...]"
        self.recording_thread = threading.Thread(target=self.record_and_transcribe, daemon=True)
        self.recording_thread.start()

        Clock.schedule_interval(self.update_transcript_label, 0.5)

    def stop_recording(self):
        """Signal the background thread to stop recording."""
        self.stop_event.set()
        if self.recording_thread:
            self.recording_thread.join()
            self.recording_thread = None

        self.root.ids.transcript_label.text = self.full_transcript
        Clock.unschedule(self.update_transcript_label)

    def record_and_transcribe(self):
        """Background thread function: capture audio from mic and feed to Vosk for recognition."""
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=4096)

        model = Model(self.vosk_model_path)
        rec = KaldiRecognizer(model, 16000)

        try:
            while not self.stop_event.is_set():
                data = stream.read(4096, exception_on_overflow=False)
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    text = json.loads(result).get('text', '')
                    if text:
                        self.full_transcript += " " + text
                else:
                    partial = json.loads(rec.PartialResult()).get('partial', '')
                    self.partial_transcript = partial
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            final_result = json.loads(rec.FinalResult()).get('text', '')
            if final_result:
                self.full_transcript += " " + final_result

    def update_transcript_label(self, dt):
        """Called periodically to show partial results in the UI."""
        combined = self.full_transcript + " " + self.partial_transcript
        self.root.ids.transcript_label.text = combined.strip()

    def summarize_transcript(self):
        """Summarize the final transcript text (after recording is stopped)."""
        cleaned = self.clean_transcript(self.full_transcript)
        if not cleaned.strip():
            self.root.ids.summary_label.text = "[No transcript to summarize]"
            return
        summary_text = self.summarize_text(cleaned)
        keywords = self.extract_keywords_spacy(cleaned)
        highlighted_summary = self.highlight_keywords(summary_text, keywords, color="#0000FF")
        self.root.ids.summary_label.text = highlighted_summary

        wiki_texts = []
        for kw in keywords:
            info = self.get_wiki_summary(kw)
            if info:
                wiki_texts.append(f"[b]{kw}[/b]: {info}")
            else:
                wiki_texts.append(f"[b]{kw}[/b]: No Wikipedia entry found.")
        self.root.ids.wiki_label.text = "\n\n".join(wiki_texts)

    def clean_transcript(self, text: str) -> str:
        """Remove common filler words and extra whitespace."""
        text_no_fillers = re.sub(r"\b(um|uh|er|like)\b", "", text, flags=re.IGNORECASE)
        text_no_fillers = re.sub(r"\s+", " ", text_no_fillers).strip()
        return text_no_fillers

    def summarize_text(self, text: str, max_length=130, min_length=30) -> str:
        """Use a transformer model to create a summary of the text."""
        if not text.strip():
            return "[No text to summarize]"
        summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]["summary_text"]

    def extract_keywords_spacy(self, text: str, top_n: int = 10) -> list:
        doc = self.nlp(text)
        raw_chunks = [chunk.text.strip() for chunk in doc.noun_chunks]
        filtered = []
        for ch in raw_chunks:
            if len(ch) < 3:
                continue
            ch_doc = self.nlp(ch)
            if all(token.is_stop or token.pos_ == "PRON" for token in ch_doc):
                continue

            filtered.append(ch)
        freq = {}
        for kw in filtered:
            freq[kw] = freq.get(kw, 0) + 1

        sorted_kws = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [kw for kw, _ in sorted_kws[:top_n]]


    def highlight_keywords(self, text: str, keywords: list, color="#0000FF") -> str:
        """Wrap each keyword in [color=...] ... [/color] tags."""
        for kw in keywords:
            pattern = re.compile(r"\b({})\b".format(re.escape(kw)), re.IGNORECASE)
            text = pattern.sub(rf"[color={color}]\1[/color]", text)
        return text

    def get_wiki_summary(self, keyword: str) -> str:
        """Attempt to retrieve a 1-sentence Wikipedia summary for the given keyword."""
        try:
            summary = wikipedia.summary(keyword, sentences=1)
            return summary
        except Exception:
            return ""

if __name__ == "__main__":
    MyNoteTakerApp().run()
