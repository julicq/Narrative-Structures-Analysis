# service/converter.py

def convert_to_format(structure: dict, structure_name: str) -> dict[str, str]:
    if structure_name == "four_act":
        return convert_to_four_act(structure)
    elif structure_name == "three_act":
        return convert_to_three_act(structure)
    elif structure_name == "hero_journey":
        return convert_to_hero_journey(structure)
    else:
        raise ValueError(f"Unknown structure name: {structure_name}")


def convert_to_hero_journey(structure: dict) -> dict[str, str]:
    return {
        "ordinary_world": ' '.join(structure["sentences"][:2]),
        "call_to_adventure": ' '.join(structure["sentences"][2:4]),
        "refusal_of_the_call": ' '.join(structure["sentences"][4:6]),
        "meeting_the_mentor": ' '.join(structure["sentences"][6:8]),
        "crossing_the_threshold": ' '.join(structure["sentences"][8:10]),
        # ... другие этапы путешествия героя
    }

def convert_to_four_act(structure: dict) -> dict[str, str]:
    total_sentences = len(structure["sentences"])
    act1 = total_sentences // 4
    act2 = total_sentences // 4
    act3 = total_sentences // 4
    act4 = total_sentences - act1 - act2 - act3
    
    return {
        "act1_setup": ' '.join(structure["sentences"][:act1]),
        "act2_complication": ' '.join(structure["sentences"][act1:act1+act2]),
        "act3_development": ' '.join(structure["sentences"][act1+act2:act1+act2+act3]),
        "act4_resolution": ' '.join(structure["sentences"][act1+act2+act3:])
    }

def convert_to_three_act(structure: dict) -> dict[str, str]:
    total_sentences = len(structure["sentences"])
    act1 = total_sentences // 4
    act2 = total_sentences // 2
    act3 = total_sentences - act1 - act2
    
    return {
        "act1_setup": ' '.join(structure["sentences"][:act1]),
        "act2_confrontation": ' '.join(structure["sentences"][act1:act1+act2]),
        "act3_resolution": ' '.join(structure["sentences"][act1+act2:])
    }
