from narr_mod import get_narrative_structure
from service.extractor import extract_structure
from service.converter import convert_to_format

def test_four_act_analysis():
    # Симулируем текст сценария
    script_text = """
    Act 1: John lives a quiet life in a small town. One day, he discovers a mysterious artifact in his backyard.
    Act 2: As John investigates the artifact, strange events begin to occur in town. He faces skepticism from locals and threats from unknown entities.
    Act 3: John uncovers a conspiracy involving the artifact. He must navigate dangerous situations and make difficult choices as he gets closer to the truth.
    Act 4: John confronts the main antagonist, reveals the truth to the town, and decides the fate of the artifact. The town returns to normalcy, but John is forever changed.
    """

    # Извлекаем структуру
    structure = extract_structure(script_text)

    # Конвертируем в формат для четырехактной структуры
    formatted_structure = convert_to_format(structure, "four_act")

    # Получаем класс структуры и создаем экземпляр
    NarrativeStructureClass = get_narrative_structure("four_act")
    narrative_structure = NarrativeStructureClass()

    # Получаем промпт и симулируем ответ LLM
    prompt = narrative_structure.get_prompt().format(**formatted_structure)
    llm_evaluation = "This is a simulated LLM evaluation of the four-act structure."

    # Выполняем анализ
    structure_analysis = narrative_structure.analyze(formatted_structure)

    # Создаем визуализацию
    visualization = narrative_structure.visualize(structure_analysis)

    # Выводим результаты
    print(f"Structure Name: {narrative_structure.name()}")
    print(f"\nPrompt for LLM:\n{prompt}")
    print(f"\nLLM Evaluation:\n{llm_evaluation}")
    print(f"\nStructure Analysis:\n{structure_analysis}")
    print(f"\nVisualization HTML:\n{visualization}")

# Запускаем тест
if __name__ == "__main__":
    test_four_act_analysis()
