# test_evaluator.py

from service import initialize_llm, NarrativeEvaluator

def main():
    # Инициализация LLM
    llm = initialize_llm()
    
    # Создание экземпляра NarrativeEvaluator
    evaluator = NarrativeEvaluator(llm)
    
    # Тестовый текст (краткое содержание "Звездных войн: Новая надежда")
    test_text = """
    Luke Skywalker lives on a farm with his uncle and aunt on the planet Tatooine. He dreams of adventure and wants to leave his home. One day he meets the droids R2-D2 and C-3PO, who are carrying a secret message from Princess Leia. Luke meets Obi-Wan Kenobi, who tells him about the Force and gives him his father's lightsaber.

    Luke decides to go with Obi-Wan to rescue Princess Leia. They hire pilot Han Solo and his ship, the Millennium Falcon. Arriving at the Death Star space station, they rescue Leia, but Obi-Wan sacrifices himself in a battle with Darth Vader.

    Luke joins the Rebels and participates in the attack on the Death Star. Using the Force, he successfully destroys the station, dealing a serious blow to the Empire. Luke becomes a hero of the Rebellion and begins his journey as a Jedi.
    """
    
    print("Тестирование классификации...")
    structure_name = evaluator.classify(test_text)
    print(f"Определенная структура: {structure_name}")
    
    print("\nТестирование полного анализа...")
    result = evaluator.analyze(test_text)
    
    print(f"\nОпределенная структура: {result['structure_name']}")
    print(f"\nОценка LLM:\n{result['llm_evaluation'][:500]}...")  # Выводим первые 500 символов
    print(f"\nАнализ структуры:\n{result['structure_analysis']}")
    print(f"\nВизуализация: {result['visualization']}")
    print("\nФорматированная структура:")
    for key, value in result['formatted_structure'].items():
        print(f"{key}: {value[:100]}...")  # Выводим первые 100 символов каждого элемента

if __name__ == "__main__":
    main()
