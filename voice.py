from TTS.api import TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

# generate speech by cloning a voice using default settings
tts.tts_to_file(text="Dużo czasu zajęło mi znalezienie swojego głosu, a teraz, gdy już go mam, nie zamierzam milczeć.",
                file_path="D:/output2.wav",
                speaker_wav="D:/Dr_John_Hall_voice.ogg",
                language="pl")

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")

# Load model directly
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

processor = AutoProcessor.from_pretrained("openai/whisper-large-v3")
model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large-v3")

#####################


from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from openai import OpenAI
import os
client = OpenAI()

# Шаг 1: Извлечение звука из видео файла
video_path = "D:\\meeting.mp4"
audio_output_path = "D:\\meetingextracted_audio.mp3"
segment_files_path = "D:\meeting"

video = VideoFileClip(video_path)
audio = video.audio
audio.write_audiofile(audio_output_path)

# Шаг 2: Нарезка аудио на части по 15 минут
audio = AudioSegment.from_file(audio_output_path)
segment_duration = 15 * 60 * 1000  # 15 минут в миллисекундах

segments = []
for i in range(0, len(audio), segment_duration):
    segment = audio[i:i + segment_duration]
    segments.append(segment)

# Шаг 3: Сохранение каждого сегмента в отдельный файл
segment_files = []
for j, segment in enumerate(segments):
    segment_file_path = f"D:\\meeting\\segment_{j + 1}.mp3"
    segment.export(segment_file_path, format="mp3")
    segment_files.append(segment_file_path)


# Шаг 4: Транскрибирование аудио сегментов и создание саммари

segment_files = [os.path.join(segment_files_path, file) for file in os.listdir(segment_files_path) if file.endswith('.mp3')]

all_transcriptions = []

for segment_file in segment_files:
    with open(segment_file, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
            language="uk"
        )
        all_transcriptions.append(transcription)

# Шаг 5: Объединение всех транскрипций и создание саммари
full_transcription = " ".join(all_transcriptions)

with open("D:\\meeting\\full_transcription.txt", "w", encoding="utf-8") as file:
    file.write(full_transcription)
    
   ########################### 
   

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def split_text_into_chunks(text, num_sentences=20):
    sentences = text.split('. ')
    chunks = ['. '.join(sentences[i:i + num_sentences]) for i in range(0, len(sentences), num_sentences)]
    return chunks

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please  summarize the following meeting transcription:\n\n{text}\n\n. Answer in ukrainian. Summary:"},
        ],

        max_tokens=4000,
        n=1,
        stop=["\n"]
    )
    summary = response.choices[0].message.content
    return summary

def save_summary_to_file(summary, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(summary)
        
def main(file_path):
    # Шаг 1: Чтение текстового файла
    full_text = read_text_file(file_path)

    # Шаг 2: Деление текста на части по 20 предложений
    chunks = split_text_into_chunks(full_text, num_sentences=20)

    # Шаг 3: Отправка каждой части в OpenAI API для создания саммари
    all_summaries = [summarize_text(chunk) for chunk in chunks]

    # Шаг 4: Объединение всех саммари
    final_summary = "\n\n".join(all_summaries)
    
    save_summary_to_file(final_summary, 'final_summary.txt')
    # Вывод итогового саммари
    print("Final Summary:")
    print(final_summary)

# Укажите путь к вашему текстовому файлу
file_path = "D:/meeting/full_transcription.txt"
main(file_path)   
   