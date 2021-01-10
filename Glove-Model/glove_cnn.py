from typing import final
import pandas as pandas
import numpy as numpy

from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras import Sequential, Model
from keras.layers import Conv1D, Dropout, Dense, Embedding, MaxPooling1D, Concatenate, Flatten, Input
from keras.layers.merge import concatenate


# load the data set from the train csv files
def load_train_data():     
    #create Pandas dataframes from the two csv files
    train_bodies = pandas.read_csv("./dataset/train_stances.csv", encoding='utf-8')
    train_headlines = pandas.read_csv("./dataset/train_stances.csv", encoding='utf-8')

    #merge the csv files on Body ID
    train_data_set = pandas.merge(train_bodies, train_headlines, how='left', on='Body ID')
    #print(train_data_set)
    return train_data_set

def prepare_data(data_set):
    #tokenize the data set
    bodies_tokenizer, headlines_tokenizer = (Tokenizer(), Tokenizer())

    #find the max length of each dataset
    bodies_max_length = data_set['articleBody'].map(lambda x : len(x.split())).max()
    headlines_max_length = data_set['Headline'].map(lambda x : len(x.split())).max()
    
    #fit the tokenizer on the data set
    bodies_tokenizer.fit_on_texts(data_set['articleBody'])
    headlines_tokenizer.fit_on_texts(data_set['Headline'])

    #convert the texts to sequences
    bodies_sequences = bodies_tokenizer.texts_to_sequences(data_set['articleBody'])
    headlines_sequences = headlines_tokenizer.texts_to_sequences(data_set['Headline'])

    #pad the data to be the max length
    bodies_sequences = pad_sequences(bodies_sequences, maxlen=bodies_max_length, padding='post', truncating='post')
    headlines_sequences = pad_sequences(headlines_sequences, maxlen=headlines_max_length, padding='post', truncating='post')

    return bodies_sequences, headlines_sequences, bodies_tokenizer.word_index, headlines_tokenizer.word_index

def create_embeddings(bodies_word_index, headlines_word_index):
    # create empty dictionaries for the embeddings
    bodies_embeddings_index, headlines_embeddings_index = ({},{})

    # open the glove txt file
    # save the vectors into memory from the glove embeddings
    with open ('./glove.6B.100d.txt') as f:
        for line in f:
            values = line.split()
            word = values[0]
            bodies_embeddings_index[word] = numpy.asarray(values[1:], dtype='float32')
            headlines_embeddings_index[word] = numpy.asarray(values[1:], dtype='float32')
    
    #save the wector for each word to the matrix
    bodies_embeddings_matrix = numpy.zeros((len(bodies_word_index)+1, 100))
    for word, i in bodies_word_index.items():
        embedding_vector = bodies_embeddings_index.get(word)
        if embedding_vector is not None:
            bodies_embeddings_matrix[i] = embedding_vector

    headlines_embeddings_matrix = numpy.zeros((len(headlines_word_index)+1, 100))
    for word, i in headlines_word_index.items():
        embedding_vector = headlines_embeddings_index.get(word)
        if embedding_vector is not None:
            headlines_embeddings_matrix[i] = embedding_vector

    return bodies_embeddings_matrix, headlines_embeddings_matrix

def create_model(embedding_matrix, vocab_size, input_length):
    model = Sequential()
   # model.add(Input())
    model.add(Embedding(vocab_size + 1, 100, weights = [embedding_matrix], trainable=False, input_length=input_length))

    model.add(Conv1D(256, 5, activation='relu'))
    model.add(Dropout(0.5))
    model.add(MaxPooling1D(pool_size=6))

    model.add(Conv1D(256, 5, activation='relu'))
    model.add(Dropout(0.5))
    model.add(MaxPooling1D(pool_size=6))

    model.add(Conv1D(512, 5, activation='relu'))
    model.add(Dropout(0.5))
    model.add(MaxPooling1D(pool_size=6))

    model.add(Conv1D(512, 5, activation='relu'))
    model.add(Dropout(0.5))
    model.add(MaxPooling1D(pool_size=6))

    model.add(Conv1D(768, 5, activation='relu'))
    model.add(Dropout(0.5))
    model.add(MaxPooling1D(pool_size=6))

    return model

if __name__ == '__main__':
    bodies_sequences, headlines_sequences, bodies_word_index, headlines_word_index = prepare_data(load_train_data())
    bodies_embeddings_matrix, headlines_embeddings_matrix = create_embeddings(bodies_word_index=bodies_word_index, headlines_word_index=headlines_word_index)

    bodies_vocab_size, headlines_vocab_size = len(bodies_word_index), len(headlines_word_index)

    bodies_model = create_model(embedding_matrix=bodies_embeddings_matrix, vocab_size=bodies_vocab_size, input_length=100)
    headlines_model = create_model(embedding_matrix=headlines_embeddings_matrix, vocab_size=headlines_vocab_size, input_length=20)

    print(bodies_vocab_size)
    print(headlines_vocab_size)

    #bodies_model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    #print(bodies_model.summary())

    #headlines_model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    #print(headlines_model.summary())
    finalModel = Sequential()
    finalModel = Concatenate()([bodies_model.output, headlines_model.output])
    finalModel = Flatten()(finalModel)
    finalModel = Dense(1024, activation='relu') (finalModel)
    finalModel = Dense(1024, activation='relu') (finalModel)
    finalModel = Dense(1024, activation='relu') (finalModel)
    finalModel = Dense(4, activation='softmax') (finalModel)

    model = Model(inputs=[bodies_model.input, headlines_model.input], outputs = finalModel)


    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    print(model.summary())

    
