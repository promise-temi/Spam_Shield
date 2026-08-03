import os
import sys
import logging
from mistralai.client import Mistral
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from ML_Flow import ML_Flow_Operations
from Database import Postgres_DB
from pathlib import Path
from Helpers_Monitoring import Helpers_Monitoring
monitor = Helpers_Monitoring() 

import time
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Charger le prompt système une fois (au démarrage de l'app, pas à chaque appel)
SYSTEM_PROMPT = Path(f"{os.path.dirname(__file__)}/data/spamshield-advisor-system-prompt.md").read_text(encoding="utf-8")

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))  # idéalement via une variable d'environnement


class LLMModel:
    def __init__(self):
        self.initial_system_prompt = SYSTEM_PROMPT
        self.ml_flow = ML_Flow_Operations()

    def get_system_data(self):
        return Postgres_DB().get_dashboard_metrics()

    def get_model_metrics(self):
        return self.ml_flow.get_latest_model_metrics()

    @monitor.calculate_func_time
    def generate_report_mistral(self) -> dict:
        payload = {
            "system_data": self.get_system_data(),
            "model_metrics": self.get_model_metrics()
        }

        start = time.time()
        try:
            response = client.chat.complete(
                model="mistral-small-2603",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}
                ],
                temperature=0.3,
            )
            self.ml_flow.log_llm_call(
                provider="mistral",
                model="mistral-small-2603",
                tokens_in=response.usage.prompt_tokens,
                tokens_out=response.usage.completion_tokens,
                duration=time.time() - start,
                success=True,
                llm_response=response.choices[0].message.content,   # ← ajouté
                payload=payload,                                       # ← ajouté
            )
            return {
                "model_used": "mistral-small-2603",
                "llm_response": response.choices[0].message.content,
                "base_metrics": payload
            }
        except Exception as e:
            self.ml_flow.log_llm_call(
                provider="mistral", model="mistral-small-2603",
                tokens_in=0, tokens_out=0, duration=time.time() - start,
                success=False, error=e,
            )
            raise



















# from typing import Any

# from google import genai
# from google.genai import types


# GEMINI_MODEL = "gemini-3.5-flash-lite"

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# if not gemini_api_key:
#     raise RuntimeError(
#         "La variable d'environnement GEMINI_API_KEY est absente."
#     )

# gemini_client = genai.Client(api_key=gemini_api_key)

# class LLMModel:
#     def __init__(self):
#         self.initial_system_prompt = SYSTEM_PROMPT

#     def get_system_data(self):
#         data = Postgres_DB().get_dashboard_metrics()
#         return data
    
#     def get_model_metrics(self):
#         data = ML_Flow_Operations().get_latest_model_metrics()
#         return data

#     @monitor.calculate_func_time  
#     def generate_report_mistral(self) -> str:
#         payload = {
#             "system_data": self.get_system_data(),
#             "model_metrics": self.get_model_metrics()
#         }

#         response = client.chat.complete(
#             model="mistral-small-2603",
#             messages=[
#                 {"role": "system", "content": SYSTEM_PROMPT},
#                 {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}
#             ],
#             temperature=0.3,  # basse température : tu veux un rapport stable et reproductible, pas créatif
#         )
#         results = {
#             "model_used": "mistral-small-2603",
#             "llm_response": response.choices[0].message.content,
#             "base_metrics": payload
#         }
#         return results


    # @monitor.calculate_func_time
    # def generate_report_gemini(self) -> dict[str, Any]:
    #     payload = {
    #         "system_data": self.get_system_data(),
    #         "model_metrics": self.get_model_metrics(),
    #     }

    #     try:
    #         response = gemini_client.models.generate_content(
    #             model=GEMINI_MODEL,
    #             contents=json.dumps(
    #                 payload,
    #                 ensure_ascii=False,
    #                 default=str,
    #             ),
    #             config=types.GenerateContentConfig(
    #                 system_instruction=self.initial_system_prompt,
    #                 max_output_tokens=700,
    #             ),
    #         )

    #     except Exception:
    #         logging.exception(
    #             "Échec de la génération du rapport avec Gemini."
    #         )
    #         raise

    #     report_text = response.text

    #     if not report_text:
    #         raise RuntimeError(
    #             "Gemini n'a retourné aucun contenu exploitable."
    #         )

    #     return {
    #         "provider": "Google Gemini",
    #         "model_used": GEMINI_MODEL,
    #         "parameters": {
    #             "max_output_tokens": 700,
    #         },
    #         "llm_response": report_text,
    #         "base_metrics": payload,
    #     }

    # def llm_report(self):
    #     report_data = {
    #         "system_data": self.get_system_data(),
    #         "model_metrics": self.get_model_metrics()
    #     }
    #     return report_data

    
