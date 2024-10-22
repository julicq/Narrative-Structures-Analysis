# service/converter.py

def convert_to_format(structure: dict, structure_name: str) -> dict[str, str]:
    if structure_name == "four_act":
        return convert_to_four_act(structure)
    elif structure_name == "three_act":
        return convert_to_three_act(structure)
    elif structure_name == "hero_journey":
        return convert_to_hero_journey(structure)
    elif structure_name == "field_paradigm":
        return convert_to_field_paradigm(structure)
    elif structure_name == "harmon_story_circle":
        return convert_to_harmon_story_circle(structure)
    elif structure_name == "guilno_sequence":
        return convert_to_gulino_sequence(structure)
    elif structure_name == "soth_story_structure":
        return convert_to_soth_story_structure(structure)
    elif structure_name == "vogler_hero_journey":
        return convert_to_vogler_hero_journey(structure)
    elif structure_name == "watts_eight_point_arc":
        return convert_to_watts_eight_point_arc(structure)
    else:
        raise ValueError(f"Unknown structure name: {structure_name}")


def convert_to_hero_journey(structure: dict) -> dict[str, str]:
    if not structure or "sentences" not in structure:
        return {"error": "Invalid or empty structure"}
    return {
        "ordinary_world": ' '.join(structure["sentences"][:2]),
        "call_to_adventure": ' '.join(structure["sentences"][2:4]),
        "refusal_of_the_call": ' '.join(structure["sentences"][4:6]),
        "meeting_the_mentor": ' '.join(structure["sentences"][6:8]),
        "crossing_the_threshold": ' '.join(structure["sentences"][8:10]),
        # ... другие этапы путешествия героя
    }

def convert_to_four_act(structure: dict) -> dict[str, str]:
    if not structure or "sentences" not in structure:
        return {"error": "Invalid or empty structure"}

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
    if not structure or "sentences" not in structure:
        return {"error": "Invalid or empty structure"}
    
    total_sentences = len(structure["sentences"])
    act1 = total_sentences // 4
    act2 = total_sentences // 2
    act3 = total_sentences - act1 - act2
    
    return {
        "act1_setup": ' '.join(structure["sentences"][:act1]),
        "act2_confrontation": ' '.join(structure["sentences"][act1:act1+act2]),
        "act3_resolution": ' '.join(structure["sentences"][act1+act2:])
    }

def convert_to_field_paradigm(structure: dict) -> dict[str, str]:
    if not structure or "sentences" not in structure:
        return {"error": "Invalid or empty structure"}
    
    total_sentences = len(structure["sentences"])
    setup = total_sentences // 4
    confrontation = total_sentences // 2
    resolution = total_sentences - setup - confrontation
    
    return {
        "setup": ' '.join(structure["sentences"][:setup]),
        "confrontation": ' '.join(structure["sentences"][setup:setup+confrontation]),
        "resolution": ' '.join(structure["sentences"][setup+confrontation:])
    }

def convert_to_harmon_story_circle(structure: dict) -> dict[str, str]:
    if not structure or "sentences" not in structure:
        return {"error": "Invalid or empty structure"}
    
    total_sentences = len(structure["sentences"])
    step_size = total_sentences // 8
    
    return {
        "you": ' '.join(structure["sentences"][:step_size]),
        "need": ' '.join(structure["sentences"][step_size:2*step_size]),
        "go": ' '.join(structure["sentences"][2*step_size:3*step_size]),
        "search": ' '.join(structure["sentences"][3*step_size:4*step_size]),
        "find": ' '.join(structure["sentences"][4*step_size:5*step_size]),
        "take": ' '.join(structure["sentences"][5*step_size:6*step_size]),
        "return": ' '.join(structure["sentences"][6*step_size:7*step_size]),
        "change": ' '.join(structure["sentences"][7*step_size:])
    }

def convert_to_gulino_sequence(structure: dict) -> dict[str, str]:
    if not structure or "sentences" not in structure:
        return {"error": "Invalid or empty structure"}
    
    total_sentences = len(structure["sentences"])
    act1 = total_sentences // 4
    act2_3 = total_sentences // 2
    act4 = total_sentences - act1 - act2_3
    
    return {
        "introduction": ' '.join(structure["sentences"][:act1//6]),
        "stating_goal": ' '.join(structure["sentences"][act1//6:act1//3]),
        "presenting_mystery": ' '.join(structure["sentences"][act1//3:act1//2]),
        "heightening_curiosity": ' '.join(structure["sentences"][act1//2:2*act1//3]),
        "reaction_to_event": ' '.join(structure["sentences"][2*act1//3:5*act1//6]),
        "emergence_of_problem": ' '.join(structure["sentences"][5*act1//6:act1]),
        "first_attempt": ' '.join(structure["sentences"][act1:act1+act2_3//4]),
        "solution_probability": ' '.join(structure["sentences"][act1+act2_3//4:act1+act2_3//2]),
        "new_characters_subplots": ' '.join(structure["sentences"][act1+act2_3//2:act1+3*act2_3//4]),
        "rethinking_tension": ' '.join(structure["sentences"][act1+3*act2_3//4:act1+act2_3]),
        "raised_stakes": ' '.join(structure["sentences"][act1+act2_3:act1+act2_3+act4//4]),
        "accelerated_pace": ' '.join(structure["sentences"][act1+act2_3+act4//4:act1+act2_3+act4//2]),
        "all_is_lost": ' '.join(structure["sentences"][act1+act2_3+act4//2:act1+act2_3+3*act4//4]),
        "final_resolution": ' '.join(structure["sentences"][act1+act2_3+3*act4//4:])
    }

def convert_to_soth_story_structure(structure: dict) -> dict[str, str]:
    if not structure or "sentences" not in structure:
        return {"error": "Invalid or empty structure"}
    
    total_sentences = len(structure["sentences"])
    step_size = total_sentences // 9
    
    return {
        "hero_world_call": ' '.join(structure["sentences"][:step_size]),
        "meeting_antagonist": ' '.join(structure["sentences"][step_size:2*step_size]),
        "hero_locked_in": ' '.join(structure["sentences"][2*step_size:3*step_size]),
        "first_attempts": ' '.join(structure["sentences"][3*step_size:4*step_size]),
        "moving_forward": ' '.join(structure["sentences"][4*step_size:5*step_size]),
        "eye_opening_trial": ' '.join(structure["sentences"][5*step_size:6*step_size]),
        "new_plan": ' '.join(structure["sentences"][6*step_size:7*step_size]),
        "final_battle": ' '.join(structure["sentences"][7*step_size:8*step_size]),
        "new_equilibrium": ' '.join(structure["sentences"][8*step_size:])
    }

def convert_to_vogler_hero_journey(structure: dict) -> dict[str, str]:
    if not structure or "sentences" not in structure:
        return {"error": "Invalid or empty structure"}
    
    total_sentences = len(structure["sentences"])
    step_size = total_sentences // 12
    
    return {
        "ordinary_world": ' '.join(structure["sentences"][:step_size]),
        "call_to_adventure": ' '.join(structure["sentences"][step_size:2*step_size]),
        "refusal_of_call": ' '.join(structure["sentences"][2*step_size:3*step_size]),
        "meeting_with_mentor": ' '.join(structure["sentences"][3*step_size:4*step_size]),
        "crossing_threshold": ' '.join(structure["sentences"][4*step_size:5*step_size]),
        "tests_allies_enemies": ' '.join(structure["sentences"][5*step_size:6*step_size]),
        "approach_inmost_cave": ' '.join(structure["sentences"][6*step_size:7*step_size]),
        "ordeal": ' '.join(structure["sentences"][7*step_size:8*step_size]),
        "reward": ' '.join(structure["sentences"][8*step_size:9*step_size]),
        "road_back": ' '.join(structure["sentences"][9*step_size:10*step_size]),
        "resurrection": ' '.join(structure["sentences"][10*step_size:11*step_size]),
        "return_with_elixir": ' '.join(structure["sentences"][11*step_size:])
    }

def convert_to_watts_eight_point_arc(structure: dict) -> dict[str, str]:
    if not structure or "sentences" not in structure:
        return {"error": "Invalid or empty structure"}
    
    total_sentences = len(structure["sentences"])
    step_size = total_sentences // 8
    
    return {
        "stasis": ' '.join(structure["sentences"][:step_size]),
        "trigger": ' '.join(structure["sentences"][step_size:2*step_size]),
        "the_quest": ' '.join(structure["sentences"][2*step_size:3*step_size]),
        "surprise": ' '.join(structure["sentences"][3*step_size:4*step_size]),
        "critical_choice": ' '.join(structure["sentences"][4*step_size:5*step_size]),
        "climax": ' '.join(structure["sentences"][5*step_size:6*step_size]),
        "reversal": ' '.join(structure["sentences"][6*step_size:7*step_size]),
        "resolution": ' '.join(structure["sentences"][7*step_size:])
    }