from __future__ import print_function, division

import pandas as pd 
import numpy as np

def parser_2004():
  columns = ['test1','test2','test3']
  candidate_name_list = []
  #columns = ['County','Carson','Coburn','Bilyeu','Total Votes']
  election_results = []
  original_df = pd.read_csv('../tabula/2004/tabula-04usrep.csv',names=columns)

  
  # output = original_df.ix[3][1]
  # for index, rows in original_df.iterrows():
  #   try:
  #     print(rows)
  #   except UnicodeEncodeError:
  #     print('BAD')
  for index, rows in original_df.iterrows():
    if original_df.ix[index][1].rfind('DISTRICT') != -1:
      candidate_count = header_split(index, original_df)
      county_split(index, original_df, candidate_count)


def county_split(df_index, df, candidate_count):
  county_index = df_index + 5
  while df.ix[county_index][0] != 'STATE TOTAL:':
    county_name = df.ix[county_index][0]
    candidate_vote_totals = df.ix[county_index][1].split(' ')[0:candidate_count]
    candidate_vote_totals.insert(0,county_name)
    county_index = county_index + 1
    print(candidate_vote_totals)

def header_split(df_index, df):
  candidate_name_list = []
  df_first_name_index = df_index + 2
  df_last_name_index = df_index + 3
  district = df.ix[df_index][1].split(' ')[-1]
  candidate_first_name = df.ix[df_first_name_index][1].split(' ')
  candidate_first_name = [x for x in candidate_first_name if x.find('.') == -1 and x.find('TOTAL') == -1]
  candidate_last_name_split = df.ix[df_last_name_index][1].split(' ')
  candidate_last_name = [x for x in candidate_last_name_split if x.find('(') == -1 and x.find('VOTES') == -1]
  for index, value in enumerate(candidate_first_name):
    candidate_name_list.append(value + ' ' + candidate_last_name[index])
  return len(candidate_name_list)

  #   election_results.append([original_df['County'][index],'U.S. Senate',' ','DEM','Brad Carson',original_df['Carson'][index]])
  #   election_results.append([original_df['County'][index],'U.S. Senate',' ','REP','Tom Coburn',original_df['Coburn'][index]])
  #   election_results.append([original_df['County'][index],'U.S. Senate',' ','IND','Sheila Bilyeu',original_df['Bilyeu'][index]])
  # candidate_df = pd.DataFrame(election_results, columns=('County','Office','District','Party','Candidate','Votes'))
  # candidate_df.to_csv('../2004/20041102__ok__general__us__senate__county.csv',index=False)

if __name__ == '__main__':
  parser_2004()