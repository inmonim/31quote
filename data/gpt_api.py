from openai import OpenAI
from datetime import datetime

from config import OPENAI_API_KEY

class GptAPI:

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def image_reqeust(self, prompt, image, temperature, model = "gpt-4o"):
        
        response = self.client.chat.completions.create(
            response_format={"type":"json_object"},
            model=model,
            temperature=temperature,
            messages=[
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": f"",
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url":  f"data:image/jpeg;base64,{image}"
                    },
                    },
                ],
                }
            ],
        )
        
        return response
    

    def text_request(self, text, prompt, temperature, model="gpt-4o"):
        """
        GPT API에 text를 보내는 가장 일반적인 방법
        
        반환 값은 다음과 같다.
        
        response_object = {
            "choices": [
                {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": "The 2020 World Series was played in Texas at Globe Life Field in Arlington.",
                    "role": "assistant"
                },
                "logprobs": null
                }
            ],
            "created": 1677664795,
            "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
            "model": "gpt-3.5-turbo-0613",
            "object": "chat.completion",
            "usage": {
                "completion_tokens": 17,
                "prompt_tokens": 57,
                "total_tokens": 74
            }
        }
        """
        
        response = self.client.chat.completions.create(
            response_format={"type" : "json_object"},
            model=model,
            temperature=temperature,
            messages=[
                # 주입받은 프롬프트를 활용하고, 시간은 서버의 시간을 사용.
                # json_object 타입의 response_format을 쓰기 위해서는 프롬프트 내에 Json이라는 문자 자체가 있어야함.
                {"role": "system", "content": ""},
                {"role": "user", "content": text}
            ]
        )
        
        return response


gpt = GptAPI()

