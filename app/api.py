from typing import Any
from fastapi import APIRouter, File, Header, UploadFile
import httpx
import os
import openai
from app.utils import getLanguage
from app.product import Product
from app.config import HF_API_URL
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ["OPENAI_API_KEY"]

router = APIRouter()


def get_completion_and_token_count(messages,
                                   model="gpt-3.5-turbo",
                                   temperature=0,
                                   max_tokens=1000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    content = response.choices[0].message["content"]

    token_dict = {
        'prompt_tokens': response['usage']['prompt_tokens'],
        'completion_tokens': response['usage']['completion_tokens'],
        'total_tokens': response['usage']['total_tokens'],
    }

    return content, token_dict


@router.post("/generate-product-desciption")
def generate_product_desciption(product: Product,
                                X_Language: str = Header("en")):
    language = getLanguage(X_Language)

    messages = [
        {'role': 'system',
         'content': f"""You are a professional product description writer
            in {language}."""},
        {'role': 'user',
         'content': f"""Write a creative product description for a {product.title}"""},
    ]
    response, token_dict = get_completion_and_token_count(messages)
    print(token_dict)

    return response


@router.get("/health")
def health():
    return


@router.post("/generate_image_caption")
async def generate_image_caption(file: UploadFile = File(...)) -> Any:
    contents = await file.read()
    async with httpx.AsyncClient() as client:
        HF_TOKEN = os.environ["HF_TOKEN"]
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}"}
        response = await client.post(HF_API_URL, headers=headers, data=contents)
        response.raise_for_status()
    return response.json()
