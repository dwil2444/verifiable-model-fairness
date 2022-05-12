#!../venv/bin/python
import json


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
    bt = getBiasTypes(df)
    btMap = {}
    for item in bt:
        btMap[item] = []
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
    cfnJSON = json.dumps(cfn)
    return cfnJSON
