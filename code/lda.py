import nltk
from nltk.corpus import stopwords
from gensim import corpora, models
import gensim
import json

import pandas as pd
import re

import WriteData


def clean_html(text):
    return re.sub(r'<[^>]*>', '', text)




def get_documents():

    documents = []

    documents_json = []

    with open(r'/checked_tag_files/github/github_sort.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:
        obj = json.loads(line.rstrip())

        # body = clean_html(obj["body"])
        # obj["body"] = body

        title = obj["title"]

        tags = obj['tags']

        tag_array = tags.split('|')

        tag_flag = False
        for tag in tag_array:
            if tag == 'github':
                continue
            
            if tag == 'github-actions':
                tag_flag = True
                break
        
        if tag_flag is True:

            documents.append(title)

            documents_json.append(obj)

    return documents, documents_json


# documents, documents_json = get_documents()
# print(len(documents))


def lda():

    print('first step: get the documents....................')

    documents, documents_json = get_documents()

    print(f'documents number: {len(documents)}..............')

    print('second step: begin topic modeling................')


    stop_words = set(stopwords.words('english'))

    # special_words = ['arangodb', '-', 'arangodb?', '1', '/', 'arangodb:', 'arango']
    special_words = ['docker', '-', 'docker?', '1', 'docker:']

    # texts = [
    #     [word for word in document.lower().split() if word not in stop_words and re.match(r'^[a-z]', word) and word not in special_words]
    #     for document in documents
    # ]

    texts = [
        [word for word in document.lower().split() if word not in stop_words and re.match(r'^[a-z]', word)]
        for document in documents
    ]

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    lda_model = gensim.models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=30)

    print('third step: print the topics...................')

    topics = lda_model.print_topics(num_words=10)
    for topic in topics:
        print(topic)
    
    number_obj = {}

    print('fourth step: number of counts..................')

    for doc in documents_json:

        # new_document = clean_html(doc["body"])
        new_document = doc["title"]

        new_bow = dictionary.doc2bow(new_document.lower().split())

        new_topic_distribution = lda_model.get_document_topics(new_bow)

        max_index = max(new_topic_distribution, key=lambda x: x[1])[0]

        # WriteData.write_in_path(json.dumps(doc), f"/checked_tag_files/mysql_class_{max_index}")

        if max_index not in number_obj.keys():
            number_obj[max_index] = 1
        else:
            number_obj[max_index] += 1

        # print(max_index)

    print(number_obj)

lda()
