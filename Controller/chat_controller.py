from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
import openai
from Service import product_service
import json

router = APIRouter(prefix="/chat", tags=["chat"])


user_prompt_count = {}


@router.post("/ask")
async def chat_assistant(chat_data: dict):
    user_id = chat_data.get("user_id")
    question = chat_data.get("question")

    if not user_id or not question:
        raise HTTPException(status_code=400, detail="user_id and question are required")

    # בדיקת כמול השאלות
    if user_id in user_prompt_count:
        if user_prompt_count[user_id] >= 5:
            raise HTTPException(status_code=429, detail="You have reached the maximum limit of 5 questions per session")
        user_prompt_count[user_id] += 1
    else:
        user_prompt_count[user_id] = 1

    try:
        # קבלת מוצרים זמינים
        products = await product_service.get_all_products()

        # הכנת context על המוצרים
        products_context = "Available products in our store:\n"
        for product in products:
            stock_status = "In Stock" if product["Stock"] > 0 else "Out of Stock"
            products_context += f"- {product['Name']}: ${product['Price']} ({stock_status} - {product['Stock']} units)\n"

        # הפרומפט לChatGPT
        system_prompt = f"""You are a helpful shopping assistant for our online store. 
        You can only answer questions about the products available in our store.
        Here are the products we currently have:

        {products_context}

        Please answer questions about these products only. If asked about products not in our inventory, 
        politely explain that we don't carry that item and suggest similar alternatives if available."""

        openai.api_key = "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"

        response = f"I can help you with questions about our {len(products)} available products. " \
                   f"Your question: '{question}' - This is a demo response. " \
                   f"You have {5 - user_prompt_count[user_id]} questions remaining in this session."

        return {
            "response": response,
            "remaining_prompts": 5 - user_prompt_count[user_id],
            "products_count": len(products)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat service error: {str(e)}")


@router.post("/reset-session/{user_id}")
async def reset_chat_session(user_id: int):
    if user_id in user_prompt_count:
        del user_prompt_count[user_id]
    return {"message": "Chat session reset successfully"}
