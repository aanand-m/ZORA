# in the code below chartData stores the value 

from flask import Flask, render_template, request, jsonify, session
from display import get_data  # Import your script
from spider import main 

import os

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

import pandas as pd
import json
from collections import Counter

app = Flask(__name__)
app.secret_key = 'SESSION-KEY'
# options = get_data()

@app.route('/')
def home():
  return render_template ('index.html')

# get details from SPIDER-INFO-FORM and upload in s3 data bucket.
@app.route('/runSpider', methods=['POST'])
def runSpider():
  spider = request.form.get("spider-type")
  productLink = request.form.get("link")
  fileName = request.form.get("file-name")
  pages = request.form.get("pages")
  
  print(spider)
  print(productLink)

  main(productLink, pages, fileName)
  message = fileName
  options = get_data()
  return render_template('select.html', message=message, options=options)


# APP ROUTE FOR SELECTING DATASET 
@app.route('/selectDataset', methods=['POST'])
def selectDataset():
  dataset = request.form.get("selected-option")
  session['selected_dataset'] = dataset
  return render_template('results.html', datasetInfo=dataset)


# PERFORMING ANALYSIS
@app.route('/data')
def getData():
  dataset = session.get('selected_dataset')
  tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
  model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

  df = pd.read_csv(os.getcwd() +f"/datasets/{dataset}", index_col=None)
  df.drop(['Customer Name', 'Date', 'Ratings', 'Review Title'],axis=1, inplace=True)

  def sentiment_score(review):
      review = str(review)
      tokens = tokenizer.encode(review, return_tensors='pt')
      result = model(tokens)
      return int(torch.argmax(result.logits))+1

  df['sentiment'] = df['Reviews'].apply(lambda x: sentiment_score(x))

  sentiment_counts = df['sentiment']

  sentiment_score = Counter(sentiment_counts)

  json_data = json.dumps(sentiment_score)
  print(json_data)
  return(json_data)

if __name__ == "__main__":
    app.run(debug=True)

