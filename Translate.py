from openai import OpenAI
import json
import re
client = OpenAI(api_key="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")

folder = "D:\\Books\\Focus\\"
Language = "Russian"
# Language = "Ukrainian"

# Функция для разбиения текста на предложения
def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return sentences

# Функция для разбиения списка предложений на части по N предложений
def split_into_parts(sentences, n=10):
    return [sentences[i:i + n] for i in range(0, len(sentences), n)]

# Функция для имитации обработки текста (в вашем случае, перевода)
def process_text_with_api(part):
    response = client.chat.completions.create(
      model="gpt-4-0613",
      messages=[
        {
          "role": "system",
          "content": f"You will be provided with a sentence in English, and your task is to translate it into {Language}."
        },
        {
          "role": "user",
           
          "content": part[0]
        }
      ],
      top_p=1,
      temperature = 0.7
    )
    # Получаем ответ от API
    answer = response.json()
    answer = json.loads(answer)
    # Предполагается, что ответ уже в формате JSON, поэтому дополнительное преобразование в JSON не требуется
    part = answer['choices'][0]['message']['content'].strip()
    
    return ' '.join(part)  # Возвращаем текст без изменений для демонстрации

# Читаем содержимое файла
file_path = folder + "Original.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

# Разбиваем текст на предложения
sentences = split_into_sentences(file_content)

# Разбиваем на части по 10 предложений
parts = split_into_parts(sentences, 1)

# Итоговый массив для склеенных результатов
result = []

# Обрабатываем каждую часть через API
for part in parts:
    processed_part = process_text_with_api(part)
    result.append(processed_part)
    print(str(processed_part))

# Вывод результата
for index, part in enumerate(result, 1):
    print(f"Часть {index}: {part}\n")

# Функция для очистки текста
def clean_text(parts):
    cleaned_parts = []
    for part in parts:
        # Удаляем указание части и номер
        part = re.sub(r'Часть \d+: ', '', part)
        # Удаляем пробелы перед точками и запятыми
        part = re.sub(r'\s+([.,])', r'\1', part)
        # Удаляем лишние пробелы внутри слов
        part = re.sub(r'(?<=\w) (?=\w)', '', part)
        # Удаляем множественные пробелы
        part = re.sub(r'\s+', ' ', part)
        # Переносим текст начинающийся с символа • на новую строку
        part = re.sub(r' • ', '\n• ', part)
        cleaned_parts.append(part.strip())
    return cleaned_parts

# Применяем функцию к нашим частям
cleaned_parts = clean_text(result)
 
# Задаем путь к файлу, в который будет произведена запись
output_file_path = f'{folder}\\{Language}.txt'

# Записываем строки из списка в файл
with open(output_file_path, 'w', encoding='utf-8') as file:
    for part in cleaned_parts:
        file.write(part + "\n")



################################
# Читаем содержимое файла
file_path = output_file_path
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

# Разбиваем текст на предложения
sentences = split_into_sentences(file_content)

# Разбиваем на части по 10 предложений
parts = split_into_parts(sentences, 1)

# Цикл для прохождения по каждой части и преобразования её в речь
for index, part in enumerate(parts, start=0):
    response = client.audio.speech.create(
        model="tts-1",
        response_format="mp3",
        voice="nova",
        input=part[0]  # Убедитесь, что part[0] корректно обращается к нужной части текста
    )
    
    # Форматируем индекс для добавления лидирующего нуля, если индекс меньше 10
    formatted_index = f"0{index}" if index < 10 else str(index)
    
    # Задаём путь к файлу, где будет сохранена речь
    speech_file_path = f"{folder}\\part_{formatted_index}.mp3"
    
    # Записываем аудиофайл
    response.stream_to_file(speech_file_path)  # Преобразование к str не требуется, так как f-строка уже возвращает строку
    print(index)


##############################################

from pydub import AudioSegment
from pathlib import Path

# Ваш код для объединения MP3 файлов
folder_path = Path(folder)
combined = AudioSegment.empty()

for mp3_file in folder_path.glob('part*.mp3'):
    sound = AudioSegment.from_mp3(mp3_file)
    combined += sound

output_file_path = folder_path / f"{Language}.mp3"
combined.export(output_file_path, format="mp3")


# Итерируем по всем файлам в папке
for file in folder_path.glob('part*.mp3'):
    # Проверяем, содержит ли имя файла "part"
    if 'part' in file.stem:
        # Удаляем файл
        file.unlink()
        print(f"Файл {file} был удален")

# Если в папке больше нет файлов с указанным условием, выводим сообщение
print("Все файлы, удовлетворяющие условиям, были удалены.")
