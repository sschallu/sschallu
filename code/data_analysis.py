import WriteData

import json

import requests

import time


def split(folder, question_num, file_name):

    with open(f'{folder}/{question_num}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        url = json_obj['url']

        if 'github.com' in url:
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{file_name}_github')

        elif 'https://registry.npmjs.org' in url or 'https://rubygems.org/gems' in url or 'https://packagist.org/packages' in url or 'https://pypi.org/project' in url or 'https://metacpan.org/pod' in url:
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{file_name}_packages')
        
        elif url.endswith('.js') or url.endswith('.css'):
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{file_name}_libraries')

        # elif status_code == 'exception':
        #     WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/issues/{file_name}_links_deprecated')

        else:
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{question_num}/{file_name}_links')


def github_account_check(folder, file_name):

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    token = ''

    headers = {
        "Authorization": f"Bearer {token}"
    }

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        # url = json_obj['url']
        url = json_obj['request_url']

        account = url.split('/')[-2]

        request_url = f'https://api.github.com/users/{account}'

        response = requests.get(request_url, headers=headers)

        status_code = response.status_code

        if status_code == 404:
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_hijacking')

        print(f'{request_url}: {status_code}')

        time.sleep(0.2)
        


def combine_batches_questions(folder, batch_number, question_num, file_name):

    with open(f'{folder}/{batch_number}/{question_num}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']

        package_request = json_obj['package_request']

        link_list = json_obj['link_list']

        for package in package_request:
            status = package[1]
            package_link = package[0]

            if status == 404 or status == 'exception':
                obj = {}
                obj['link'] = package_link
                obj['status'] = status

                WriteData.write_in_path(json.dumps(obj), f'{folder}/data_total/{file_name}_package_404')
                
        
        for link in link_list:
            status = link[1]
            link_detail = link[0]

            if status == 404 or status == 'exception':

                obj = {}
                obj['link'] = link_detail
                obj['status'] = status

                WriteData.write_in_path(json.dumps(obj), f'{folder}/data_total/{file_name}_link_404')

           

# folder = r'\batches\gpt-4o-mini\data_total'

folder = r'\defense'

# split(folder, 'question2', 'original_4o_mini_intersection_404_overview')
# github_account_check(folder, 'question6', '')

def get_total():

    question_num = 'question1'

    folder_template = 'batches_prompts_'

    for index in range(0, 15):

        batch_number = f'{folder_template}{index}'

        print(f'{folder}{batch_number}/{question_num}')
        
        combine_batches_questions(folder, batch_number, question_num, f'{question_num}_parse_request')

# get_total()

def read_files(destination, suffix):

    with open(f'{destination}.{suffix}', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    return all_lines


def deprecated_data(folder, filename):

    destination = f'{folder}/{filename}'

    all_lines = read_files(destination, "json")

    total = 0

    count_false = 0

    count_true = 0

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        total += 1

        deprecated = json_obj["deprecated"]

        
        if filename == 'package_total_php_new_request':
            if deprecated != False:
                count_true += 1
        
        else:
            if deprecated == True:
                count_true += 1
        
        
    # print(f'false: {count_false}')
    print(f'true: {count_true}')
    print(f'total: {total}')

# folder = r'\batches\gpt-4o-mini\data_total'
# folder = r'\batches\gpt-3.5-turbo\data_total'
# folder = r'\batches\llama-3.1-8b-instruct\data_total'
folder = r'\batches\llama-3.1-sonar-small-128k-chat\data_total'

question_list = ['question1', 'question2', 'question4', 'question6']

# for question in question_list:
#     print(question)

#     if question == 'question6':
#         print('package_total_nodejs_new_request')
#         deprecated_data(f'{folder}/{question}', 'package_total_nodejs_new_request')
#     else:
#         print('package_total_nodejs_request')
#         deprecated_data(f'{folder}/{question}', 'package_total_nodejs_request')

#     print('package_total_php_new_request')
#     deprecated_data(f'{folder}/{question}', 'package_total_php_new_request')

#     print('package_total_perl_new_request')
#     deprecated_data(f'{folder}/{question}', 'package_total_perl_new_request')

    




