#!../venv/bin/python
import json
import pandas as pd
# from nltk.corpus import words


def sanitizeString(str):
    """
    :param str: string input (expected to contain
    punctuation)
    :return: string with punctuation stripped
    """
    i = 0
    for cahr in str:
        if not cahr.isalpha():
            break
        else:
            i += 1
    sub = str[0:i]
    return sub.lower()


def loadJSONFile(f):
    """
    :param f: the data file (.json) containing
    the list of bias types

    :return: the full json object
    """
    df = open(f)
    df = json.load(df)
    return df


def getBiasTypes(df):
    """
    :param df: the json object

    :return: a list of the bias types
    """
    biasTypes = []
    biasTypeJSON = df['data']['intersentence']
    for item in biasTypeJSON:
        bt = item['bias_type']
        if bt not in biasTypes:
            biasTypes.append(bt)
    return biasTypes


def getBiasTypeMap(df):
    """
    :param df: the json object

    :return: a map of key: race types and
    value: list of all targets for that race
    type
    """


    addList = []
    # for ex in extras:
    #     add = sanitizeString(ex[0])
    #     addList.append(ex)
    bt = getBiasTypes(df)
    btMap = {}
    for item in bt:
        btMap[item] = []
    # extra words taken from:
    # https://github.com/XuhuiZhou/Toxic_Debias/blob/main/data/word_based_bias_list.csv
    btMap['orientation'] = ['lesbians', 'gays',
                            'bisexuals', 'transgender', 'trans',
                            'queers', 'lgbt', 'lgbt', 'homosexual',
                            'heterosexual']
    btMap['gender'] = ['woman', 'females', 'girls', 'non-binary']
    btMap['race'] = ['africans', 'african-americans', 'blacks',
                    'hispanics', 'latino', 'latina', 'latinx', 'mexicans',
                    'indians', 'middle-eastern']
    btMap['religion'] = ['muslims', 'arabs', 'jews']
    targets = df['data']['intersentence']
    for target in targets:
        bt = target['bias_type']
        tt = target['target']
        if tt not in btMap[bt]:
            btMap[bt].append(tt)
    return btMap


def cfNeighbours(btMap):
    """
    :param btMap: the map of bias types
    and lists of targets
    :return: counterfitted-neighbours
    in json format
    """
    cfn = {}
    for bt in btMap:
        for item in btMap[bt]:
            ll = list(btMap[bt])
            ll.remove(item)
            cfn[item] = ll
    # cfnJSON = json.dumps(cfn)
    return cfn
