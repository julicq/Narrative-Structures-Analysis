# service/converter.py

def convert_to_format(structure, structure_name):
    if structure_name == "four_act":
        return convert_to_four_act(structure)
    elif structure_name == "three_act":
        return convert_to_three_act(structure)
    elif structure_name == "hero_journey":
        return convert_to_hero_journey(structure)
    else:
        raise ValueError(f"Unknown structure name: {structure_name}")


def convert_to_hero_journey(structure):
    # Пример конвертации в структуру "Путешествие героя"
    # Это упрощенная версия, которую нужно будет доработать
    return {
        "ordinary_world": structure["sentences"][:2],
        "call_to_adventure": structure["sentences"][2:4],
        "refusal_of_the_call": structure["sentences"][4:6],
        "meeting_the_mentor": structure["sentences"][6:8],
        "crossing_the_threshold": structure["sentences"][8:10],
        # ... другие этапы путешествия героя
    }

def convert_to_four_act(structure):
    total_sentences = len(structure["sentences"])
    act1 = total_sentences // 4
    act2 = total_sentences // 4
    act3 = total_sentences // 4
    act4 = total_sentences - act1 - act2 - act3
    
    return {
        "act1_setup": structure["sentences"][:act1],
        "act2_complication": structure["sentences"][act1:act1+act2],
        "act3_development": structure["sentences"][act1+act2:act1+act2+act3],
        "act4_resolution": structure["sentences"][act1+act2+act3:]
    }

def convert_to_three_act(structure):
    total_sentences = len(structure["sentences"])
    act1 = total_sentences // 4
    act2 = total_sentences // 2
    act3 = total_sentences - act1 - act2
    
    return {
        "act1_setup": structure["sentences"][:act1],
        "act2_confrontation": structure["sentences"][act1:act1+act2],
        "act3_resolution": structure["sentences"][act1+act2:]
    }