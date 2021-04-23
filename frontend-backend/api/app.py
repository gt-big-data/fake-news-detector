from flask import Flask
from flask import request
import usearchapi
from tensorflow import keras
import test
from decouple import config

rootPath = config('ROOT')

model = keras.models.load_model(rootPath)
query = "No query yet"
prediction = "N/A"

app = Flask(__name__, static_folder='../build', static_url_path='/')
@app.route("/predict", methods=["GET", "POST"])
def predict():
    global query
    global prediction

    query = request.get_json()['text']
    articleList = usearchapi.call_usearch_news_api(query)
    
    predictions = []
    for article in articleList:
        predictions.append(test.test(query, article, model))
    return {"data" : [{"title" : articleList[i][0], "link" : articleList[i][2], "prediction" : predictions[i]} for i in range(1, len(articleList))], "receive" : query}

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(debug=True)