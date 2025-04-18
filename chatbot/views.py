from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
import numpy as np

# ✅ Load your dataset once
df = pd.read_csv("India Agriculture Crop Production.csv")
df["Crop"] = df["Crop"].str.lower()
df["District_Name"] = df["District_Name"].str.lower()
df["Season"] = df["Season"].str.lower()

# ✅ Create a readable text column for embeddings (optional, used for RAG later)
df["text"] = df.apply(lambda row: 
    f"In {row['District_Name']} during {row['Season']} season of {row['Crop_Year']}, "
    f"{row['Crop']} was grown over {row['Area']} hectares producing {row['Production']} tonnes "
    f"with a yield of {row['Yield']} kg/hectare.", axis=1)

# ✅ Dictionary for metric keywords
METRIC_MAP = {
    "yield": "Yield",
    "harvest": "Yield",
    "roi": "Production",
    "return": "Production",
    "area": "Area",
    "production": "Production"
}

def extract_crop_and_metric(question):
    question = question.lower()
    crop = None
    metric = None

    # Match crop
    for name in df["Crop"].unique():
        if name in question:
            crop = name
            break

    # Match metric
    for keyword in METRIC_MAP:
        if keyword in question:
            metric = METRIC_MAP[keyword]
            break

    # Match year (optional)
    year = None
    for word in question.split():
        if word.isdigit() and 1900 < int(word) < 2050:
            year = int(word)
            break

    return crop, metric, year


def chatbot_ui(request):
    return render(request, "chatbot/index.html")


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question", "")

            crop, metric = extract_crop_and_metric(question)

            if crop and metric:
                filtered = df[df["Crop"] == crop]
                if not filtered.empty:
                    avg_value = filtered[metric].mean()
                    return JsonResponse({
                        "answer": f"Average {metric.lower()} for {crop.title()} is {round(avg_value, 2)}."
                    })
                else:
                    return JsonResponse({"answer": f"No data available for {crop}."})
            else:
                return JsonResponse({
                    "answer": "Sorry, I couldn’t understand your question. Try asking about yield, ROI, or area for a crop."
                })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)