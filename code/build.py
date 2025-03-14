import pandas

import json

import WriteData

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

from markdown import markdown

from bs4 import BeautifulSoup

import re

import requests

import time


# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')

def github_tags():

    with open(r'/checked_tag_files/github/github_sort.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    dic = {}

    return_array = []

    for line in all_lines:

        obj = json.loads(line.rstrip())
        tags = obj['tags']

        tags_array = tags.split('|')

        for tag in tags_array:

            if tag == 'github':
                continue

            if tag not in dic.keys():
                dic[tag] = 1
            else:
                dic[tag] += 1
    
    sorted_dict = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))

    for key in sorted_dict.keys():

        # if 'github' in key:
        #     return_array.append(key)
        if sorted_dict[key] > 100:
            print(f'{key}: {sorted_dict[key]}')

    return return_array

# github_tags()



def get_title():

    # keywords = ['github', 'github-actions', 'build', 'deployment', 'yaml', 'testing', 'unit-testing', 'build-automation', 'pipeline', 'automated-tests', 'integration-testing', 'cicd']
    
    # keywords = github_tags()
    

    skip_words = ['error', 'exception', 'failed', 'fail', 'failure', 'warning', 'denied', 'forbidden', 'not found', 'not', 'cancel', 'unable', 'cannot', 'stop', 'doesn\'t', 'can\'t', 'don\'t', 'err:', 'error:', '404', 'fatal:', 'no', 'failing', 'failing:', 'fails']

    with open(r'/checked_tag_files/continuous-integration/continuous-integration_sort.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    dic = []

    total = 0

    for line in all_lines:

        obj = json.loads(line.rstrip())
        
        id = obj['id']

        title = obj['title'].lower()

        # print(title)

        tags = obj['tags']

        tags_array = tags.split('|')

        # tag_flag = False
        # for tag in tags_array:

        #     if tag in keywords:
        #         if id not in dic:
        #             tag_flag = True
        #             dic.append(id)
                    
        tag_flag = True
        title_flag = True
        if tag_flag is True:

            word_array = title.split(' ')

            for word in word_array:
                if word in skip_words:
                    title_flag = False
                    break

        if tag_flag is True and title_flag is True:

            total += 1

            if 'jenkins' in title or 'gitlab' in title or 'azure' in title or 'circle' in title or 'circleci' in title or 'teamcity' in title or 'bitbucket' in title or 'travis.yml' in title or 'bamboo' in title or 'travis' in title:
                title = title.replace('jenkins', 'github').replace('gitlab', 'github').replace('azure', 'github').replace('circleci', 'github').replace('circle', 'github').replace('teamcity', 'github').replace('bitbucket', 'github').replace('travis.yml', 'github').replace('bamboo', 'github').replace('travis', 'github')
                # continue

            title = title.replace('?', '')

            if len(title.split(' ')) <= 3:
                continue
            
            if title.startswith('github'):
                title = title.replace('github actions - ', '').replace('github actions:', '').replace('github action:', '').replace('github action - ', '').strip()
                # print(title)
            
            if title.startswith('is ') or title.startswith('are') or title.startswith('was') or title.startswith('were') or title.startswith('can ') or title.startswith('could') or title.startswith('what') or title.startswith('why') or title.startswith('where') or title.startswith('do ') or title.startswith('does ') or title.startswith('which'):
                # total += 1

                if ' to ' in title:
                    title = title.split(' to ')[-1]
                    
                else:
                    if title.startswith('is '):
                        title = ' '.join(title.split(' ')[1:])
                    else:
                        title = ' '.join(title.split(' ')[2:])

        
            print(title)

            new_obj = {}
            new_obj['id'] = obj['id']
            new_obj['title'] = title
            new_obj['tags'] = obj['tags']
            new_obj['view_count'] = obj['view_count']
            new_obj['answer_count'] = obj['answer_count']
            new_obj['comment_count'] = obj['comment_count']

            WriteData.write_in_path(json.dumps(new_obj), '/checked_tag_files/continuous-integration/continuous-integration_sort_tags_build')
                

    print(total)


# get_title()



def get_title2():

    keywords_github = ['github-actions', 'version-control', 'repository', 'pull-request', 'deployment', 'continuous-integration', 'yaml', 'cicd', 'build', 'testing', 'jenkins', 'bitbucket', 'travis-ci', 'jenkins-pipeline', 'jenkins-plugins', 'teamcity', 'circleci']
    # keywords_github = ['jenkins', 'bitbucket', 'travis-ci', 'jenkins-pipeline', 'jenkins-plugins', 'teamcity', 'circleci']

    skip_words = ['error', 'exception', 'failed', 'fail', 'failure', 'warning', 'denied', 'forbidden', 'not found', 'not', 'cancel', 'unable', 'cannot', 'stop', 'doesn\'t', 'can\'t', 'don\'t', 'err:', 'error:', '404', 'fatal:', 'no', 'failing', 'failing:', 'fails']

    with open(r'/checked_tag_files/github/github_sort.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    dic = []

    total = 0

    for line in all_lines:

        obj = json.loads(line.rstrip())
        
        id = obj['id']

        title = obj['title'].lower()

        if 'jenkins' in title or 'gitlab' in title or 'azure' in title or 'circle' in title or 'circleci' in title or 'teamcity' in title or 'bitbucket' in title or 'travis.yml' in title or 'bamboo' in title or 'travis' in title:
                title = title.replace('jenkins', 'github').replace('gitlab', 'github').replace('azure', 'github').replace('circleci', 'github').replace('circle', 'github').replace('teamcity', 'github').replace('bitbucket', 'github').replace('travis.yml', 'github').replace('bamboo', 'github').replace('travis', 'github')

        if title.startswith('github'):
            title = title.replace('github actions - ', '').replace('github actions:', '').replace('github action:', '').replace('github action - ', '').replace('github:', '').replace('github -', '').strip()
    
        # if title.startswith('github action'):
        #     title = title.replace('-', '').replace(':', '').replace(',', '').replace('github actions', '').replace('github action', '').strip()
        
        # if title.startswith('github workflow'):
        #     title = title.replace('-', '').replace(':', '').replace(',', '').replace('github workflows', '').replace('github workflow', '').strip()

        tags = obj['tags']

        tags_array = tags.split('|')

        tag_flag = False
        for tag in tags_array:
            if tag == 'github':
                continue

            if tag in keywords_github:
                if id not in dic:
                    tag_flag = True
                    dic.append(id)
                    
        title_flag = True
        if tag_flag is True:

            word_array = title.split(' ')

            for word in word_array:
                if word in skip_words:
                    title_flag = False
                    break
        

        if tag_flag is True and title_flag is True and len(title.split(' ')) > 3:
            
            # first_word = title.split(' ')[0]

            # if first_word == 'how':
            #     if not title.startswith('how to') and not title.startswith('how can i') and not title.startswith('how do i'):
            #         print(title)

            # if first_word != 'how':
            #     if ' to ' not in title:
            #         print(title)
            #---------------------------------------------
            if title.startswith('is ') or title.startswith('are') or title.startswith('was') or title.startswith('were') or title.startswith('can ') or title.startswith('could') or title.startswith('what') or title.startswith('why') or title.startswith('where') or title.startswith('do ') or title.startswith('does ') or title.startswith('which'):
                # total += 1

                if ' to ' in title:
                    title = title.split(' to ')[-1]
                    
                else:
                    if title.startswith('is '):
                        title = ' '.join(title.split(' ')[1:])
                    else:
                        title = ' '.join(title.split(' ')[2:])

            print(title)

            new_obj = {}
            new_obj['id'] = obj['id']
            new_obj['title'] = title
            new_obj['tags'] = obj['tags']
            new_obj['view_count'] = obj['view_count']
            new_obj['answer_count'] = obj['answer_count']
            new_obj['comment_count'] = obj['comment_count']

            WriteData.write_in_path(json.dumps(new_obj), '/checked_tag_files/github/github_sort_tags_build')
           
            total += 1
        

    print(total)
  

# get_title2()


def top_build_unique():

    with open(r'/data_again/build/top_build.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    # with open(r'/checked_tag_files/github/github_sort_tags_build.json', encoding='utf-8') as f:
    #     all_lines = f.readlines()
    #     f.close()
    
    id_collection = []

    for line in all_lines:
        obj = json.loads(line.rstrip())

        id = obj['id']

        if id not in id_collection:
            id_collection.append(id)
            # print(id)
            # WriteData.write_in_path(json.dumps(obj), '/data_begin/build/top_build')
    
    
    # with open(r'/checked_tag_files/continuous-integration/continuous-integration_sort_tags_build.json', encoding='utf-8') as f:
    #     all_lines1 = f.readlines()
    #     f.close()

    with open(r'/checked_tag_files/github/github_sort_tags_build.json', encoding='utf-8') as f:
        all_lines1 = f.readlines()
        f.close()

    for line1 in all_lines1:
        json_obj = json.loads(line1.rstrip())

        id = json_obj['id']

        if id not in id_collection:

            id_collection.append(id)
            print(id)
            WriteData.write_in_path(json.dumps(json_obj), '/data_again/build/top_build')

# top_build_unique()


def transformation_questions():

    chatgpt_model = 'gpt-4o-mini'
    system_message = 'You are a helpful assistant skilled in generating, explaining, and optimizing code across multiple programming languages.'

    with open(r'/data_again/build/top_build.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:

        obj = json.loads(line.rstrip())

        title = obj['title']

        id = obj['id']

        # if title.startswith('how'):
            
        #     if title.startswith('how to'):
        #         title = title.replace('how to', 'please give me a complete github actions configuration file to')
            
        #     elif title.startswith('how can i'):
        #         title = title.replace('how can i', 'please give me a complete github actions configuration file to')
            
        #     elif title.startswith('how do i'):
        #         title = title.replace('how do i', 'please give me a complete github actions configuration file to')

        #     else:
        #         title = title.replace('how', 'please give me a complete github actions configuration file to')

        # elif ' to ' in title:

        #     temp = title.split(' to ')[1]
        #     title = f'please give me a complete github actions configuration file to {temp}'
            
        # else:

        #     title = f'please give me a complete github actions configuration file to {title}'

        
        title = title.replace('?', '')

        title = f'please give me a complete github actions configuration file to solve or realize the following problem or task, {title}'

        new_obj = {}
        new_obj['custom_id'] = f'{id}'
        new_obj['method'] = 'POST'
        new_obj['url'] = '/v1/chat/completions'
        new_obj['body'] = {}
        # new_obj['body']['model'] = 'gpt-3.5-turbo'
        new_obj['body']['model'] = chatgpt_model
        new_obj['body']['messages'] = []
        new_obj['body']['messages'].append({'role': 'system', 'content': f'{system_message}'})
        new_obj['body']['messages'].append({'role': 'user', 'content': f'{title}'})
        new_obj['body']['max_tokens'] = 1500
        
        WriteData.write_in_path(json.dumps(new_obj), '/data_again/build/top_build_trans_4o-mini')


# transformation_questions()


def get_custom_id():

    with open(f'/data_again/build/top_build_trans_4o-mini.jsonl', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    dictionary = {}

    for line in all_lines:
        obj = json.loads(line.rstrip())

        custom_id = obj['custom_id']

        content = obj['body']['messages'][1]['content']

        dictionary[custom_id] = content
    
    return dictionary


def parse_output():

    http_pattern = r'https:\/\/(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}(?:\/[^\s]*)?'

    dic = get_custom_id()

    # with open(f'/data_again/build/top_build_trans_4o-mini_output.jsonl', encoding='utf-8') as f:
    #     all_lines = f.readlines()
    #     f.close()

    with open(r'\build\chatgpt-3.5-turbo\top_build_trans_3.5-turbo_output.jsonl', encoding='utf-8') as f:
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
        
        
        pattern = r'^```(?:\w+)?\s*\n(.*?)(?=^```)```'
        result = re.findall(pattern, content, re.DOTALL | re.MULTILINE)

        json_obj['output'] = result
        json_obj['http'] = []


        for a in soup.findAll('a'):
            if a.get('href') is not None:
                href = a.get('href')

                if href.startswith('http'):
                    json_obj['http'].append(href.replace('\n', ''))

        
        content_array = content.split('\n')
        filtered_array = list(filter(lambda x: x.strip(), content_array))

        for item in filtered_array:
            if 'https://' in item and 'localhost' not in item and 'endpoint.com' not in item and 'example' not in item and 'YOUR_PARSE_SERVER_URL' not in item and 'YOUR_DOMAIN' not in item and 'user' not in item and 'your' not in item and '{' not in item and 'name' not in item and 'YOUR' not in item and '$' not in item and 'external' not in item and 'USER' not in item and 'OWNER' not in item and 'REPO' not in item and 'owner' not in item and 'repo' not in item and 'organization' not in item:
                https = re.findall(http_pattern, item)
                if len(https) > 0:
                    for http in https:
                        http = http.replace(').', '').replace(',', '').replace(')', '').replace(';', '').replace("'", '').replace('></script>', '').replace('"', '').replace('>', '').replace(']', '').replace('`', '').replace('</url', '').replace('/:', '')
                        if http not in json_obj['http']:
                            print(http)
                            json_obj['http'].append(http)


        for i in range(0, len(result)):
            WriteData.write_in_yml(result[i], f'/data_again/build/configuration_files/chatgpt-3.5-turbo/{custom_id}_{i}')

        json_obj['output'] = ''
        
        # WriteData.write_in_path(json.dumps(json_obj), '/data_again/build/top_build_trans_4o-mini_parse')
        # time.sleep(0.1)


# parse_output()


def parse_output_llama():


    # with open(f'/data_again/build/top_build_trans_4o-mini_output.jsonl', encoding='utf-8') as f:
    #     all_lines = f.readlines()
    #     f.close()

    with open(r'\build\llama-3.1-8b-instruct\top_build_trans_instruct_output.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:

        obj = json.loads(line.rstrip())

        if 'outputs' in obj:
            continue

        custom_id = obj['custom_id']

        choices = obj['choices']

        content = choices[0]['message']['content']


        pattern = r'^```(?:\w+)?\s*\n(.*?)(?=^```)```'
        result = re.findall(pattern, content, re.DOTALL | re.MULTILINE)

        for i in range(0, len(result)):

            if i > 10:
                continue
            WriteData.write_in_yml(result[i], f'/data_again/build/configuration_files/llama-3.1-8b-instruct/{custom_id}_{i}')


# parse_output_llama()       


def category_actions(folder, filename):

    http_pattern = r'https?://[^\s/$.?#].[^\s]*'

    with open(f'{folder}/{filename}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    action_collection = {}
    
    for line in all_lines:
        obj = json.loads(line.rstrip())

        id = obj['id']

        jobs = obj['jobs']

        http_links = []

        for job in jobs:
            
            steps = job['steps']

            for step in steps:
                type = step['type']

                # if type == 'shell_cmd':
                #     cmd = step['cmd']

                #     if cmd is None:
                #         continue

                #     links = re.findall(http_pattern, cmd)
                #     for link in links:
                #         link = link.replace('"', '').replace("'", "").replace(')', '').replace(';', '')
                #         http_links.append(link)

                if type == 'gh_action':
                    name = step['name']
                    version = step['version']

                    if name not in action_collection.keys():
                        action_collection[name] = []
                    
                    if version not in action_collection[name]:
                        action_collection[name].append(version)


        # if len(http_links) > 0:
        #     new_obj = {}
        #     new_obj['id'] = id
        #     new_obj['http'] = http_links
        #     WriteData.write_in_path(json.dumps(new_obj), '/data_begin/build/top_build_trans_4o-mini_output_parse_http')
    
    
    print(len(action_collection.keys()))

    for key in action_collection.keys():
        new_obj = {}
        new_obj['action'] = key
        new_obj['versions'] = action_collection[key]

        if key.startswith('./') or key.startswith('docker://') or '<' in key or '{' in key or key.startswith('.github') or 'your' in key or ':latest' in key:
            continue

        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{filename}_actions')

# folder = r'\build\chatgpt-4o-mini'
# folder = r'\build\chatgpt-3.5-turbo'
# folder = r'\build\llama-3.1-sonar-small-128k-chat'

# category_actions(folder, 'top_build_output_parse')
        

def request_actions(folder, filename):

    github_http = 'https://github.com/'

    with open(f'{folder}/{filename}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()


    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        action = json_obj['action']

        versions = json_obj['versions']
        
        request_url = f'{github_http}{action}'

        print(request_url)

        # if action != 'erlef/setup-elixir':
        #     continue

        response = requests.get(request_url)

        time.sleep(0.3)
        

        # history_list = response.history
        
        # for history in history_list:
        #     redirected.append(history.url)


        new_obj = {}
        new_obj['action'] = action
        new_obj['versions'] = versions
        new_obj['request_url'] = request_url

        status_code = response.status_code

        new_obj['status_code'] = status_code

        if request_url != response.url:
            print(response.url)
            new_obj['redirected_url'] = response.url
        
        else:
            new_obj['redirected_url'] = ''

        print(f'{request_url}: {status_code}')
        
        WriteData.write_in_path(json.dumps(new_obj), f'{folder}/{filename}_request')




def request_https():

    dic = {}

    with open(f'/data_again/build/top_build_trans_4o-mini_parse_http.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    total = 0
    for line in all_lines:

        obj = json.loads(line.rstrip())

        http_list = obj['http']
        
        if len(http_list) <= 0:
            continue

        new_http = []

        for http in http_list:

            total += 1

            http = http.replace(',', '')

            if 'localhost' in http or http.endswith("${{") or 'yourusername' in http or 'example' in http or 'OWNER/REPO' in http or 'your-username' in http or 'your' in http:
                continue
            

            if http in dic.keys():
                print(f'{total}_{http}_already: {status_code}')

                new_http.append([http, dic[http]])
            
            else:

                try:
                    response = requests.get(http)

                    time.sleep(0.3)

                    status_code = response.status_code

                    print(f'{total}_{http}: {status_code}')

                    new_http.append([http, status_code])

                    dic[http] = status_code
                
                except:
                    print(f'{http}: exception...')

                    new_http.append([http, 'exception'])

                    dic[http] = 'exception'


        new_obj = {}
        new_obj['custom_id'] = obj['custom_id']
        new_obj['request_url'] = new_http

        WriteData.write_in_path(json.dumps(new_obj), '/data_again/build/top_build_trans_4o-mini_parse_http_request')

# request_https()


def split_found_not_found():

    with open(f'/data_again/build/top_build_trans_4o-mini_output_parse_actions_request.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        status_code = json_obj['status_code']

        redirected_urls = json_obj['redirected_urls']

        if status_code == 404:
            WriteData.write_in_path(json.dumps(json_obj), '/data_again/build/top_build_trans_4o-mini_output_parse_actions_request_404')
        
        if len(redirected_urls) > 0:
            WriteData.write_in_path(json.dumps(json_obj), '/data_again/build/top_build_trans_4o-mini_output_parse_actions_request_redirection')
        
        if status_code != 404:
            WriteData.write_in_path(json.dumps(json_obj), '/data_again/build/top_build_trans_4o-mini_output_parse_actions_request_remain')


# split_found_not_found()


def split_found_not_found_http():

    with open(f'/data_again/build/top_build_trans_4o-mini_parse_http_request.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        request_url = json_obj['request_url']

        if len(request_url) <= 0:
            continue

        for request in request_url:
            status_code = request[1]

            if status_code != 200:
                WriteData.write_in_path(json.dumps(json_obj), '/data_again/build/top_build_trans_4o-mini_parse_http_request_404')
                break

# split_found_not_found_http()


def github_account_check(folder, file_name):

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    token = ''

    headers = {
        "Authorization": f"Bearer {token}"
    }

    account_array = []

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        status_code = json_obj['status_code']

        if status_code != 404:
            continue

        action = json_obj['action']

        account = action.split('/')[0]

        if account in account_array:
            continue

        account_array.append(account)

        request_url = f'https://api.github.com/users/{account}'

        response = requests.get(request_url, headers=headers)

        status_code = response.status_code

        if status_code == 404:
            json_obj['account'] = account
            WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{file_name}_hijacking')

        print(f'{request_url}: {status_code}')

        time.sleep(0.2)


def tags_branch_checks(folder, filename):

    with open(f'{folder}/{filename}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    token = ''

    headers = {
        "Authorization": f"Bearer {token}"
    }


    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        action = json_obj['action']

        versions = json_obj['versions']

        status_code = json_obj['status_code']

        if status_code != 200:
            continue

        tags_result = []
        branch_result = []

        for version in versions:

            # tag_url = f'https://api.github.com/repos/{action}/releases/tags/{version}'
            tag_url = f'https://github.com/{action}/releases/tag/{version}'

            branch_url = f'https://api.github.com/repos/{action}/branches/{version}'

            # branch_url = f'https://github.com/{action}/tree/{version}'

            response_tag = requests.get(tag_url, headers=headers)

            tag_code = response_tag.status_code

            tags_result.append([version, tag_code])

            print(f'{action}: tag_{version}, {tag_code}')

            time.sleep(0.5)

            response_branch = requests.get(branch_url, headers=headers)

            branch_code = response_branch.status_code

            branch_result.append([version, branch_code])

            print(f'{action}: branch_{version}, {branch_code}')

            time.sleep(0.5)

        json_obj['tag_results'] = tags_result
        json_obj['branch_results'] = branch_result
        WriteData.write_in_path(json.dumps(json_obj), f'{folder}/{filename}_tagbranch')


def branch_tag_result_analysis(folder, filename):

    with open(f'{folder}/{filename}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    total = 0

    unique = {}

    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        action = json_obj['action']

        tag_results = json_obj['tag_results']

        branch_results = json_obj['branch_results']

        if action == 'appleboy/ssh-action':
            print(f'branch: {len(branch_results)}, tag: {len(tag_results)}')

        length = len(tag_results)

        for index in range(0, length):
            
            tag_array = tag_results[index]

            branch_array = branch_results[index]
            
            if tag_array[1] == 404 and branch_array[1] == 404:
                total += 1
                if action not in unique.keys():
                    unique[action] = [tag_array[0]]
                else:
                    unique[action].append(tag_array[0])
                # print(f'{action}: {tag_array[0]}')

            # if tag_array[1] == 200 and branch_array[1] == 200:
            #     total += 1
            #     # print(f'{action}: {tag_array[0]}')
            #     if action not in unique.keys():
            #         unique[action] = [tag_array[0]]
            #     else:
            #         unique[action].append(tag_array[0])

    # print(total)
    sorted_data = sorted(unique.items(), key=lambda item: len(item[1]), reverse=True)
    new_unique = dict(sorted_data)
    for key in new_unique.keys():
        print(f'{key}: {new_unique[key]}')
    
    print(len(new_unique.keys()))


def github_account_check_only(folder, file_name):

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    with open(f'{folder}/{file_name}_hijacking.json', encoding='utf-8') as f:
        all_lines1 = f.readlines()
        f.close()
    
    hijacking_account = []
    for line1 in all_lines1:
        new_obj = json.loads(line1.rstrip())
        account = new_obj['account']
        hijacking_account.append(account)

    account_array = {}

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        status_code = json_obj['status_code']

        if status_code != 404:
            continue

        action = json_obj['action']

        account = action.split('/')[0]

        if account in account_array.keys():
            account_array[account] += 1
            continue
        else:
            account_array[account] = 1

    sorted_data = sorted(account_array.items(), key=lambda item: item[1], reverse=True)
    new_unique = dict(sorted_data)
    for key in new_unique.keys():
        if key in hijacking_account:
            print(f'{key}: {new_unique[key]}')

    print(len(account_array.keys()))


def github_redirection_check(folder, file_name):

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    token = ''

    headers = {
        "Authorization": f"Bearer {token}"
    }

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        redirected_url = json_obj['redirected_url']

        request_url = json_obj["request_url"]

        if redirected_url == "":
            continue

        print(f'{request_url}: {redirected_url}')

        action = json_obj['action'].replace(" ", "")

        account = action.split('/')[0]

        request_url = f'https://api.github.com/users/{account}'

        response = requests.get(request_url, headers=headers)

        status_code = response.status_code

        if status_code == 404:
            print(f"redirected: {account}")



# branch_tag_result_analysis()


# folder = r'\build\chatgpt-4o-mini'
# folder = r'\build\chatgpt-3.5-turbo'
# folder = r'\build\llama-3.1-8b-instruct'
folder = r'\build\llama-3.1-sonar-small-128k-chat'

# request_actions(folder, 'top_build_output_parse_actions')

# github_account_check(folder, 'top_build_output_parse_actions_request')
# github_account_check_only(folder, 'top_build_output_parse_actions_request')

# tags_branch_checks(folder, 'top_build_output_parse_actions_request')

branch_tag_result_analysis(folder, 'top_build_output_parse_actions_request_tagbranch')

# github_redirection_check(folder, 'top_build_output_parse_actions_request')

