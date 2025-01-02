from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from typing import Optional, Dict, List, Any
from .multilingual_embeddings import MultilingualEmbeddings
from .extractor import extract_structure
import logging
import os

logger = logging.getLogger(__name__)

import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
import torch
torch.set_num_threads(4)
class NarrativeRAGProcessor:
    def __init__(self, llm, credentials: dict = None):
        self.llm = llm
        self.embeddings = MultilingualEmbeddings()
        # Уменьшаем размер чанков для более компактного представления
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=150,  # Уменьшаем размер чанка
            chunk_overlap=20,  # Уменьшаем перекрытие
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " "]
        )
        self.vector_store = None
        # Добавляем максимальное количество токенов для результата
        self.max_tokens = 25000
        # Максимальное количество сущностей для включения в результат
        self.max_entities = 3
        # Максимальное количество чанков в результате
        self.max_chunks = 3

    def process_text(self, text: str) -> Dict[str, Any]:
        try:
            if not text or not text.strip():
                return self._get_empty_result()
            chunks = self.text_splitter.split_text(text)
            chunks_with_metadata = []
            
            # Ограничиваем количество обрабатываемых чанков
            for i, chunk in enumerate(chunks[:self.max_chunks]):
                chunk_structure = extract_structure(chunk)
                
                if not isinstance(chunk_structure, dict):
                    chunk_structure = {}
                
                # Ограничиваем количество метаданных
                metadata = {
                    "chunk_id": i,
                    "word_count": chunk_structure.get("word_count", 0),
                    "sentence_count": chunk_structure.get("sentence_count", 0),
                    # Ограничиваем количество сущностей
                    "entities": [e.get("text", "") for e in chunk_structure.get("entities", [])[:self.max_entities]],
                    # Оставляем только самые важные метаданные
                    "complexity_score": chunk_structure.get("metadata", {}).get("complexity_score", 0.0),
                    "document_type": chunk_structure.get("metadata", {}).get("document_type", "unknown")
                }
                
                chunks_with_metadata.append({
                    "content": chunk,
                    "metadata": metadata
                })
            
            if chunks_with_metadata:
                self.vector_store = FAISS.from_texts(
                    texts=[c["content"] for c in chunks_with_metadata],
                    embedding=self.embeddings,
                    metadatas=[c["metadata"] for c in chunks_with_metadata]
                )

            try:
                from langdetect import detect
                detected_language = detect(text[:1000])  # Ограничиваем текст для определения языка
            except:
                detected_language = "unknown"
            
            # Получаем структуру только для первой части текста
            sample_text = text[:2000]  # Ограничиваем размер текста для анализа структуры
            full_structure = extract_structure(sample_text)
            
            if not isinstance(full_structure, dict):
                full_structure = self._get_default_structure()
            
            full_structure["metadata"] = {
                "language": detected_language,
                "complexity_score": full_structure.get("metadata", {}).get("complexity_score", 0.0),
                "document_type": full_structure.get("metadata", {}).get("document_type", "unknown")
            }
            
            # Ограничиваем количество сущностей в полной структуре
            if "entities" in full_structure:
                full_structure["entities"] = full_structure["entities"][:self.max_entities]

            self._document_structure = full_structure
            
            return {
                "chunks": chunks_with_metadata[:self.max_chunks],  # Ограничиваем количество чанков в результате
                "vector_store_status": "created" if chunks_with_metadata else "empty",
                "total_chunks": len(chunks),
                "document_structure": full_structure,
                "document_metadata": {
                    "total_words": full_structure.get("word_count", 0),
                    "total_sentences": full_structure.get("sentence_count", 0),
                    "avg_chunk_size": (sum(c["metadata"]["word_count"] for c in chunks_with_metadata[:self.max_chunks]) / 
                                    len(chunks_with_metadata[:self.max_chunks])) if chunks_with_metadata else 0,
                    "language": detected_language
                }
            }
        except Exception as e:
            logger.error(f"Error in process_text: {e}")
            raise

    def analyze_structure(self, structure_type: str, prompt: str) -> Dict[str, any]:
        if not self.vector_store:
            raise ValueError("No vector store available. Process text first.")
        try:
            qa_chain = create_retrieval_chain.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(
                    search_kwargs={
                        "k": 3,  # Уменьшаем количество извлекаемых документов
                        "fetch_k": 4,
                        "filter": lambda x: x.get("complexity_score", 1.0) < 0.8
                    }
                ),
                return_source_documents=True
            )

            enhanced_prompt = self._enhance_prompt_with_structure(prompt, structure_type)
            response = qa_chain({"query": enhanced_prompt})
            
            used_chunks = [
                {
                    "content": doc.page_content[:500],  # Ограничиваем размер содержимого чанка
                    "metadata": {k: v for k, v in doc.metadata.items() if k in ['chunk_id', 'complexity_score']},  # Оставляем только важные метаданные
                    "structural_elements": self._extract_minimal_elements(doc.page_content)
                } for doc in response.get("source_documents", [])[:self.max_chunks]  # Ограничиваем количество документов
            ]
            return {
                "analysis": response.get("result", "No analysis available")[:5000],  # Ограничиваем размер анализа
                "source_chunks": used_chunks,
                "structure_type": structure_type,
                "confidence_score": self._calculate_confidence(used_chunks)
            }
        except Exception as e:
            logger.error(f"Error in analyze_structure: {e}")
            return {
                "analysis": "Analysis failed",
                "error": str(e),
                "structure_type": structure_type,
                "confidence_score": 0.0
            }

    def _extract_minimal_elements(self, chunk_text: str) -> Dict[str, Any]:
        """Извлекает минимальный набор структурных элементов"""
        try:
            structure = extract_structure(chunk_text[:1000])  # Ограничиваем размер анализируемого текста
            return {
                "entities": [e.get("text") for e in structure.get("entities", [])[:self.max_entities]],
                "complexity_score": structure.get("metadata", {}).get("complexity_score", 0.0)
            }
        except Exception:
            return {"entities": [], "complexity_score": 0.0}

    def _get_empty_result(self) -> Dict[str, Any]:
        """Возвращает пустой результат с минимальным набором полей"""
        return {
            "chunks": [],
            "vector_store_status": "empty_text",
            "document_structure": self._get_default_structure(),
            "document_metadata": {
                "total_words": 0,
                "total_sentences": 0,
                "language": "unknown"
            }
        }

    def _get_default_structure(self) -> Dict[str, Any]:
        """Возвращает структуру по умолчанию с минимальным набором полей"""
        return {
            "word_count": 0,
            "sentence_count": 0,
            "entities": [],
            "metadata": {
                "complexity_score": 0.0,
                "document_type": "unknown",
                "language": "unknown"
            }
        }

    def _enhance_prompt_with_structure(self, base_prompt: str, structure_type: str) -> str:
        """Создает улучшенный промпт с минимальной структурной информацией"""
        if not hasattr(self, '_document_structure'):
            return base_prompt

        metadata = self._document_structure.get('metadata', {})
        if not isinstance(metadata, dict):
            metadata = {}
                
        structure_info = f"""
        Document Type: {metadata.get('document_type', 'unknown')}
        Complexity: {metadata.get('complexity_score', 0.0):.2f}
        Key entities: {', '.join(e.get('text', '') for e in self._document_structure.get('entities', [])[:self.max_entities])}
        
        Analysis ({structure_type}):
        {base_prompt}
        """
        
        return structure_info