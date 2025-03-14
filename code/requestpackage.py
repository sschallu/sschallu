import WriteData

import json

import os

import requests

import time


def init_request_dic():

    with open(f'/packages_request_status.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = {}

    for line in all_lines:
        
        obj = json.loads(line.rstrip())
        url = obj['url']
        status_code = obj['status_code']

        dic[url] = status_code
    
    return dic


# for question1 and question2 and question7
def request_packages_question1():

    with open(f'/gpt-3.5-turbo/question7/question7_parse.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = init_request_dic()

    python = 'https://pypi.org/project/'
    nodejs = 'https://registry.npmjs.org/'
    php = 'https://packagist.org/packages/'
    ruby = 'https://rubygems.org/gems/'
    perl = 'https://metacpan.org/pod/'

    total = 0

    for line in all_lines:

        obj = json.loads(line.rstrip())

        output_list = obj['output']

        http_list = obj['http']

        libraries = obj['libraries']

        new_output = []

        new_http = []

        new_libraries = []

        for output in output_list:
            
            total += 1

            if isinstance(output, list):
                
                label = output[0]

                package_name = output[1]

                if label == 'cpanm' or label == 'cpan':
                    request_url = f'{perl}{package_name}'

                elif label == 'pip install':
                    request_url = f'{python}{package_name.lower()}'
                
                elif label == 'composer require':
                    request_url = f'{php}{package_name.lower()}'
                
                elif label == 'gem install':
                    request_url = f'{ruby}{package_name.lower()}'
                
                else:
                    request_url = f'{nodejs}{package_name.lower()}'
                

                if request_url in dic.keys():

                    new_output.append([request_url, dic[request_url]])

                    print(f'{total}_already: {request_url}: {dic[request_url]}')

                else:

                    try:

                        response = requests.get(request_url)

                        time.sleep(0.5)

                        status_code = response.status_code

                        dic[request_url] = status_code

                        request_obj = {}

                        request_obj['url'] = request_url
                        request_obj['status_code'] = status_code
                        WriteData.write_in_path(json.dumps(request_obj), '/packages_request_status')

                        new_output.append([request_url, status_code])

                        print(f'{total}: {request_url}: {status_code}')
                    
                    except:
                        new_output.append([request_url, 'exception'])
                        print(f'{total}: {request_url}: exception...')

            else:

                request_url = output
                
                if request_url in dic.keys():
                    
                    new_output.append([request_url, dic[request_url]])

                    print(f'{total}_already: {request_url}: {dic[request_url]}')
                
                else:

                    try:

                        response = requests.get(request_url)

                        time.sleep(0.5)

                        status_code = response.status_code

                        dic[request_url] = status_code

                        request_obj = {}

                        request_obj['url'] = request_url
                        request_obj['status_code'] = status_code
                        WriteData.write_in_path(json.dumps(request_obj), '/packages_request_status')

                        new_output.append([request_url, status_code])

                        print(f'{total}: {request_url}: {status_code}')
                    
                    except:
                        new_output.append([request_url, 'exception'])
                        print(f'{total}: {request_url}: exception...')


        for http in http_list:

            total += 1

            # print(http)
            
            request_url = http
                
            if request_url in dic.keys():
                    
                new_http.append([request_url, dic[request_url]])

                print(f'{total}_already: {request_url}: {dic[request_url]}')
                
            else:

                try:

                    response = requests.get(request_url)

                    time.sleep(0.5)

                    status_code = response.status_code

                    dic[request_url] = status_code

                    request_obj = {}

                    request_obj['url'] = request_url
                    request_obj['status_code'] = status_code
                    WriteData.write_in_path(json.dumps(request_obj), '/packages_request_status')

                    new_http.append([request_url, status_code])

                    print(f'{total}: {request_url}: {status_code}')
                    
                except:
                    new_http.append([request_url, 'exception'])
                    print(f'{total}: {request_url}: exception...')

        
        for lib in libraries:

            total += 1

            # print(http)
            
            request_url = lib
                
            if request_url in dic.keys():
                    
                new_libraries.append([request_url, dic[request_url]])

                print(f'{total}_already: {request_url}: {dic[request_url]}')
                
            else:

                try:

                    response = requests.get(request_url)

                    time.sleep(0.5)

                    status_code = response.status_code

                    dic[request_url] = status_code

                    request_obj = {}

                    request_obj['url'] = request_url
                    request_obj['status_code'] = status_code
                    WriteData.write_in_path(json.dumps(request_obj), '/packages_request_status')

                    new_libraries.append([request_url, status_code])

                    print(f'{total}: {request_url}: {status_code}')
                    
                except:
                    new_libraries.append([request_url, 'exception'])
                    print(f'{total}: {request_url}: exception...')


        obj['output'] = new_output
        obj['http'] = new_http
        obj['libraries'] = new_libraries

        WriteData.write_in_path(json.dumps(obj), '/gpt-3.5-turbo/question7/question7_parse_request')
    
    print(total)






def request_packages_question4():

    with open(f'/question4/4o-mini/question4_parse_tags_identification_filter.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    dic = init_request_dic()

    python = 'https://pypi.org/project/'
    nodejs = 'https://registry.npmjs.org/'
    php = 'https://packagist.org/packages/'
    ruby = 'https://rubygems.org/gems/'
    perl = 'https://metacpan.org/pod/'

    total = 0

    for line in all_lines:

        obj = json.loads(line.rstrip())

        output_list = obj['output']

        http_list = obj['http']

        link_list = obj['list']

        new_output = []

        new_http = []

        new_link = []

        for output in output_list:
            
            total += 1

            if isinstance(output, list):
                
                label = output[0]

                package_name = output[1]

                if label == 'cpanm' or label == 'cpan':
                    request_url = f'{perl}{package_name}'

                elif label == 'pip install':
                    request_url = f'{python}{package_name.lower()}'
                
                elif label == 'composer':
                    request_url = f'{php}{package_name.lower()}'
                
                elif label == 'gem install':
                    request_url = f'{ruby}{package_name.lower()}'
                
                else:
                    request_url = f'{nodejs}{package_name.lower()}'
                

                if request_url in dic.keys():

                    new_output.append([request_url, dic[request_url]])

                    print(f'{total}_already: {request_url}: {dic[request_url]}')

                else:

                    try:

                        response = requests.get(request_url)

                        time.sleep(0.5)

                        status_code = response.status_code

                        dic[request_url] = status_code

                        request_obj = {}

                        request_obj['url'] = request_url
                        request_obj['status_code'] = status_code
                        WriteData.write_in_path(json.dumps(request_obj), '/packages_request_status')

                        new_output.append([request_url, status_code])

                        print(f'{total}: {request_url}: {status_code}')
                    
                    except:
                        new_output.append([request_url, 'exception'])
                        print(f'{total}: {request_url}: exception...')

            else:

                request_url = output
                
                if request_url in dic.keys():
                    
                    new_output.append([request_url, dic[request_url]])

                    print(f'{total}_already: {request_url}: {dic[request_url]}')
                
                else:

                    try:

                        response = requests.get(request_url)

                        time.sleep(0.5)

                        status_code = response.status_code

                        dic[request_url] = status_code

                        request_obj = {}

                        request_obj['url'] = request_url
                        request_obj['status_code'] = status_code
                        WriteData.write_in_path(json.dumps(request_obj), '/packages_request_status')

                        new_output.append([request_url, status_code])

                        print(f'{total}: {request_url}: {status_code}')
                    
                    except:
                        new_output.append([request_url, 'exception'])
                        print(f'{total}: {request_url}: exception...')


        for http in http_list:

            total += 1

            print(http)
            
            request_url = http
                
            if request_url in dic.keys():
                    
                new_http.append([request_url, dic[request_url]])

                print(f'{total}_already: {request_url}: {dic[request_url]}')
                
            else:

                try:

                    response = requests.get(request_url)

                    time.sleep(0.5)

                    status_code = response.status_code

                    dic[request_url] = status_code

                    request_obj = {}

                    request_obj['url'] = request_url
                    request_obj['status_code'] = status_code
                    WriteData.write_in_path(json.dumps(request_obj), '/packages_request_status')

                    new_http.append([request_url, status_code])

                    print(f'{total}: {request_url}: {status_code}')
                    
                except:
                    new_http.append([request_url, 'exception'])
                    print(f'{total}: {request_url}: exception...')



        label = obj['label']

        for link in link_list:

            total += 1

            if 'http' in link:
                request_url = link
            
            elif link.startswith('github.com'):
                request_url = f'https://{link}'

            else:
                if label == 'python':
                    request_url = f'{python}{link.lower()}'

                elif label == 'php':
                    request_url = f'{php}{link.lower()}'
                
                elif label == 'ruby':
                    request_url = f'{ruby}{link.lower()}'
                
                elif label == 'perl':
                    request_url = f'{perl}{link}'
                
                else:
                    request_url = f'{nodejs}{link.lower()}'

            
            if request_url in dic.keys():
                    
                new_link.append([request_url, dic[request_url]])

                print(f'{total}_already: {request_url}: {dic[request_url]}')
                
            else:

                try:

                    response = requests.get(request_url)

                    time.sleep(0.5)

                    status_code = response.status_code

                    dic[request_url] = status_code

                    request_obj = {}

                    request_obj['url'] = request_url
                    request_obj['status_code'] = status_code
                    WriteData.write_in_path(json.dumps(request_obj), '/packages_request_status')

                    new_link.append([request_url, status_code])

                    print(f'{total}: {request_url}: {status_code}')
                    
                except:
                    new_link.append([request_url, 'exception'])
                    print(f'{total}: {request_url}: exception...')



        new_obj = {}
        new_obj['custom_id'] = obj['custom_id']
        new_obj['title'] = obj['title']
        new_obj['output'] = new_output
        new_obj['http'] = new_http
        new_obj['list'] = new_link

        WriteData.write_in_path(json.dumps(new_obj), '/question4/4o-mini/question4_parse_tags_identification_filter_request')
    
    print(total)


# request_packages_question4()


# request_packages_question1()


def extract_404():

    with open(f'/question1/4o-mini/question1_parse_request.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    total = 0
    for line in all_lines:

        obj = json.loads(line.rstrip())

        custom_id = obj['custom_id']
        output_list = obj['output']
        http_list = obj['http']
        list_list = obj['list']

        new_output = []
        new_http = []
        new_list = []


        if len(output_list) > 0 or len(http_list) > 0 or len(list_list) > 0:
            total += 1

        if len(output_list) > 0:
            
            for output in output_list:
                status_code = output[1]
                if status_code == 404:
                    new_output.append(output)


        if len(http_list) > 0:
            
            for http in http_list:
                status_code = http[1]
                if status_code == 404:
                    new_http.append(http)
        
        if len(list_list) > 0:

            for li in list_list:
                status_code = li[1]
                if status_code == 404:
                    new_list.append(li)
        
        if len(new_output) > 0 or len(new_http) > 0 or len(new_list) > 0:
            
            obj['output'] = new_output
            obj['http'] = new_http
            obj['list'] = new_list

            # WriteData.write_in_path(json.dumps(obj), '/question4/question4_parse_tags_identification_filter_request_404')

    print(total)


# extract_404()



request_packages_question1()


