from __future__ import print_function, division

import pandas as pd 
import numpy as np

def parser_2004():
  election_results = []
  original_df = pd.read_csv('../tabula/2004/tabula-04ss.csv',header=None)

  for index, rows in original_df.iterrows():
    if original_df.ix[index][1].rfind('DISTRICT') != -1:
      return_list = header_split(index, original_df)
      top_results = county_split(index, original_df, return_list,election_results)

def header_split(df_index, df):
  candidate_name_list = []
  df_first_name_index = df_index + 2
  df_last_name_index = df_index + 3
  district = df.ix[df_index][1].split(' ')[-1]
  candidate_first_name = df.ix[df_first_name_index][1].split(' ')
  candidate_first_name = [x for x in candidate_first_name if x.find('.') == -1 and x.find('TOTAL') == -1]
  candidate_last_name_split = df.ix[df_last_name_index][1].split(' ')
  candidate_last_name = [x for x in candidate_last_name_split if x.find('(') == -1 and x.find('VOTES') == -1]
  candidate_party = [x for x in candidate_last_name_split if x.find('(') != -1]
  #print(candidate_first_name)
  #print('-----')
  #print(candidate_last_name)
  #print('-----')
  for index, value in enumerate(candidate_first_name):
    #print(value)
    candidate_name_list.append(value + ' ' + candidate_last_name[index])
  return_list = [len(candidate_name_list),district,candidate_name_list,candidate_party]
  #print(return_list)
  return return_list

def county_split(df_index, df, return_list,election_results):
  county_index = df_index + 5
  candidate_count = return_list[0]
  while df.ix[county_index][0] != 'STATE TOTAL:':
    county_name = df.ix[county_index][0]
    candidate_vote_totals = df.ix[county_index][1].split(' ')[0:candidate_count]
    candidate_vote_totals.insert(0,county_name)
    county_index = county_index + 1
    election_output(return_list[1],return_list[2],return_list[3],candidate_vote_totals,election_results)

def election_output(district, candidates, candidate_party, candidates_vote_totals,election_results):
  for index, value in enumerate(candidates):
    index_value = index+1
    election_results.append(([str(candidates_vote_totals[0]),'State Senate',str(district),candidate_party[index],value,str(candidates_vote_totals[index_value])]))
  election_totals(election_results)

def election_totals(results_string):
  candidate_df = pd.DataFrame(results_string, columns=('County','Office','District','Party','Candidate','Votes'))
  candidate_df.loc[candidate_df['Candidate'].str.contains('JUDY'),'Candidate'] = 'Judy Eason McIntyre'
  candidate_df.loc[candidate_df['Candidate'].str.contains('DEWEY'),'Candidate'] = 'Dewey Bartlett, Jr.'
  candidate_df.to_csv('../2004/20041102__ok__general__state_senate__county.csv',index=False)
  

if __name__ == '__main__':
  parser_2004()