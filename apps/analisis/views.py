from django.shortcuts import render
import requests
import numpy as np
from django.views import View
from sentence_transformers import SentenceTransformer



API_TOKEN = "JrQmXsqG4W3b9SJAWNuSyQtDsOTGWwubD5v53N_U"
ACCOUNT_ID = "dea18ceb8496cd48c6b923cf46ee24dc"
API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}


model = SentenceTransformer('distiluse-base-multilingual-cased')

def generar_embedding(texto):
    return model.encode(texto).tolist()



