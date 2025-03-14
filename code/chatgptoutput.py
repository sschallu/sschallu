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

    with open(f'/gpt-3.5-turbo/top_60000_output.jsonl', encoding='utf-8') as f:
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
        # if custom_id.endswith('_2'):
        #     # WriteData.write_in_html(soup, f'/question1/4o-mini/{custom_id}')

        #     for a in soup.findAll('a'):
        #         if a.get('href') is not None:
        #             href = a.get('href')

        #             if href.startswith('http'):
        #                 json_obj['http'].append(href.replace('\n', ''))

        #     WriteData.write_in_path(json.dumps(json_obj), '/gpt-3.5-turbo/question2/question2')


        # _5 and _6 
        # if custom_id.endswith('_6'):
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
            
        #     WriteData.write_in_path(json.dumps(json_obj), '/gpt-3.5-turbo/question6/question6')


        # if custom_id.endswith('_3'):

        #     content_array = content.split('\n')
        #     filtered_array = list(filter(lambda x: x.strip(), content_array))
        #     json_obj['content'] = filtered_array

        #     for a in soup.findAll('a'):
        #         if a.get('href') is not None:
        #             href = a.get('href')

        #             if href.startswith('http'):
        #                 json_obj['http'].append(href.replace('\n', ''))

        #     WriteData.write_in_path(json.dumps(json_obj), '/gpt-3.5-turbo/question3/question3')
        
        



def get_custom_id():

    with open(f'/top_60000.jsonl', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    dictionary = {}

    for line in all_lines:
        obj = json.loads(line.rstrip())

        custom_id = obj['custom_id']

        content = obj['body']['messages'][1]['content']

        dictionary[custom_id] = content
    
    return dictionary


# parse_output()


#   question4 - step1
def question4_parse():

    with open(f'/question4/4o-mini/question4.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:

        obj = json.loads(line.rstrip())

        list = obj['list']

        new_list = []
        for item in list:
            item = item.replace('\n', '')

            if ': ' in item:
                sub_array = item.split(': ')
                print(sub_array)
                new_list.append(sub_array)
            elif ' - ' in item:
                sub_array = item.split(' - ')
                print(sub_array)
                new_list.append(sub_array)
            else:
                print(item)
                new_list.append(item)      

        obj['list'] = new_list
        WriteData.write_in_path(json.dumps(obj), '/question4/4o-mini/question4_parse')        


# question4_parse()


def tag_collections():

    # languages = ['javascript', 'python', 'java', 'c#', 'php', 'ruby', 'typescript', 'scala', 'perl', 'go', 'rust', 'kotlin', 'node.js']

    dic = {}
    with open(f'/top_10000.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    # for language in languages:
    #     dic[language] = []
    
    # dic['rest'] = []

    for line in all_lines:

        obj = json.loads(line.rstrip())

        id = obj['id']

        dic[f'{id}'] = obj['tags']

        # tags = obj['tags'].split('|')
        # print(tags)

        # flag = False
        # flag_name = ''
        # for tag in tags:
        #     print(tag)
        #     if tag in languages:
        #         flag = True
        #         flag_name = tag
        #         break
        
        # if flag is True:
        #     dic[flag_name].append(f'{id}')
        # else:
        #     dic['rest'].append(f'{id}')

    return dic


# dic = tag_collections()

# print(len(dic.keys()))


#   question4 - step2
def get_tag():

    with open(f'/question4/4o-mini/question4_parse.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    dic = tag_collections()

    for line in all_lines:
        
        obj = json.loads(line.rstrip())

        custom_id = obj['custom_id']

        id = custom_id.replace('_4', '')

        new_obj = {}
        new_obj['custom_id'] = custom_id
        new_obj['title'] = obj['title']
        new_obj['tags'] = dic[id]
        new_obj['output'] = obj['output']
        new_obj['http'] = obj['http']
        new_obj['list'] = obj['list']

        WriteData.write_in_path(json.dumps(new_obj), '/question4/4o-mini/question4_parse_tags')


# get_tag()


#   question4 - step3
def tag_identification():

    languages = ['javascript', 'python', 'php', 'ruby', 'typescript', 'perl', 'node.js']

    with open(f'/question4/4o-mini/question4_parse_tags.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
  
    
    for line in all_lines:

        obj = json.loads(line.rstrip())

        new_obj = {}
        new_obj['custom_id'] = obj['custom_id']
        new_obj['title'] = obj['title']

        custom_id = obj['custom_id']

        title = obj['title'].lower().replace('?', '').replace('nodejs', 'node.js')

        tags = obj['tags'].split('|')
        # print(tags)

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
        
        new_obj['tags'] = obj['tags']
        new_obj['output'] = obj['output']
        new_obj['http'] = obj['http']
        new_obj['list'] = obj['list']

        WriteData.write_in_path(json.dumps(new_obj), '/question4/4o-mini/question4_parse_tags_identification')

            
# tag_identification()



def is_valid_regex(pattern):
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False


#   question4 - step4
def deal_question4_output():

    pattern = r'^(?:@[a-zA-Z0-9_-]+/)?[a-zA-Z0-9_-]+(/[a-zA-Z0-9_-]+)*(\.[a-zA-Z0-9_-]+)*$'

    with open(f'/question4/4o-mini/question4_parse_tags_identification.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    install_array = ['npm install', 'pip install', 'composer', 'gem install', 'cpanm', 'cpan']

    keywords = ['require', 'xxx', 'npm', 'COPY', 'Test', 'Run', 'Install', 'CMD', 'sh', 'python', '$', 'm', 'install', 'pip', 'requirements.txt', 'your_project_name', 'example', 'as', 'an', 'and', 'tar.gz']

    skip_keywords = ['Link', 'Vue.js', 'Description', 'Website', 'Documentation', 'npm-run-all', 'GitHub', 'click', 'Installation', 'Benchmark', 'AnyEventWebSocketServer', 'AnyEventWebSocketClient', 'ProtocolWebSocket', 'pre-commit', 'S4144', 'S4487', 'S5698', 'S4784', 'S4830', 'Repository', 'socket.io', 'npm', 'Protocol', 'Perl', 'Callable', 'Runnable', 'AnyEvent', 'Directory', 'file_include', 'Package', 'Good', 'Bad', 'Ugly', 'Composer', 'npm-run', 'npm-download', 'Problem', 'Iteration', 'Enumerable', 'Iterator', 'os']

    for line in all_lines:

        obj = json.loads(line.rstrip())

        custom_id = obj['custom_id']

        output_list = obj['list']

        new_output = []

        for output in output_list:
            
            if isinstance(output, list):
                for sub_output in output:
                    sub_output = sub_output.replace('"', '')

                    match = re.match(pattern, sub_output)

                    if not match and 'http' not in sub_output and 'github' not in sub_output:

                        # if len(sub_output) < 30 and 'package' in sub_output:
                        # if len(sub_output) < 30:
                        #     print(sub_output)
                            # package_name = sub_output.split(' ')[0]

                            # if package_name != 'npm':
                            #     # print(package_name)
                            #     new_output.append(package_name)
                            
                        # else:
                        #     continue
                        continue

                    else:

                        if 'http' in sub_output:
                            http_pattern = r'https?://[^\s/$.?#].[^\s]*'
    
                            links = re.findall(http_pattern, sub_output)
                            for link in links:
                                link = link.replace(')', '').rstrip('.')
                                # print(link)
                                new_output.append(link)

                        elif 'github.com' in sub_output:
                            github_pattern = r'github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+'
                            links = re.findall(github_pattern, sub_output)

                            for link in links:
                                # print(link)
                                new_output.append(link)

                        else:
                            if len(sub_output) > 30:
                                continue

                            if sub_output not in skip_keywords and not sub_output[0].isdigit() and not sub_output.endswith('.py') and not sub_output.startswith('com.') and not sub_output.startswith('org.'):
                                # print(sub_output)
                                new_output.append(sub_output)
                # break

            else:
                output = output.replace(':', '')

                if len(output) <= 50:
                    match = re.match(pattern, output)

                    if not match and 'http' not in output and 'github' not in output:
                        continue
                    else:
                        if 'http' in output:
                            http_pattern = r'https?://[^\s/$.?#].[^\s]*'
    
                            links = re.findall(http_pattern, output)
                            for link in links:
                                # print(link)
                                new_output.append(link)

                        elif 'github.com' in output:
                            github_pattern = r'github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+'
                            links = re.findall(github_pattern, output)

                            for link in links:
                                # print(link)
                                new_output.append(link)

                        else:
                            if not output.startswith('com.') and not output.endswith('.py') and not output.startswith('org.') and output not in skip_keywords and not output.startswith('net.') and not output.startswith('IO') and not output.startswith('Net') and not output.startswith('Mojo') and not output.startswith('java.'):
                                # print(output)
                                new_output.append(output)
                        # print(f'{custom_id}: {output}')


        first_output = obj['output']
        new_first_output = []

        if len(output) > 0:
            for output in first_output:

                sub_output = output.split('\n')

                for sub in sub_output:
                    
                    if '<script ' in sub:
                        links = re.findall(http_pattern, sub)

                        for link in links:
                            link = link.replace('"', '').replace('></script>', '').replace("><\/script>');", '')
                            new_first_output.append(link)
                            print(link.replace('"', '').replace('></script>', ''))
                    
                    if '<link ' in sub:
                        links = re.findall(http_pattern, sub)

                        for link in links:
                            link = link.replace("'", "").replace('"', '').replace('>', '')
                            new_first_output.append(link)
                            print(link)

                    for install in install_array:

                        if install in sub and not sub.startswith('//') and not sub.startswith('#'):

                            output_rest = sub.split(install)[1].strip()

                            output_rest_array = output_rest.split(' ')

                            for rest in output_rest_array:

                                if rest in keywords:
                                    continue

                                if rest.startswith('--') or rest.startswith('-'):
                                    continue
                                    
                                match = re.match(pattern, rest)

                                if match:
                                    new_first_output.append([install, rest])
                                    print(f'{custom_id}: {install}: {rest}')

        new_obj = {}
        new_obj['custom_id'] = obj['custom_id']
        new_obj['title'] = obj['title']
        try:
            new_obj['label'] = obj['label']
        except:
            print(obj['custom_id'])
            break
        new_obj['tags'] = obj['tags']
        new_obj['output'] = new_first_output
        new_obj['http'] = obj['http']
        new_obj['list'] = list(set(new_output))

        WriteData.write_in_path(json.dumps(new_obj), '/question4/4o-mini/question4_parse_tags_identification_filter')
        

# deal_question4_output()


def request_packages():

    with open(f'/description/question2_result_parse_tags_identification_filter.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = {}

    python = 'https://pypi.org/project/'
    nodejs = 'https://registry.npmjs.org/'
    php = 'https://packagist.org/packages/'
    ruby = 'https://rubygems.org/gems/'
    perl = 'https://metacpan.org/pod/'

    label_array = []

    total = 0

    for line in all_lines:

        obj = json.loads(line.rstrip())

        label = obj['label']

        output_list = obj['output']

        new_output = []

        for output in output_list:
            
            total += 1

            output = output.replace(')', '')

            if 'http' in output:
                request_url = output

            else:
                if label == 'python':
                    request_url = f'{python}{output.lower()}'

                elif label == 'php':
                    request_url = f'{php}{output.lower()}'
                
                elif label == 'ruby':
                    request_url = f'{ruby}{output.lower()}'
                
                elif label == 'perl':
                    request_url = f'{perl}{output}'
                
                else:
                    request_url = f'{nodejs}{output.lower()}'
            
            if request_url in dic.keys():

                new_output.append([request_url, dic[request_url]])

                print(f'{total}_already: {request_url}: {dic[request_url]}')
            else:

                try:

                    response = requests.get(request_url)

                    time.sleep(0.5)

                    status_code = response.status_code

                    dic[request_url] = status_code

                    new_output.append([request_url, status_code])

                    print(f'{total}: {request_url}: {status_code}')
                
                except:
                    new_output.append([request_url, 'exception'])
                    print(f'{total}: {request_url}: exception...')

        new_obj = {}
        new_obj['custom_id'] = obj['custom_id']
        new_obj['title'] = obj['title']
        new_obj['label'] = obj['label']
        new_obj['tags'] = obj['tags']
        new_obj['output'] = new_output

        WriteData.write_in_path(json.dumps(new_obj), '/description/question2_result_parse_tags_identification_filter_request')

                    

# request_packages()


def deal_with_429():

    with open(f'/description/question2_result_parse_tags_identification_filter_request.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = {}
    total = 0

    for line in all_lines:

        obj = json.loads(line.rstrip())

        output_list = obj['output']

        new_output = []

        for output in output_list:
            request_url = output[0]

            status_code = output[1]

            if status_code == 429:

                if request_url not in dic.keys():

                    time.sleep(2)

                    response = requests.get(request_url)

                    new_status_code = response.status_code

                    dic[request_url] = new_status_code
                    total += 1
                    print(f'{request_url}: {new_status_code}')
                
                else:
                    new_status_code = dic[request_url]
                
                new_output.append([request_url, new_status_code])
            
            else:
                new_output.append(output)
        
        obj['output'] = new_output
        WriteData.write_in_path(json.dumps(obj), '/description/question2_result_parse_tags_identification_filter_request_429')

    
    print(total)

# deal_with_429()


# extract the information from question1 and question2
def deal_question1_result():

    pattern = r'^(?:@[a-zA-Z0-9_-]+/)?[a-zA-Z0-9_-]+(/[a-zA-Z0-9_-]+)*(\.[a-zA-Z0-9_-]+)*$'
    http_pattern = r'https?://[^\s/$.?#].[^\s]*'

    with open(f'/question2/4o-mini/question2.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    install_array = ['npm install', 'pip install', 'composer', 'gem install', 'cpanm', 'cpan']

    keywords = ['require', 'xxx', 'npm', 'COPY', 'Test', 'Run', 'Install', 'CMD', 'sh', 'python', '$', 'm', 'install', 'pip', 'requirements.txt', 'your_project_name', 'example', 'as', 'an', 'and', 'tar.gz']

    total = 0
    for line in all_lines:

        obj = json.loads(line.rstrip())

        custom_id = obj['custom_id']

        output_list = obj['output']

        new_output = []
        
        for output in output_list:

            sub_output = output.split('\n')

            for sub in sub_output:
                
                if '<script ' in sub:
                    total += 1

                    links = re.findall(http_pattern, sub)

                    for link in links:
                        link = link.replace('"', '').replace('></script>', '')
                        new_output.append(link)
                        print(link.replace('"', '').replace('></script>', ''))
                
                if '<link ' in sub:
                    total += 1

                    links = re.findall(http_pattern, sub)

                    for link in links:
                        link = link.replace("'", "").replace('"', '').replace('>', '')
                        new_output.append(link)
                        print(link)

                for install in install_array:

                    if install in sub and not sub.startswith('//') and not sub.startswith('#'):

                        output_rest = sub.split(install)[1].strip()
                        total += 1

                        output_rest_array = output_rest.split(' ')

                        for rest in output_rest_array:

                            if rest in keywords:
                                continue

                            if rest.startswith('--') or rest.startswith('-'):
                                continue
                                
                            match = re.match(pattern, rest)

                            if match:
                                new_output.append([install, rest])
                                print(f'{custom_id}: {install}: {rest}')
        
        
        new_obj = {}
        new_obj['custom_id'] = custom_id
        new_obj['title'] = obj['title']
        new_obj['output'] = new_output
        new_obj['http'] = obj['http']
        new_obj['list'] = obj['list']

        WriteData.write_in_path(json.dumps(new_obj), '/question2/4o-mini/question2_parse')
                
    print(total)


# deal_question1_result()





def get_404():

    # with open(f'/description/question1_result_parse_request.json', encoding='utf-8') as f:
    #     all_lines = f.readlines()
    #     f.close()

    with open(f'/description/question2_result_parse_tags_identification_filter_request.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:
        obj = json.loads(line.rstrip())

        output_list = obj['output']

        for output in output_list:

            link = output[0]

            status_code = output[1]

            if status_code == 404:
                new_obj = {}
                new_obj['custom_id'] = obj['custom_id']
                new_obj['list'] = link
                new_obj['status_code'] = status_code

                print(f'{link}: {status_code}')

                WriteData.write_in_path(json.dumps(new_obj), '/description/question2_result_parse_tags_identification_filter_request_404')

# get_404()


def deal_question3_result():

    pattern = r'^(?:@[a-zA-Z0-9_-]+/)?[a-zA-Z0-9_-]+(/[a-zA-Z0-9_-]+)*(\.[a-zA-Z0-9_-]+)*$'
    http_pattern = r'https?://[^\s/$.?#].[^\s]*'

    install_array = ['npm install', 'pip install', 'composer require', 'gem install', 'cpanm ', 'cpan ']

    skip_keywords = ['require', '.', 'run:', '|', 'xxx', 'npm', 'COPY', 'Test', 'Run', 'RUN', 'Install', 'CMD', 'sh', 'python', '$', 'm', 'install', 'pip', 'requirements.txt', 'your_project_name', 'example', 'as', 'an', 'and', 'tar.gz']

    with open(f'/gpt-3.5-turbo/question3/question3.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    total = 0
    for line in all_lines:

        obj = json.loads(line.rstrip())

        custom_id = obj['custom_id']

        content = obj['content']

        output_list = obj['output']

        new_output = []
        
        for output in output_list:

            sub_output = output.split('\n')

            for sub in sub_output:
                
                if '<script ' in sub:
                    
                    links = re.findall(http_pattern, sub)

                    for link in links:
                        link = link.replace('"', '').replace('></script>', '')
                        new_output.append(link)
                        print(link)
                
                if '<link ' in sub:
                    links = re.findall(http_pattern, sub)

                    for link in links:
                        if 'example.com' in link:
                            continue

                        link = link.replace("'", "").replace('"', '').replace('>', '')
                        new_output.append(link)
                        print(link)

                for install in install_array:

                    if install in sub and not sub.startswith('#'):
                        total += 1
                        
                        sub = sub.replace('//', '').replace('cpan install', 'cpan').strip()

                        sub_array = sub.split(f'{install.strip()} ')

                        filtered_array = list(filter(lambda x: x.strip(), sub_array))

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

                            if target in skip_keywords:
                                continue
                        
                            if '<' in target or 'username' in target or '>' in target or 'package-name' in target or 'package_name' in target:
                                continue

                            if '==' in target:
                                target = target.split('==')[0]
                            
                            if '===' in target:
                                target = target.split('===')[0]
                            
                            if '@' in target:
                                target = target.split('@')[0]
                            
                            if 'github.com' in target and 'username' not in target.lower():
                                temp = target.split('github.com')[1]
                                new_output.append(f'https://github.com/{temp}')
                                
                            match = re.match(pattern, target)
                            if match:
                                new_output.append([install.strip(), target])
            
        flag = False
        if len(content) > 2:
            package = content[1]
            license = content[2]
            if 'package' in package.lower() and 'license' in license.lower():
                flag = True


        if len(new_output) > 0 or len(obj['http']) > 0 or len(obj['list']) > 0 or flag is True:
            new_obj = {}
            new_obj['custom_id'] = custom_id
            new_obj['title'] = obj['title']
            new_obj['output'] = new_output
            new_obj['content'] = obj['content']
            new_obj['http'] = obj['http']
            new_obj['list'] = obj['list']

            WriteData.write_in_path(json.dumps(new_obj), '/gpt-3.5-turbo/question3/question3_package')
    
    print(total)
    

# deal_question3_result()



# for the license, I need to think differently
# I need a license array
# I want to collect the licenses metioned in the answers
def deal_question3_license():

    http_pattern = r'https?://[^\s/$.?#].[^\s]*'
    pattern = r'^(?:@[a-zA-Z0-9_-]+/)?[a-zA-Z0-9_-]+(/[a-zA-Z0-9_-]+)*(\.[a-zA-Z0-9_-]+)*$'

    license_array = ['MIT']

    with open(f'/gpt-3.5-turbo/question3/question3_package.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    for line in all_lines:

        json_obj = json.loads(line.rstrip())

        custom_id = json_obj['custom_id']
        content = json_obj['content']
        output = json_obj['output']

        http = json_obj['http']
        

        if len(output) <= 0 and len(http) <= 0:
            
            package_info = content[1].replace('*', '').replace('`', '').strip()
            license_info = content[2].replace('*', '').replace('`', '').strip()

            if '::' in package_info:
                package_info = package_info.replace('::', '|')

            if 'https:' in package_info:
                links = re.findall(http_pattern, package_info)
                # print(links)

            else:
                print(f'{custom_id}: {package_info}')
                    

            
            # package_info_array = package_info.split(':')

            # if len(package_info_array) <= 1:
            #     continue
            # print(package_info_array)
            

            total += 1



        # for index in range(0, len(content)):
        #     item = content[index]

        #     if 'license:' in item.lower() and index != 0:
        #         total += 1
        #         print(f'{custom_id}, {index-1}: {content[index-1]}')
        #         print(f'{custom_id}, {index}: {item}')

            # if 'license:' not in item.lower() and 'license' in item.lower():
            #     total += 1
            #     print(f'{custom_id}: {item}')

    print(total)


# deal_question3_license()


    