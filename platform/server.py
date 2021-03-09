from flask import Flask
from flask import request
import usearchapi
from tensorflow import keras
import test
from decouple import config

rootPath = config('ROOT')

model = keras.models.load_model(rootPath)

app = Flask(__name__)
@app.route("/predict", methods=["GET", "POST"])

def predict():
    query = request.args.get("claim")
    articleList = usearchapi.call_usearch_news_api(query)
    
    predictions = []
    for article in articleList:
        predictions.append(test.test(query, article, model))
    predictionString = ""
    for prediction in predictions:
        predictionString += prediction + "\n"
    return predictionString

if __name__ == "__main__":
    app.run(debug=True)