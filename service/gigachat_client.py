import requests
import uuid
import json
from typing import Optional, Dict, Any
import logging

from shared.config import Config

logger = logging.getLogger(__name__)

class GigaChatClient:
    def __init__(self, auth_token: str):
        self.auth_token = auth_token
        self.access_token: Optional[str] = None
        
    def get_access_token(self, scope='GIGACHAT_API_PERS') -> Optional[str]:
        """Получение access token для GigaChat API"""
        rq_uid = str(uuid.uuid4())
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': rq_uid,
            'Authorization': f'Basic {self.auth_token}'
        }
        
        payload = {'scope': scope}
        
        try:
            response = requests.post(url, headers=headers, data=payload, verify=Config.GIGACHAT_VERIFY_SSL)
            response.raise_for_status()
            self.access_token = response.json()['access_token']
            return self.access_token
        except requests.RequestException as e:
            logger.error(f"Failed to get access token: {e}")
            return None
            
    def get_chat_completion(self, messages: list, 
                          temperature: float = 1.0,
                          top_p: float = 0.1,
                          n: int = 1,
                          max_tokens: int = 512) -> Optional[Dict[str, Any]]:
        """Получение ответа от модели"""
        if not self.access_token:
            self.access_token = self.get_access_token()
            if not self.access_token:
                raise ValueError("Failed to obtain access token")
        
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        
        payload = {
            "model": "GigaChat",
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stream": False,
            "max_tokens": max_tokens,
            "repetition_penalty": 1,
            "update_interval": 0
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        
        try:
            response = requests.post(
                url, 
                headers=headers, 
                data=json.dumps(payload), 
                verify=Config.GIGACHAT_VERIFY_SSL
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Chat completion request failed: {e}")
            return None
