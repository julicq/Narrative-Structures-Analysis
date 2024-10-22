# tests/test_converter.py

from service.converter import convert_to_format
import nltk


nltk.download('punkt_tab')

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def preprocess_text(text):
    sentences = nltk.sent_tokenize(text)
    return {"sentences": sentences}

def main():
    # Чтение файла
    story_text = read_file('test_story.txt')
    
    # Предобработка текста
    structure = preprocess_text(story_text)
    
    # Конвертация в разные форматы
    formats = ["three_act", "four_act", "hero_journey"]
    
    for format_name in formats:
        result = convert_to_format(structure, format_name)
        print(f"\n{format_name.upper()} STRUCTURE:")
        for key, value in result.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    nltk.download('punkt')  # Загрузка токенизатора для предложений
    main()
