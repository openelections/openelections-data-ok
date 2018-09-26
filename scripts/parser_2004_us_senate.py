from __future__ import print_function, division

import pandas as pd 

def parser_2004():
  columns = ['County','Carson','Coburn','Bilyeu','Total Votes']
  election_results = []
  original_df = pd.read_csv('../tabula/2004/tabula-04ussen.csv',names=columns)

  for index, rows in original_df.iterrows():
    election_results.append([original_df['County'][index],'U.S. Senate',' ','DEM','Brad Carson',original_df['Carson'][index]])
    election_results.append([original_df['County'][index],'U.S. Senate',' ','REP','Tom Coburn',original_df['Coburn'][index]])
    election_results.append([original_df['County'][index],'U.S. Senate',' ','IND','Sheila Bilyeu',original_df['Bilyeu'][index]])
  candidate_df = pd.DataFrame(election_results, columns=('County','Office','District','Party','Candidate','Votes'))
  candidate_df.to_csv('../2004/20041102__ok__general__us__senate__county.csv',index=False)

if __name__ == '__main__':
  parser_2004()