#!./venv/bin/python
import argparse
import json

from parser.biastypes import loadJSONFile, getBiasTypeMap, cfNeighbours


def main():
    parser = argparse.ArgumentParser(description='Load Json file with bias types and create'
                                                 'Counterfitted Neighbours')
    parser.add_argument('-d', '--data-file',  type=str,
                        help='path to json file containing bias types')
    parser.add_argument('-o', '--output-file', type=str,
                        help='output file for counterfitted '
                             'neighbours')
    args = parser.parse_args()
    df = vars(args)['data_file']
    of = vars(args)['output_file']
    print(of)
    f = loadJSONFile(df)
    df = getBiasTypeMap(f)
    cfn = cfNeighbours(df)
    with open(of, 'w', encoding='utf-8') as f:
        json.dump(cfn, f, indent=4)


if __name__ == "__main__":
    main()