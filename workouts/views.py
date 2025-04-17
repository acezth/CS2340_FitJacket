import os
#keep safe
#key: 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
from django.http import JsonResponse
from django.shortcuts import render
from openai import OpenAI


def index(request):
    return render(request, 'workouts/index.html')

client = OpenAI(api_key="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")

def ai_suggest(request):
    category = request.GET.get("type", "workout")
    prompt_map = {
        "workout": "Give me two short strength or cardio workouts under 150 words total.",
        "rehab": "Give me two short rehabilitation exercises under 150 words total.",
        "recovery": "Give me two short recovery tips under 150 words total."
    }

    prompt = prompt_map.get(category, prompt_map["workout"])

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a smart fitness and rehab assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.8,
        )
        return JsonResponse({"response": response.choices[0].message.content})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

