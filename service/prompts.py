# service/prompts.py

from narr_mod.vogler_hero_journey import vogler_hero_journey

def get_evaluation_prompt(structure_name, formatted_structure):
    if structure_name == "hero_journey":
        return hero_journey_prompt(formatted_structure)
    elif structure_name == "three_act":
        return three_act_prompt(formatted_structure)
    elif structure_name == "four_act":
        return four_act_prompt(formatted_structure)
    elif structure_name == "vogler_hero_journey":
        return vogler_hero_journey.get_prompt()
    else:
        raise ValueError(f"Unknown structure name: {structure_name}")
    

def get_evaluation_prompt(structure_name, formatted_structure):
    if structure_name == "hero_journey":
        return hero_journey_prompt(formatted_structure)
    elif structure_name == "three_act":
        return three_act_prompt(formatted_structure)
    elif structure_name == "four_act":
        return four_act_prompt(formatted_structure)
    else:
        raise ValueError(f"Unknown structure name: {structure_name}")
    

def hero_journey_prompt(structure):
    prompt = f"""
    Analyze the following narrative structure based on the Hero's Journey:

    Ordinary World:
    {' '.join(structure['ordinary_world'])}

    Call to Adventure:
    {' '.join(structure['call_to_adventure'])}

    Refusal of the Call:
    {' '.join(structure['refusal_of_the_call'])}

    Meeting the Mentor:
    {' '.join(structure['meeting_the_mentor'])}

    Crossing the Threshold:
    {' '.join(structure['crossing_the_threshold'])}

    Evaluate how well this narrative follows the Hero's Journey structure. 
    Provide insights on the strengths and weaknesses of each stage, and suggest improvements.
    """
    return prompt


def three_act_prompt(structure):
    prompt = f"""
    Analyze the following narrative structure based on the Three-Act Structure:

    Act 1 (Setup):
    {' '.join(structure['act1_setup'])}

    Act 2 (Confrontation):
    {' '.join(structure['act2_confrontation'])}

    Act 3 (Resolution):
    {' '.join(structure['act3_resolution'])}

    Evaluate how well this narrative follows the Three-Act Structure. 
    Provide insights on the strengths and weaknesses of each act, and suggest improvements.
    """
    return prompt


def four_act_prompt(structure):
    prompt = f"""
    Analyze the following narrative structure based on the Four-Act Structure:

    Act 1 (Setup):
    {' '.join(structure['act1_setup'])}

    Act 2 (Complication):
    {' '.join(structure['act2_complication'])}

    Act 3 (Development):
    {' '.join(structure['act3_development'])}

    Act 4 (Resolution):
    {' '.join(structure['act4_resolution'])}

    Evaluate how well this narrative follows the Four-Act Structure. 
    Provide insights on the strengths and weaknesses of each act, and suggest improvements.
    Consider the following aspects for each act:

    Act 1 (Setup): How well does it introduce the main characters, setting, and initial conflict?
    Act 2 (Complication): Does it effectively escalate the conflict and introduce new challenges?
    Act 3 (Development): How does it deepen the conflict and develop character arcs?
    Act 4 (Resolution): Does it provide a satisfying conclusion and resolve the main conflicts?

    Also, analyze the pacing and balance between the acts. Are there any acts that feel too short or too long?
    Suggest how the narrative could be improved to better fit the Four-Act Structure.
    """
    return prompt
