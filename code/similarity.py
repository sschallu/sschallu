from sentence_transformers import SentenceTransformer, util
from Levenshtein import distance
from itertools import combinations
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine

import WriteData

import json

# model = SentenceTransformer('all-MiniLM-L6-v2')

def find_semantically_similar_combination(word, sentence):
    # words = sentence.split()
    # word_embedding = model.encode(word)

    sentence_words = sentence.split()

    possible_combinations = ["".join(comb) for n in range(2, 4) for comb in combinations(sentence_words, n)]

    word_vector = model.encode(word, convert_to_tensor=True)
    best_match = None
    best_score = -np.inf

    for candidate in possible_combinations:
        candidate_vector = model.encode(candidate, convert_to_tensor=True)
        
        similarity = util.cos_sim(word_vector, candidate_vector).item()
        
        edit_dist = -distance(word, candidate)
        
        score = similarity + (edit_dist / len(word))
        
        if score > best_score:
            best_score = score
            best_match = candidate

    print(f"Best match: {best_match}, Score: {best_score}")

    return best_match, best_score

sentence = "how to generate a list instead of an array in ruby with xsd.exe"
target_word = "xsd2rb"

model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_similarity_bert(sentence, target_word):
    word_array = sentence.split(' ')

    vec1 = model.encode(target_word)

    best_score = 0
    best_word = ""

    for word in word_array:
        vec2 = model.encode(word)
        similarity = 1 - cosine(vec1, vec2)

        if similarity > best_score:
            best_score = similarity
            best_word = word

    return best_word, best_score

# best_word, best_score = calculate_similarity_bert(sentence, target_word)
# print(f'best_word: {best_word}, best_score: {best_score}')




# best_match, best_score = find_semantically_similar_combination(word, sentence)
# print(f"Closest semantic combination: {best_match}, Best score: {best_score}")

def read_files(folder, question_num, file_name):
    with open(f'{folder}/{question_num}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    return all_lines


def get_packages(folder, question, filename):
    all_lines = read_files(folder, question, filename)

    total = 0
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        total += 1

        title = json_obj["title"]

        custom_id = json_obj["custom_id"]

        # if total <= 5725:
        #     continue

        # print(title)

        packages = json_obj["packages"]

        json_obj["best_word"] = []
        json_obj["best_score"] = []

        json_obj["new_packages"] = []

        for package in packages:
            package_name = package[1]
            status_code = package[2]

            if status_code == 200:
                continue

            if len(package_name) == 0:
                continue
            
            json_obj["new_packages"].append(package)

            best_match, best_score = calculate_similarity_bert(title, package_name)
            print(f"{package_name}, Closest semantic word: {best_match}, Best score: {best_score}")
            json_obj["best_word"].append(best_match)
            json_obj["best_score"].append(best_score)
        
        if len(json_obj["best_word"]) > 0:
            json_obj["packages"] = []
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question}/package_notfound_similarity')


# folder = '/llm/gpt-4o-mini'
# folder = '/llm/gpt-3.5-turbo'
# folder = '/llm/llama-3.1-instruct'
folder = '/llm/llama-128k-sonar'
question_num = 'question1'
filename = 'package_notfound_title'

get_packages(folder, question_num, filename)

