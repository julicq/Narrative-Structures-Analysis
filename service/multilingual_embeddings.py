from typing import List
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

class MultilingualEmbeddings(Embeddings):
    """
    Класс для работы с многоязычными эмбеддингами через SentenceTransformers
    """
    
    def __init__(self, model_name: str = 'paraphrase-multilingual-mpnet-base-v2'):
        """
        Инициализация многоязычной модели эмбеддингов
        
        Args:
            model_name: Название модели SentenceTransformers
        """
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Multilingual embeddings initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize multilingual embeddings: {e}")
            raise

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Получение эмбеддингов для списка текстов
        
        Args:
            texts: Список текстов для эмбеддинга
            
        Returns:
            List[List[float]]: Список векторов эмбеддингов
        """
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error in embed_documents: {e}")
            raise

    def embed_query(self, text: str) -> List[float]:
        """
        Получение эмбеддинга для одного текста запроса
        
        Args:
            text: Текст для эмбеддинга
            
        Returns:
            List[float]: Вектор эмбеддинга
        """
        try:
            embedding = self.model.encode([text], convert_to_tensor=False)[0]
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error in embed_query: {e}")
            raise