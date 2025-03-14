import WriteData
import json
import re
import ast


def read_files(destination, suffix):

    with open(f'{destination}.{suffix}', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    return all_lines


def get_github_account(folder, question, filename):
    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    unique_github_account = {}

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        link = json_obj['link'].replace('https://github.com/', '')

        account = link.split('/')[0]

        if account not in unique_github_account:
            unique_github_account[account] = 1
        else:
            unique_github_account[account] += 1

    sorted_dict = dict(sorted(unique_github_account.items(), key=lambda item: item[1], reverse=True))
    print(len(sorted_dict.keys()))

    hijacking_account = []
    destination2 = f'{folder}/{question}/{filename}_redirected_hijacking'
    all_lines2 = read_files(destination2, 'json')
    for line2 in all_lines2:
        new_obj = json.loads(line2.rstrip())

        link = new_obj['link'].replace('https://github.com/', '')
        account = link.split('/')[0]
        if account not in hijacking_account:
            hijacking_account.append(account)
    
    print(len(hijacking_account))

    print(len(hijacking_account) / len(sorted_dict) * 100)

    # for account in sorted_dict.keys():
    #     if account in hijacking_account:
    #         print(f'{account}: {sorted_dict[account]}')


def read_package_count(folder, question, filename):
    destination = f'{folder}/{question}/{filename}'

    all_lines = read_files(destination, 'json')

    print(filename)

    depre = 0

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        deprecated = json_obj['deprecated']

        # print(deprecated)

        if deprecated is True:
            depre += 1

    print(depre)
    print(len(all_lines))

    print(depre / len(all_lines) * 100)


folder = r'/gpt-4o-mini'
# folder = r'/gpt-3.5-turbo'
# folder = r'/llama-3.1-instruct'
# folder = r'/llama-128k-sonar'
question = 'question1'
filename = 'package_total_nodejs_request'
# filename = 'package_total_nodejs_new_request'

# get_github_account(folder, question, filename)

read_package_count(folder, question, filename)
