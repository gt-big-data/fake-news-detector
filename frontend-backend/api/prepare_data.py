from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences

def prepare_data(data_set, length=None):
    #tokenize the data set
    bodies_tokenizer, headlines_tokenizer = (Tokenizer(), Tokenizer())

    #find the max length of each dataset
    bodies_max_length = 0
    headlines_max_length = 0
    if not length:
      bodies_max_length = data_set['articleBody'].map(lambda x : len(x.split())).max()
      headlines_max_length = data_set['Headline'].map(lambda x : len(x.split())).max()
    else:
      bodies_max_length = length[0]
      headlines_max_length = length[1]
    
    #fit the tokenizer on the data set
    bodies_tokenizer.fit_on_texts(data_set['articleBody'])
    headlines_tokenizer.fit_on_texts(data_set['Headline'])

    #convert the texts to sequences
    bodies_sequences = bodies_tokenizer.texts_to_sequences(data_set['articleBody'])
    headlines_sequences = headlines_tokenizer.texts_to_sequences(data_set['Headline'])

    #pad the data to be the max length
    bodies_sequences = pad_sequences(bodies_sequences, maxlen=bodies_max_length, padding='post', truncating='post')
    headlines_sequences = pad_sequences(headlines_sequences, maxlen=headlines_max_length, padding='post', truncating='post')

    
    return bodies_sequences, headlines_sequences, bodies_tokenizer.word_index, headlines_tokenizer.word_index, data_set['Stance']
