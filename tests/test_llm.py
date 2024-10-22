# tests/test_llm.py

from service.llm import initialize_llm

def test_llm():
    llm = initialize_llm()
    
    prompt = "Напиши короткое стихотворение о программировании на Python."
    
    print("Отправка запроса к модели...")
    response = llm(prompt)
    
    print("\nОтвет модели:")
    print(response)

if __name__ == "__main__":
    test_llm()
