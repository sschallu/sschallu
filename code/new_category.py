import WriteData

import json

import requests

from markdown import markdown

from bs4 import BeautifulSoup

import re

import requests

import time

batch_folder_template = 'batches_prompts_'
question_folder_template = 'question'
parent_foler = r'\batches'


def read_files(destination, suffix):

    with open(f'{destination}.{suffix}', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    return all_lines





def data_aggregation_gpt(subfolder):

    gpt_folder = f'{parent_foler}/{subfolder}'

    for index in range(0, 15):
       batch_folder = f'{batch_folder_template}{index}'
       target_folder = f'{gpt_folder}/{batch_folder}'

       for question_index in range(1, 8):
           
           question_folder = f'{question_folder_template}{question_index}'

           destination = f'{target_folder}/{question_folder}/{question_folder}'

           all_lines = read_files(destination, 'json')

           write_folder = f'{gpt_folder}/data_total/{question_folder}/{question_folder}'
           print(write_folder)

           for line in all_lines:
               WriteData.write_in_path(line.rstrip(), f'{write_folder}')


def arrange_customid_title_llama(all_lines):
    dic = {}

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        content = json_obj['body']['messages'][1]['content']

        if custom_id not in dic.keys():
            dic[custom_id] = content

    return dic


def write_customid_llama(obj, write_folder):
    
    custom_id = obj['custom_id']

    target_folder = f'{write_folder}/data_total'

    if custom_id.endswith("_1"):
        WriteData.write_in_path(json.dumps(obj), f'{target_folder}/question1/question1')

    elif custom_id.endswith("_2"):
        WriteData.write_in_path(json.dumps(obj), f'{target_folder}/question2/question2')
        
    elif custom_id.endswith("_3"):
        WriteData.write_in_path(json.dumps(obj), f'{target_folder}/question3/question3')

    elif custom_id.endswith("_4"):
        WriteData.write_in_path(json.dumps(obj), f'{target_folder}/question4/question4')

    elif custom_id.endswith("_5"):
        WriteData.write_in_path(json.dumps(obj), f'{target_folder}/question5/question5')
        
    elif custom_id.endswith("_6"):
        WriteData.write_in_path(json.dumps(obj), f'{target_folder}/question6/question6')
        
    elif custom_id.endswith("_7"):
        WriteData.write_in_path(json.dumps(obj), f'{target_folder}/question7/question7')
        
    else:
        print(f"{custom_id} error...")


def data_aggregation_llama(subfolder):

    llama_folder = f'{parent_foler}/{subfolder}'

    for index in range(0, 15):
        batch_folder = f'{batch_folder_template}{index}'

        target_folder = f'{llama_folder}/{batch_folder}'

        prompt_output = f'{batch_folder}_output'

        destination = f'{target_folder}/{batch_folder}'
        destination_output = f'{target_folder}/{prompt_output}'

        print(target_folder)

        all_lines_output = read_files(destination_output, 'json')

        all_lines = read_files(destination, 'jsonl')

        dic = arrange_customid_title_llama(all_lines)

        for line in all_lines_output:
            json_obj = json.loads(line.rstrip())

            custom_id = json_obj['custom_id']
            title = dic[custom_id]

            if 'choices' in json_obj:
                output = json_obj['choices'][0]['message']['content']
            else:
                output = ''

            new_obj = {}
            new_obj['custom_id'] = custom_id
            new_obj['title'] = title
            new_obj['output'] = output

            write_customid_llama(new_obj, llama_folder)




# data_aggregation_llama('llama-3.1-sonar-small-128k-chat')

# data_aggregation_gpt('gpt-4o-mini')



