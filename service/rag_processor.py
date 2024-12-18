from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS  # Обновленный импорт
from langchain.chains import RetrievalQA
from typing import Optional, Dict, List, Any
from .multilingual_embeddings import MultilingualEmbeddings
from .extractor import extract_structure
import logging
import os

logger = logging.getLogger(__name__)

# В начале файла
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''  # Отключаем GPU
import torch
torch.set_num_threads(4)  # Ограничиваем количество потоков CPU

class NarrativeRAGProcessor:
    """
    RAG процессор для улучшенного анализа нарративных структур
    """
    def __init__(self, llm, credentials: dict = None):
        self.llm = llm
        self.embeddings = MultilingualEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=250,  # Уменьшаем с 500 до 250
            chunk_overlap=25,  # Уменьшаем с 50 до 25
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " "]
        )
        self.vector_store = None

    def process_text(self, text: str) -> Dict[str, Any]:
        """
        Обработка текста с использованием RAG и извлечением структурной информации
        
        Args:
            text: Входной текст для анализа
            
        Returns:
            Dict[str, Any]: Результаты анализа с контекстом и метаданными
        """
        try:
            # Проверка на пустой текст или только пробелы
            if not text or not text.strip():
                return {
                    "chunks": [],
                    "vector_store_status": "empty_text",
                    "document_structure": {
                        "entities": [],
                        "discourse_markers": [],
                        "word_count": 0,
                        "sentence_count": 0,
                        "metadata": {
                            "document_type": "unknown",
                            "complexity_score": 0.0,
                            "language": "unknown"
                        }
                    },
                    "document_metadata": {
                        "total_words": 0,
                        "total_sentences": 0,
                        "avg_chunk_size": 0,
                        "complexity_score": 0.0,
                        "document_type": "unknown",
                        "language": "unknown"
                    }
                }

            # Разбиваем текст на чанки
            chunks = self.text_splitter.split_text(text)
            
            # Извлекаем структурную информацию для каждого чанка
            chunks_with_metadata = []
            for i, chunk in enumerate(chunks):
                # Получаем структурную информацию для чанка
                chunk_structure = extract_structure(chunk)
                
                # Убедимся, что все необходимые поля присутствуют
                if not isinstance(chunk_structure, dict):
                    chunk_structure = {}
                
                # Установим значения по умолчанию, если они отсутствуют
                metadata = {
                    "chunk_id": i,
                    "word_count": chunk_structure.get("word_count", 0),
                    "sentence_count": chunk_structure.get("sentence_count", 0),
                    "entities": [e.get("text", "") for e in chunk_structure.get("entities", [])],
                    "key_phrases": chunk_structure.get("key_phrases", []),
                    "complexity_score": chunk_structure.get("metadata", {}).get("complexity_score", 0.0),
                    "document_type": chunk_structure.get("metadata", {}).get("document_type", "unknown"),
                    "sentiment": chunk_structure.get("metadata", {}).get("sentiment", "neutral")
                }
                
                chunks_with_metadata.append({
                    "content": chunk,
                    "metadata": metadata
                })
            
            # Создаем векторное хранилище с метаданными
            if chunks_with_metadata:
                self.vector_store = FAISS.from_texts(
                    texts=[c["content"] for c in chunks_with_metadata],
                    embedding=self.embeddings,
                    metadatas=[c["metadata"] for c in chunks_with_metadata]
                )
            try:
                # Add language detection at the start
                from langdetect import detect
                try:
                    detected_language = detect(text)
                except:
                    detected_language = "unknown"
                
                # Объединяем структурную информацию всех чанков
                full_structure = extract_structure(text, chunk_size=len(text))
                if not isinstance(full_structure, dict):
                    full_structure = {
                        "word_count": 0,
                        "sentence_count": 0,
                        "entities": [],
                        "metadata": {
                            "complexity_score": 0.0,
                            "document_type": "unknown",
                            "language": "unknown"
                        }
                    }
                else:
                    # Ensure metadata exists and has language
                    if "metadata" not in full_structure:
                        full_structure["metadata"] = {}
                    full_structure["metadata"]["language"] = detected_language

                
                # Сохраняем структуру документа для использования в других методах
                self._document_structure = full_structure
                
                return {
                    "chunks": chunks_with_metadata,
                    "vector_store_status": "created" if chunks_with_metadata else "empty",
                    "total_chunks": len(chunks),
                    "document_structure": full_structure,
                    "document_metadata": {
                        "total_words": full_structure.get("word_count", 0),
                        "total_sentences": full_structure.get("sentence_count", 0),
                        "avg_chunk_size": (sum(c["metadata"]["word_count"] for c in chunks_with_metadata) / 
                                        len(chunks_with_metadata)) if chunks_with_metadata else 0,
                        "complexity_score": full_structure.get("metadata", {}).get("complexity_score", 0.0),
                        "document_type": full_structure.get("metadata", {}).get("document_type", "unknown"),
                        "language": full_structure.get("metadata", {}).get("language", "unknown")
                    }
                }
            except Exception as e:
                logger.error(f"Error in process_text: {e}")
                raise
                
        except Exception as e:
            logger.error(f"Error in process_text: {e}")
            raise

    def analyze_structure(self, structure_type: str, prompt: str) -> Dict[str, any]:
        """
        Анализ структуры с использованием RAG и структурной информации
        
        Args:
            structure_type: Тип нарративной структуры
            prompt: Базовый промпт для анализа
            
        Returns:
            Dict[str, any]: Результаты анализа
        """
        if not self.vector_store:
            raise ValueError("No vector store available. Process text first.")

        try:
            # Создаем цепочку для анализа с улучшенными параметрами поиска
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(
                    search_kwargs={
                        "k": 4,
                        "fetch_k": 8,
                        "filter": lambda x: x.get("complexity_score", 1.0) < 0.8  # Используем get с дефолтным значением
                    }
                ),
                return_source_documents=True
            )

            # Формируем улучшенный промпт с учетом структурной информации
            enhanced_prompt = self._enhance_prompt_with_structure(prompt, structure_type)

            # Получаем ответ
            response = qa_chain({"query": enhanced_prompt})
            
            # Извлекаем информацию о использованных чанках
            used_chunks = [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "structural_elements": self._extract_chunk_elements(doc.page_content)
                } for doc in response.get("source_documents", [])
            ]
            
            return {
                "analysis": response.get("result", "No analysis available"),
                "source_chunks": used_chunks,
                "structure_type": structure_type,
                "confidence_score": self._calculate_confidence(used_chunks),
                "structural_coverage": self._calculate_structural_coverage(used_chunks)
            }
        except Exception as e:
            logger.error(f"Error in analyze_structure: {e}")
            return {
                "analysis": "Analysis failed",
                "error": str(e),
                "structure_type": structure_type,
                "confidence_score": 0.0,
                "structural_coverage": 0.0
            }

    def _enhance_prompt_with_structure(self, base_prompt: str, structure_type: str) -> str:
        """
        Улучшает промпт информацией о структуре текста
        """
        if not hasattr(self, '_document_structure'):
            return base_prompt

        metadata = self._document_structure.get('metadata', {})
        if not isinstance(metadata, dict):
            metadata = {}
                
        structure_info = f"""
        Document Analysis Context:
        - Type: {metadata.get('document_type', 'unknown')}
        - Complexity: {metadata.get('complexity_score', 0.0)}
        - Key entities: {', '.join(e.get('text', '') for e in self._document_structure.get('entities', [])[:5])}
        - Main discourse markers: {', '.join(m.get('text', '') for m in self._document_structure.get('discourse_markers', [])[:5])}
        
        Analyze the following text using {structure_type} approach, considering:
        {base_prompt}
        """
        
        return structure_info

    def _extract_chunk_elements(self, chunk_text: str) -> Dict[str, Any]:
        """
        Извлекает структурные элементы из чанка
        """
        return extract_structure(chunk_text)

    def _calculate_structural_coverage(self, used_chunks: List[Dict[str, Any]]) -> float:
        """
        Вычисляет покрытие структурных элементов текста
        """
        total_elements = sum(len(chunk["structural_elements"]["entities"]) +
                           len(chunk["structural_elements"]["key_phrases"]) 
                           for chunk in used_chunks)
        
        if not total_elements:
            return 0.0
            
        return min(total_elements / (len(used_chunks) * 10), 1.0)  # Нормализация до 1

    def _calculate_confidence(self, used_chunks: List[Dict[str, Any]]) -> float:
        """
        Вычисляет уверенность в анализе на основе использованных чанков
        
        Args:
            used_chunks: Список использованных чанков с метаданными
            
        Returns:
            float: Оценка уверенности от 0 до 1
        """
        if not used_chunks:
            return 0.0
            
        try:
            # Вычисляем среднюю оценку сложности
            avg_complexity = sum(
                chunk.get("metadata", {}).get("complexity_score", 0.0) 
                for chunk in used_chunks
            ) / len(used_chunks)
            
            # Учитываем количество найденных сущностей
            total_entities = sum(
                len(chunk.get("structural_elements", {}).get("entities", []))
                for chunk in used_chunks
            )
            
            # Нормализуем количество сущностей (предполагаем, что больше 20 - это хорошо)
            entity_score = min(total_entities / 20.0, 1.0)
            
            # Вычисляем итоговую оценку
            # Меньшая сложность даёт большую уверенность
            confidence = (1.0 - avg_complexity) * 0.6 + entity_score * 0.4
            
            return max(0.0, min(1.0, confidence))
            
        except Exception as e:
            logger.warning(f"Error calculating confidence: {e}")
            return 0.0

    def _calculate_structural_coverage(self, used_chunks: List[Dict[str, Any]]) -> float:
        """
        Вычисляет покрытие структурных элементов текста
        
        Args:
            used_chunks: Список использованных чанков
            
        Returns:
            float: Оценка покрытия от 0 до 1
        """
        if not used_chunks:
            return 0.0
            
        try:
            total_elements = 0
            for chunk in used_chunks:
                structural_elements = chunk.get("structural_elements", {})
                # Подсчитываем количество различных структурных элементов
                total_elements += len(structural_elements.get("entities", []))
                total_elements += len(structural_elements.get("key_phrases", []))
                total_elements += len(structural_elements.get("discourse_markers", []))
                
            # Нормализуем результат (предполагаем, что 30 элементов - это хорошее покрытие)
            coverage = total_elements / 30.0
            
            return max(0.0, min(1.0, coverage))
            
        except Exception as e:
            logger.warning(f"Error calculating structural coverage: {e}")
            return 0.0

    def _extract_chunk_elements(self, chunk_text: str) -> Dict[str, Any]:
        """
        Извлекает структурные элементы из чанка
        
        Args:
            chunk_text: Текст чанка
            
        Returns:
            Dict[str, Any]: Структурные элементы
        """
        try:
            return extract_structure(chunk_text)
        except Exception as e:
            logger.warning(f"Error extracting chunk elements: {e}")
            return {
                "entities": [],
                "key_phrases": [],
                "discourse_markers": [],
                "metadata": {
                    "complexity_score": 0.0,
                    "document_type": "unknown"
                }
            }