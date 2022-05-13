from argparse import ArgumentParser
import json
import pandas as pd
import numpy as np

if __name__ == "__main__":
    parser = ArgumentParser()
    
    parser.add_argument('--normal-metrics-file', type=str)
    parser.add_argument('--fair-metrics-file', type=str)
    parser.add_argument('--social-groups', type=str)

    args = vars(parser.parse_args())
    
    normal_metrics_file = args['normal_metrics_file']
    fair_metrics_file = args['fair_metrics_file']
    social_groups = args['social_groups'].split()

    with open(normal_metrics_file) as infile:
        normal_metrics = json.load(infile)

    with open(fair_metrics_file) as infile:
        fair_metrics = json.load(infile)

    TPED_normal = sum([abs(normal_metrics['dev']['TPR'] - normal_metrics[social_group]['TPR']) for social_group in social_groups])
    TPED_fair = sum([abs(fair_metrics['dev']['TPR'] - fair_metrics[social_group]['TPR']) for social_group in social_groups])

    FPED_normal = sum([abs(normal_metrics['dev']['FPR'] - normal_metrics[social_group]['FPR']) for social_group in social_groups])
    FPED_fair = sum([abs(fair_metrics['dev']['FPR'] - fair_metrics[social_group]['FPR']) for social_group in social_groups])

    EOdds_normal = TPED_normal + FPED_normal
    EOdds_fair = TPED_fair + FPED_fair

    results_df = pd.DataFrame({'TPED': [TPED_normal, TPED_fair], 'FPED': [FPED_normal, FPED_fair], 'EOdds': [EOdds_normal, EOdds_fair]})
    results_df = results_df.round(4)
    for col_name in results_df.columns:
        results_df[col_name] = results_df[col_name].apply(lambda val: "{:.4f}".format(val))
    results_df['Model'] = ['normal', 'fair']
    results_df.set_index('Model', inplace=True)

    print(results_df)

    results_df.to_csv('results/EOdds.csv')
