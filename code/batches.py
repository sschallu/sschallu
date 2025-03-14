import WriteData

import json

import os

import random

from openai import OpenAI
client = OpenAI()


def get_top_1000_ids():

    folder = r''

    file_name = 'top_10000'

    id_collection = []

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        id = json_obj['id']

        if id not in id_collection:
            id_collection.append(id)
    
    return id_collection
    



def get_total_rest_questions():

    folder = r"\checked_tag_files"

    folder_array = os.listdir(folder)

    id_collection = get_top_1000_ids()

    for folder_name in folder_array:

        if folder_name == 'apache-camel' or folder_name == 'apache-flex' or folder_name == 'apache-kafka':
            continue
        
        file_path = os.path.join(folder, folder_name)

        # questions = os.path.join(file_path, f'{folder_name}_sort_tags_normal')
        # questions = os.path.join(file_path, f'{folder_name}_sort_tags_transformation_detail')

        questions_array = [f'{folder_name}_sort_tags_normal', f'{folder_name}_sort_tags_transformation_detail']

        for index in range(0, len(questions_array)):
            item = questions_array[index]

            questions = os.path.join(file_path, item)

            with open(f'{questions}.json', encoding='utf-8') as f:
                all_lines = f.readlines()
                f.close()
            
            take_number = 1300
            question_number = len(all_lines)

            if question_number < take_number:
                take_number = question_number
            
            for i in range(0, take_number):

                obj = json.loads(all_lines[i].rstrip())

                id = obj['id']

                if id in id_collection:
                    continue
                else:
                    id_collection.append(id)
                
                title = obj['title'].lower()

                print(title)

                if title.startswith('can') or title.startswith('cannot') or title.startswith('can not') or title.startswith('is') or title.startswith('does'):
                    continue

                if title.startswith('which') or title.startswith('why') or title.startswith('what'):
                    continue
                
                WriteData.write_in_path(all_lines[i].rstrip(), f'/rest_100000_{index}')



# get_total_rest_questions()



def split_batches():

    rest_100000_0 = "/rest_100000_0"
    rest_100000_1 = "/rest_100000_1"

    write_files = r"\batches"

    with open(f'{rest_100000_0}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    with open(f"{rest_100000_1}.json", encoding='utf-8') as f:
        all_line1 = f.readlines()
        f.close()

    for index in range(0, 14):

        take_number_1 = 3200
        take_number_total = 7000

        start_1 = index * take_number_1
        end_1 = (index + 1) * take_number_1


        if index == 13:
            file_number_1 = all_line1[start_1: len(all_line1)]
        else:
            file_number_1 = all_line1[start_1: end_1]

        rest_number_0 = take_number_total - take_number_1
        start_0 = index * rest_number_0
        end_0 = (index + 1) * rest_number_0

        if index == 13:
            file_number_0 = all_lines[start_0: len(all_lines)]
        else:
            file_number_0 = all_lines[start_0: end_0]
    

        for item0 in file_number_0:
            WriteData.write_in_path(item0.rstrip(), f'{write_files}/batches_{index}')
        
        for item1 in file_number_1:
            WriteData.write_in_path(item1.rstrip(), f'{write_files}/batches_{index}')


# split_batches()


def random_license():

    licenses_array = ['Public Domain', 'MIT/X11', 'BSD-new', 'Apache 2.0', 'LGPLv2.1', 'LGPLv2.1+', 'LGPLv3', 'LGPLv3+', 'MPL 1.1', 'GPLv2', 'GPLv2+', 'GPLv3', 'GPLv3+', 'Affero GPLv3', 'Proprietary']
    random_value = random.choice(licenses_array)

    return random_value


def transformation_new_questions(index):

    custom_id_array = []
    # chatgpt_model = 'gpt-4o-mini'
    chatgpt_model = 'gpt-3.5-turbo'
    # write_path = '/batches/questions_prompts/batches_prompts_'
    write_path = '/batches/gpt-3.5-turbo/batches_prompts_'
    read_path = '/batches/questions/batches_'

    template = 'batches_prompts_'

    system_message = 'You are a helpful assistant skilled in generating, explaining, and optimizing code across multiple programming languages.'

    with open(f'{read_path}{index}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:
        obj = json.loads(line.rstrip())

        id = obj['id']
        title = obj['title'].lower()
        
        if id not in custom_id_array:
            custom_id_array.append(id)
        else:
            continue

        print(f'{id}: {title}')


        new_obj1 = {}
        new_obj1['custom_id'] = f'{id}_1'
        new_obj1['method'] = 'POST'
        new_obj1['url'] = '/v1/chat/completions'
        new_obj1['body'] = {}
        new_obj1['body']['model'] = chatgpt_model
        new_obj1['body']['messages'] = []
        new_obj1['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj1['body']['messages'].append({'role': 'user', 'content': f'{title}'})
        new_obj1['body']['max_tokens'] = 1000
        
        WriteData.write_in_jsonl(json.dumps(new_obj1), f'{write_path}{index}/{template}{index}')

        license_value = random_license()

        prompt_2 = f'please give me a code example to solve or realize the following problem or task, {title}'

        new_obj2 = {}
        new_obj2['custom_id'] = f'{id}_2'
        new_obj2['method'] = 'POST'
        new_obj2['url'] = '/v1/chat/completions'
        new_obj2['body'] = {}
        new_obj2['body']['model'] = chatgpt_model
        new_obj2['body']['messages'] = []
        new_obj2['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj2['body']['messages'].append({'role': 'user', 'content': f'{prompt_2}'})
        new_obj2['body']['max_tokens'] = 1000

        WriteData.write_in_jsonl(json.dumps(new_obj2), f'{write_path}{index}/{template}{index}')


        prompt_3 = f'my software is under {license_value}, to maintain license compatibility with my software, please give me a code example to solve or realize the following problem or task, {title}'

        new_obj3 = {}
        new_obj3['custom_id'] = f'{id}_3'
        new_obj3['method'] = 'POST'
        new_obj3['url'] = '/v1/chat/completions'
        new_obj3['body'] = {}
        new_obj3['body']['model'] = chatgpt_model
        new_obj3['body']['messages'] = []
        new_obj3['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj3['body']['messages'].append({'role': 'user', 'content': f'{prompt_3}'})
        new_obj3['body']['max_tokens'] = 1000

        WriteData.write_in_jsonl(json.dumps(new_obj3), f'{write_path}{index}/{template}{index}')


        # new_title1 = f'please give me a package and its license, {title}'
        prompt_4 = f"please first give me a package, the package's registry, and its license in the fixed format (package-name, package-registry: package-license), and then show me how to use this package to solve or realize the following problem or task, {title}"

        new_obj4 = {}
        new_obj4['custom_id'] = f'{id}_4'
        new_obj4['method'] = 'POST'
        new_obj4['url'] = '/v1/chat/completions'
        new_obj4['body'] = {}
        new_obj4['body']['model'] = chatgpt_model
        new_obj4['body']['messages'] = []
        new_obj4['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj4['body']['messages'].append({'role': 'user', 'content': f'{prompt_4}'})
        new_obj4['body']['max_tokens'] = 1000

        WriteData.write_in_jsonl(json.dumps(new_obj4), f'{write_path}{index}/{template}{index}')

        prompt_5 = f"my software is under {license_value}, to maintain license compatibility with my software, please first give me a package, the package's registry, and its license in the fixed format (package-name, package-registry: package-license), and then show me how to use this package to solve or realize the following problem or task, {title}"

        new_obj5 = {}
        new_obj5['custom_id'] = f'{id}_5'
        new_obj5['method'] = 'POST'
        new_obj5['url'] = '/v1/chat/completions'
        new_obj5['body'] = {}
        new_obj5['body']['model'] = chatgpt_model
        new_obj5['body']['messages'] = []
        new_obj5['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj5['body']['messages'].append({'role': 'user', 'content': f'{prompt_5}'})
        new_obj5['body']['max_tokens'] = 1000

        WriteData.write_in_jsonl(json.dumps(new_obj5), f'{write_path}{index}/{template}{index}')



        # new_title = f'please give me five more packages and their licenses, {title}'
        prompt_6 = f"please further give me five more packages, the packages' registries, and their licenses in the fixed format (package-name, package-registry: package-license) to solve or realize the following problem or task (this time please don't show me the code detail), {title}"
        
        new_obj6 = {}

        new_obj6['custom_id'] = f'{id}_6'
        new_obj6['method'] = 'POST'
        new_obj6['url'] = '/v1/chat/completions'
        new_obj6['body'] = {}
        new_obj6['body']['model'] = chatgpt_model
        new_obj6['body']['messages'] = []
        new_obj6['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj6['body']['messages'].append({'role': 'user', 'content': f'{prompt_6}'})
        new_obj6['body']['max_tokens'] = 1000

        WriteData.write_in_jsonl(json.dumps(new_obj6), f'{write_path}{index}/{template}{index}')


        prompt_7 = f"my software is under {license_value}, to maintain license compatibility with my software, please only give me five more packages, the packages' registries, and their licenses in the fixed format (package-name, package-registry: package-license) to solve or realize the following problem or task (this time please don't show me the code detail), {title}"

        new_obj7 = {}
        new_obj7['custom_id'] = f'{id}_7'
        new_obj7['method'] = 'POST'
        new_obj7['url'] = '/v1/chat/completions'
        new_obj7['body'] = {}
        new_obj7['body']['model'] = chatgpt_model
        new_obj7['body']['messages'] = []
        new_obj7['body']['messages'].append({'role': 'system', 'content': system_message})
        new_obj7['body']['messages'].append({'role': 'user', 'content': f'{prompt_7}'})
        new_obj7['body']['max_tokens'] = 1000

        WriteData.write_in_jsonl(json.dumps(new_obj7), f'{write_path}{index}/{template}{index}')



def begin_generate_prompts():

    for index in range(0, 14):

        transformation_new_questions(index)


# begin_generate_prompts()






