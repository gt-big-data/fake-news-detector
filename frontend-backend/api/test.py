import pandas as pd
import numpy as np
import prepare_data

def test(headline, body, model):
    data = {'Headline': [headline], 'articleBody':[body], 'Stance': [None]}
    df = pd.DataFrame.from_dict(data)
    bodies_sequences, headlines_sequences, bodies_word_index, headlines_word_index, stances = prepare_data.prepare_data(df, [4788,40])
    stances = {
        0: "agree",
        1: "disagree",
        2: "discuss",
        3: "unrelated"
    }
    prediction = model.predict([bodies_sequences, headlines_sequences])
    print(stances[np.argmax(prediction)])
    return stances[np.argmax(prediction)]