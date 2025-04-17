from django.shortcuts import render

#OpenAI API Key: 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
# Create your views here.
from django.http import JsonResponse
import openai
import os

openai.api_key = os.getenv("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")  # or hardcoded for testing

def get_workout(request):
    user_input = request.GET.get("q", "Give me a workout plan")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a smart workout coach."},
            {"role": "user", "content": user_input}
        ]
    )

    return JsonResponse({"response": response["choices"][0]["message"]["content"]})

