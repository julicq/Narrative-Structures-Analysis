# tests/test_gigachat.py

import logging
from dotenv import load_dotenv
from service.llm import initialize_llm, ModelType
from langchain_core.messages import HumanMessage
import sys, os

def test_gigachat():
    # Загружаем переменные окружения
    load_dotenv()
    
    # Включаем отладочное логирование
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Создаем экземпляр GigaChat
        model = initialize_llm(ModelType.GIGACHAT)
        logger.debug("Created GigaChat instance")
        
        # Создаем тестовое сообщение
        message = HumanMessage(content="Привет! Как дела?")
        messages = [message]
        logger.debug(f"Created message: {message}")
        
        # Получаем ответ
        logger.debug("Attempting to generate response...")
        response = model.invoke(messages)
        
        # Проверяем ответ
        logger.debug(f"Received response: {response}")
        assert response.content.strip() != ""
        print(f"Response: {response.content}")
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    test_gigachat()
