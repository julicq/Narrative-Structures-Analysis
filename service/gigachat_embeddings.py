from typing import List
from langchain.embeddings.base import Embeddings
from langchain_gigachat.embeddings import GigaChatEmbeddings as LangchainGigaChatEmbeddings
import logging

logger = logging.getLogger(__name__)

class GigaChatEmbeddings(Embeddings):
    """
    Класс для работы с эмбеддингами GigaChat через LangChain
    """
    
    def __init__(self, credentials: dict):
        """
        Инициализация GigaChat embeddings
        
        Args:
            credentials: Учетные данные для GigaChat (токен авторизации)
        """
        try:
            self.client = LangchainGigaChatEmbeddings(credentials=credentials)
            logger.info("GigaChat embeddings initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize GigaChat embeddings: {e}")
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
            # Используем встроенный метод для пакетной обработки
            embeddings = self.client.embed_documents(texts)
            return embeddings
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
            # Используем встроенный метод для одиночного текста
            embedding = self.client.embed_query(text)
            return embedding
        except Exception as e:
            logger.error(f"Error in embed_query: {e}")
            raise
