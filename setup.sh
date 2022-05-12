#!/bin/bash
mkdir venv/
source venv/bin/activate
pip install -r requirements.txt
./defsetneighbours.py --d="data/dev.json" --o="data/cfn.json"