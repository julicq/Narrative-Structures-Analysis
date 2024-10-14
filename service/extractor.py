import spacy

nlp = spacy.load("en_core_web_sm")

def extract_structure(text):
    doc = nlp(text)
    
    # Простой пример извлечения структуры
    sentences = [sent.text for sent in doc.sents]
    entities = [ent.text for ent in doc.ents]
    
    structure = {
        "sentences": sentences,
        "entities": entities,
        "word_count": len(doc),
        "sentence_count": len(sentences)
    }
    
    return structure
