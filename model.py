from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import json
from collections import Counter

def runmodel(filename):
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

    df = pd.read_csv(filename, index_col=None)
    df.drop(['Customer Name', 'Date', 'Ratings', 'Review Title'],axis=1, inplace=True)

    def sentiment_score(review):
        tokens = tokenizer.encode(review, return_tensors='pt')
        result = model(tokens)
        return int(torch.argmax(result.logits))+1

    df['sentiment'] = df['Reviews'].apply(lambda x: sentiment_score(x))



    # sentiment_counts = df['sentiment'].value_counts().sort_values(ascending=False)
    sentiment_counts = df['sentiment']

    sentiment_score = Counter(sentiment_counts)
    # sentiment_counts = sentiment_counts.to_dict()


    sentiment_scores = sentiment_counts.to_numpy().tolist()

    json_data = json.dumps(sentiment_score)
    print(json_data)

runmodel()