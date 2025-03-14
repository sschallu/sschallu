import WriteData

import json

import os

import requests

import time


perplexity_api = ''


target_batch_folder = 'top_build_trans_4o-mini'  




write_file_name = f'{target_batch_folder}_output'

# folder = f'/batches/llama-3.1-8b-instruct/{target_batch_folder}'

# folder = f'/batches/llama-3.1-sonar-small-128k-chat/{target_batch_folder}'

folder = f'/build/llama-3.1-8b-instruct'

# folder = f'/build/llama-3.1-sonar-small-128k-chat'

# model = 'llama-3.1-sonar-small-128k-chat'       

model = 'llama-3.1-8b-instruct'      


def request_api(custom_id, content):

    url = 'https://api.perplexity.ai/chat/completions'

    try:

        payload = {
            # "model": "llama-3.1-8b-instruct",
            "model": f"{model}",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant skilled in generating, explaining, and optimizing code across multiple programming languages."
                },
                {
                    "role": "user",
                    "content": f"{content}"
                }
            ],
            "max_tokens": 10000,
            "temperature": 0.2,
            "top_p": 0.9,
            "return_citations": False,
            "search_domain_filter": ["perplexity.ai"],
            "return_images": False,
            "return_related_questions": False,
            "search_recency_filter": "month",
            "top_k": 0,
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 1
        }
        headers = {
            "Authorization": f"Bearer {perplexity_api}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        response_obj = json.loads(response.text)

        response_obj['custom_id'] = custom_id

        id = response_obj['id']

        WriteData.write_in_path(json.dumps(response_obj), f'{folder}/{write_file_name}')

        print(f'{model}, {custom_id}, {id}, done...')

    except:
        response_obj = {}
        response_obj['custom_id'] = custom_id
        response_obj['outputs'] = 'exception'
        WriteData.write_in_path(json.dumps(response_obj), f'{folder}/{write_file_name}')

        print(f'{model}, {custom_id}, exception...')
    


def read_file(folder, file_name):

    print(f'{folder}/{file_name}.jsonl')

    with open(f'{folder}/{file_name}.jsonl', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    total = 0
    for line in all_lines:

        total += 1

        if total <= 17735:
            continue
        

        json_obj = json.loads(line.rstrip())

        user_message = json_obj['body']['messages'][1]

        custom_id = json_obj['custom_id']

        content = user_message['content']

        print(f'{model}, {total}, {custom_id}...')

        request_api(custom_id, content)

        time.sleep(1)


read_file(folder, target_batch_folder)

