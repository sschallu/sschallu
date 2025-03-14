import os

import Log
import json

def checkDir(mypath):
    if not os.path.exists(mypath):
        os.makedirs(mypath)

def writeIn(jsonData, path):
    try:

        Log.Logger(f'{path}.json', level='info').logger.info(str(jsonData))

    except Exception as msg:
        Log.Logger('error.log', level='error', fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s').logger.error(msg)


def write_in_path(json_data, path):

    try:

        Log.Logger(f'{path}.json', level='info').logger.info(str(json_data))

    except Exception as msg:
        Log.Logger('error.log', level='error', fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s').logger.error(msg)


def write_in_html(json_data, path):

    try:

        Log.Logger(f'{path}.html', level='info').logger.info(str(json_data))

    except Exception as msg:
        Log.Logger('error.log', level='error', fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s').logger.error(msg)



def write_in_yml(json_data, path):

    with open(f'{path}.yml', 'w', encoding='utf-8') as f:
        f.write(json_data)


def write_in_jsonl(json_data, path):

    try:

        Log.Logger(f'{path}.jsonl', level='info').logger.info(str(json_data))

    except Exception as msg:
        Log.Logger('error.log', level='error', fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s').logger.error(msg)


    # try:

    #     Log.Logger(f'{path}.yml', level='info').logger.info(str(json_data))

    # except Exception as msg:
    #     Log.Logger('error.log', level='error', fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s').logger.error(msg)
