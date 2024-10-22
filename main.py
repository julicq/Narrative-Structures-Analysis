# main.py

import argparse
import os
from service.evaluator import evaluate_narrative
from service.llm import initialize_llm

def load_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    parser = argparse.ArgumentParser(description="Analyze narrative structure of a text file.")
    parser.add_argument("file_path", help="Path to the text file to analyze")
    parser.add_argument("structure_type", choices=["hero_journey", "three_act", "four_act"], 
                        help="Type of narrative structure to analyze")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file_path):
        print(f"Error: File '{args.file_path}' does not exist.")
        return

    text = load_text_from_file(args.file_path)
    llm = initialize_llm()
    
    print(f"Analyzing file: {args.file_path}")
    print(f"Using structure type: {args.structure_type}")
    print("Please wait, this may take a few moments...")

    result = evaluate_narrative(text, args.structure_type, llm)
    
    print("\nEvaluation Result:")
    print(result["evaluation"])
    
    print("\nFormatted Structure:")
    for key, value in result["formatted_structure"].items():
        print(f"\n{key.capitalize()}:")
        print(' '.join(value))

if __name__ == "__main__":
    main()
