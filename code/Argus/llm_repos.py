from fileinput import filename
import json
import pathlib
import time
from xmlrpc.client import Boolean
import argus_components
import base64
import yaml
from argus_components.workflow import Workflow, GHWorkflow
import datetime
import os

import argus_components



def read_yml_content(filename):

    folder = pathlib.Path(r"\build\configuration_files\chatgpt-3.5-turbo")
    file_path = folder / filename

    print(file_path)

    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    
    return content


def read_config_files(name, filepath):

    return_obj = {}

    name = name.replace('.yml', '')

    try:

        workflow = GHWorkflow(filepath, '')
        jobs = workflow.jobs

    except:
        print(filepath)
        jobs = []
        

    return_obj['id'] = name

    return_obj['jobs'] = []

    for job in jobs:
        
        job_obj = {}

        job_obj['name'] = job.name

        job_obj['steps'] = []

        for step in job.steps:

            step_run = step.run
            job_obj['steps'].append(step_run)
        
        return_obj['jobs'].append(job_obj)

    return return_obj


def write_to_local_files(content, file_path):
    with open(file_path, "a+") as f:
        f.write(f"{content}\n")


def begin_parse_yml():

    # folder = r'\build\configuration_files\chatgpt-3.5-turbo'
    # folder = r'D:\Code\LLM\exported_files\data_begin\build\configuration_files\gpt-4o-mini'

    # folder = r'\build\configuration_files\llama-3.1-8b-instruct'

    folder = r'\build\configuration_files\llama-3.1-sonar-small-128k-chat'

    for dirpath, dirnames, filenames in os.walk(folder):

        for filename in filenames:

            file_path = os.path.join(dirpath, filename)
            
            # content = read_yml_content(file_path)
            # print(file_path)

            return_obj = read_config_files(filename, file_path)

            jobs = return_obj['jobs']

            if len(jobs) > 0:

                write_to_local_files(json.dumps(return_obj), r'\build\llama-3.1-sonar-small-128k-chat\top_build_trans_sonar_output_parse.json')


# content = read_yml_content('535_0.yml')

# folder = pathlib.Path(r"\build\configuration_files\chatgpt-3.5-turbo")
# file_path = folder / '10043816_0.yml'

# obj = read_config_files('10043816_0.yml', file_path)

# print(obj)

# begin_parse_yml()

def begin_argus(folder, filename):

    with open(f'{folder}/{filename}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    # with open(f'/build/top_build_trans_4o-mini_output_parse.json', encoding='utf-8') as f:
    #     all_lines = f.readlines()
    #     f.close()
    
    total = 0
    for line in all_lines:
        obj = json.loads(line.rstrip())

        total += 1

        if total < 16678:
            continue

        id = obj['id']

        print(f'{total} begin...')
        
        try:
            repo = argus_components.Repo(id, {})
            repo.run()
            repo.save_report_to_file()

        except:
            write_to_local_files(json.dumps(obj), f'{folder}/{filename}_argus_error.json')


folder = r'\build\chatgpt-4o-mini'
# folder = r'\build\chatgpt-3.5-turbo'
# folder = r'\build\llama-3.1-8b-instruct'
# folder = r'\build\llama-3.1-sonar-small-128k-chat'


begin_argus(folder, 'top_build_output_parse')

# repo = argus_components.Repo('10004508_0', {})
# repo.run()
# repo.save_report_to_file()


