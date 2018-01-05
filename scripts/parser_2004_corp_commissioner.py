from __future__ import print_function, division

import pandas as pd 

def parser_2004():
  columns = ['County','Wylie','Bode','Total Votes']
  election_results = []
  original_df = pd.read_csv('../tabula/2004/tabula-04corp.csv',names=columns)

  for index, rows in original_df.iterrows():
    election_results.append([original_df['County'][index],'Corporation Commissioner',' ','(D)','John Wylie',original_df['Wylie'][index]])
    election_results.append([original_df['County'][index],'Corporation Commissioner',' ','(R)','Denise Bode',original_df['Bode'][index]])
  candidate_df = pd.DataFrame(election_results, columns=('County','Office','District','Party','Candidate','Votes'))
  candidate_df.to_csv('../2004/20041102__ok__general__corp__commissioner__county.csv',index=False)

if __name__ == '__main__':
  parser_2004()