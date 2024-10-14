def convert_to_format(structure, structure_name):
    if structure_name == "four_act":
        return convert_to_four_act(structure)
    else:
        raise ValueError(f"Unknown structure name: {structure_name}")

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