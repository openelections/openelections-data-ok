from __future__ import print_function, division

import pandas as pd 

def parser_2004():
  columns = ['County','Kerry','Bush',' Total Votes']
  election_results = []
  original_df = pd.read_csv('../tabula/2004/tabula-04pres.csv',names=columns)

  for index, rows in original_df.iterrows():
    election_results.append([original_df['County'][index],'George W. Bush','REP',original_df['Bush'][index]])
    election_results.append([original_df['County'][index],'John F. Kerry','DEM',original_df['Kerry'][index]])

  candidate_df = pd.DataFrame(election_results, columns=('County','Candidate','Party','Votes'))
  candidate_df.to_csv('../2004/20041102__ok__general__president.csv',index=False)

if __name__ == '__main__':
  parser_2004()