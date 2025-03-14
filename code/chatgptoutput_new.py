import WriteData

import json

import requests

from markdown import markdown

from bs4 import BeautifulSoup

import re

import requests

import time


def parse_output():

    dic = get_custom_id()

    with open(f'/gpt-3.5-turbo/top_70000_output.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    total = 0
    for line in all_lines:

        obj = json.loads(line.rstrip())

        custom_id = obj['custom_id']

        choices = obj['response']['body']['choices']

        content = choices[0]['message']['content']

        html = markdown(content, output_format='html5')

        soup = BeautifulSoup(html, 'html.parser')
        
        json_obj = {}
        json_obj['custom_id'] = custom_id
        json_obj['title'] = dic[custom_id]
        # json_obj['content'] = content
        # json_obj['output'] = []

        # print(custom_id)
        # if custom_id == '5001225_nodejs_3':
        #     print(soup)
        # else:
        #     continue
        
        pattern = r'^```(?:\w+)?\s*\n(.*?)(?=^```)```'
        result = re.findall(pattern, content, re.DOTALL | re.MULTILINE)

        json_obj['output'] = result
        json_obj['content'] = []
        json_obj['http'] = []
        json_obj['list'] = []       
        
        # for question1 and question2
        if custom_id.endswith('_2'):
            # WriteData.write_in_html(soup, f'/question1/4o-mini/{custom_id}')

            content_array = content.split('\n')
            filtered_array = list(filter(lambda x: x.strip(), content_array))
            json_obj['content'] = filtered_array

            for a in soup.findAll('a'):
                if a.get('href') is not None:
                    href = a.get('href')

                    if href.startswith('http'):
                        json_obj['http'].append(href.replace('\n', ''))

            WriteData.write_in_path(json.dumps(json_obj), '/gpt-3.5-turbo/question2/question2')


        # _5 and _6 
        # if custom_id.endswith('_3'):
        #     # for question4 only
        #     for li in soup.findAll('li'):
        #         print(li.get_text())
        #         # json_obj['output'].append(li.get_text().replace('\n', ''))
        #         json_obj['list'].append(li.get_text().replace('\n', ''))
            
        #     for a in soup.findAll('a'):
        #         if a.get('href') is not None:
        #             href = a.get('href')

        #             if href.startswith('http'): 
        #                 print(href)
        #                 # json_obj['output'].append(a.get('href').replace('\n', ''))
        #                 json_obj['http'].append(href.replace('\n', ''))
            
        #     WriteData.write_in_path(json.dumps(json_obj), '/gpt-3.5-turbo/question3/question3')


        # if custom_id.endswith('_6'):

        #     content_array = content.split('\n')
        #     filtered_array = list(filter(lambda x: x.strip(), content_array))
        #     json_obj['content'] = filtered_array

        #     for li in soup.findAll('li'):
        #         print(li.get_text())
        #         json_obj['list'].append(li.get_text().replace('\n', ''))

        #     for a in soup.findAll('a'):
        #         if a.get('href') is not None:
        #             href = a.get('href')

        #             if href.startswith('http'):
        #                 json_obj['http'].append(href.replace('\n', ''))

        #     WriteData.write_in_path(json.dumps(json_obj), '/gpt-3.5-turbo/question6/question6')
        
        



def get_custom_id():

    with open(f'/top_70000.jsonl', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    dictionary = {}

    for line in all_lines:
        obj = json.loads(line.rstrip())

        custom_id = obj['custom_id']

        content = obj['body']['messages'][1]['content']

        dictionary[custom_id] = content
    
    return dictionary


def tag_collections():

    dic = {}
    with open(f'/top_10000.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    
    for line in all_lines:

        obj = json.loads(line.rstrip())

        id = obj['id']

        dic[f'{id}'] = obj['tags']

    return dic


# for question3, question4, question5, question6
def tag_identification():

    languages = ['javascript', 'python', 'php', 'ruby', 'typescript', 'perl', 'node.js']

    with open(f'/gpt-3.5-turbo/question3/question3.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    tags_list = tag_collections()
    
    for line in all_lines:

        obj = json.loads(line.rstrip())

        new_obj = {}
        new_obj['custom_id'] = obj['custom_id']
        new_obj['title'] = obj['title']

        custom_id = obj['custom_id']

        id_array = custom_id.split('_')

        id = id_array[0]
        if len(id_array) > 2:
            id = f'{id_array[0]}_{id_array[1]}'

        title = obj['title'].lower().replace('?', '').replace('nodejs', 'node.js')

        tags = tags_list[id].split('|')

        word_array = title.split(' ')
        title_target = ''
        for word in word_array:
            if word in languages:
                title_target = word
                break
        
        tag_target = ''
        for tag in tags:
            if tag in languages:
                tag_target = tag
                break
        
        if title_target != '':
            new_obj['label'] = title_target

        elif tag_target != '':
            new_obj['label'] = tag_target
        
        else:
            custom_id_array = custom_id.split('_')
            new_obj['label'] = custom_id_array[1]
        
        new_obj['output'] = obj['output']
        new_obj['content'] = obj['content']
        new_obj['http'] = obj['http']
        new_obj['list'] = obj['list']

        WriteData.write_in_path(json.dumps(new_obj), '/gpt-3.5-turbo/question3/question3_tags_identification')


def deal_question1_output():
    
    pattern = r'^(?:@[a-zA-Z0-9_-]+/)?[a-zA-Z0-9_-]+(/[a-zA-Z0-9_-]+)*(\.[a-zA-Z0-9_-]+)*$'
    http_pattern = r'https?://[^\s/$.?#].[^\s]*'

    with open(f'/gpt-3.5-turbo/question7/question7.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    distinct = []
    install_array = ['npm install', 'pip install', 'composer require', 'gem install', 'cpanm ', 'cpan ']
    skip_words = ['or', 'any', 'other', 'you', 'want', 'to', 'use', 'module::name', '.', 'libraryname', './', 'xxx', 'run', 'install', 'npm', 'run:', 'requirements.txt', 'pip', '&&', 'n', '\\', '0.0.0.0:8000', '$']

    for line in all_lines:

        obj = json.loads(line.rstrip())

        output_list = obj['output']

        obj['libraries'] = []

        new_output = []

        for output in output_list:

            sub_output_list = output.split('\n')

            for sub_output in sub_output_list:
                
                links = re.findall(http_pattern, sub_output)

                for link in links:

                    if 'localhost' in link or 'example.com' in link or 'your' in link.lower() or '127.0.0.1' in link or ':port' in link or '<' in link:
                        continue
                    
                    link = link.replace('"', '').replace(';', '').replace(',', '').replace(')', '').replace("'", "").replace('}', '').replace('`', '').replace('></script>', '').replace('>', '').replace(']', '').replace('\\', '')
                    
                    if '?' in link:
                        link = link.split('?')[0]
                    
                    
                    obj['libraries'].append(link)



                for install in install_array:

                    if install in sub_output and not sub_output.startswith('#'):

                        sub_output = sub_output.replace('//', '').replace('"', '').replace('cpan install', 'cpan').strip()
                        
                        sub_install_array = sub_output.split(f'{install.strip()} ')
                        filtered_array = list(filter(lambda x: x.strip(), sub_install_array))
                        
                        target_str = filtered_array[0]

                        if len(filtered_array) > 1:
                            target_str = filtered_array[1]
                        
                        if '#' in target_str:
                            target_str = target_str.split('#')[0].strip()
                        
                        target_str_array = target_str.split(' ')

                        for target in target_str_array:
                            
                            target = target.replace("'", "")

                            if target.startswith('-') or target.startswith('--'):
                                continue
                            
                            if '<' in target or 'username' in target or '>' in target or 'package-name' in target or 'package_name' in target or '}' in target or '{' in target or 'example-package' in target:
                                continue
                                
                            if target.lower() in skip_words:
                                continue

                            if 'github.com' in target and 'username' not in target.lower():
                                temp = target.split('github.com')[1]
                                new_output.append([install.strip(), f'https://github.com/{temp}'])
                            
                            elif '===' in target:
                                package = target.split('===')
                                # print(f'{package[0]}: {package[1]}')
                                new_output.append([install.strip(), package[0], package[1]])

                            elif '==' in target and '===' not in target:
                                package = target.split('==')
                                # print(f'{package[0]}: {package[1]}')
                                new_output.append([install.strip(), package[0], package[1]])

                            elif '@' in target and not target.startswith('@'):
                                package = target.split('@')
                                # print(f'{package[0]}: {package[1]}')
                                new_output.append([install.strip(), package[0], package[1]])

                            elif ':' in target and 'https' not in target:
                                if install.strip() in ['cpan', 'cpanm']:
                                    continue
                                
                                package = target.split(':')
                                # print(f'{package[0]}: {package[1]}')
                                new_output.append([install.strip(), package[0], package[1]])

                            else:
                                # if target not in distinct:
                                #     distinct.append(target)
                                new_output.append([install.strip(), target])
                
        obj['output'] = new_output
        obj['content'] = ''

        if len(obj['output']) > 0 or len(obj['libraries']) > 0 or len(obj['http']) > 0 or len(obj['list']) > 0:

            WriteData.write_in_path(json.dumps(obj), '/gpt-3.5-turbo/question7/question7_parse')
    


# deal_question1_output()

# tag_identification()

# parse_output()



