from __future__ import print_function, division

import pandas as pd

positions = ['President', 'U.S. Senate', 'U.S. House',
            'State Senate','State House', 'Governor']

def parse_2012():
    '''Reads in CSV from Oklahoma Elections and parses into OpenElections
    format.
    '''
    df = pd.read_csv(
        'http://www.ok.gov/elections/support/12gen_cnty_csv.zip')

    df = df.rename(columns={'county_name': 'county',
                            'race_description': 'office',
                            'cand_absmail_votes': 'absentee',
                            'cand_early_votes': 'early_votes',
                            'cand_elecday_votes': 'election_day',
                            'cand_tot_votes': 'votes',
                            'cand_name': 'candidate',
                            'cand_party': 'party'})

    df = df.drop(['elec_date', 'race_number', 'race_party', 'cand_number',
                  'entity_description', 'tot_race_prec',
                  'race_prec_reporting'], axis=1)

    # extract district information
    df['district'] = df['office'].str.extract('(\d{1,2})', expand=True)

    # clean up office descriptions
    df.loc[df['office'].str.contains(
        'PRESIDENT'), 'office'] = 'President'
    df.loc[df['office'].str.contains(
        'UNITED STATES SENATOR'), 'office'] = 'U.S. Senate'
    df.loc[df['office'].str.contains(
        'UNITED STATES REPRESENTATIVE'), 'office'] = 'U.S. House'
    df.loc[df['office'].str.contains(
        'STATE REPRESENTATIVE'), 'office'] = 'State House'
    df.loc[df['office'].str.contains(
        'STATE SENATOR'), 'office'] = 'State Senate'

    # select only the positions of interest
    df = df[df['office'].isin(positions)].copy()

    # clean up candidate names
    df.loc[df['candidate'].str.contains(
        'CLINTON'), 'candidate'] = 'Hillary Clinton'
    df.loc[df['candidate'].str.contains(
        'JOHNSON'), 'candidate'] = 'Gary Johnson'
    df.loc[df['candidate'].str.contains(
        'TRUMP'), 'candidate'] = 'Donald Trump'
    df.loc[df['candidate'].str.contains(
        'JUSTIN JJ HUMPHREY', case=False), 'candidate'] = 'Justin Humphrey'
    df.candidate = df.candidate.str.title()
    df.candidate = df.candidate.str.replace(r'^(\S+)\s+(.*\b).\s+(\S+)$',
                                            "\\1 \\3").astype('str')
    # melt the votes together
    # dfm = pd.melt(df, id_vars=['county', 'precinct_code', 'office',
    #                         'cand_name', 'cand_party', 'district'],
    #                 value_vars=['Early', 'In-Person', 'Absentee', 'Total'],
    #                 value_name='votes')

    df.county = df.county.str.title()

    # https://www.ok.gov/elections/support/20161108_seb.html
    dft = df.groupby(['office', 'candidate']).agg({'votes': 'sum'})
    assert dft.loc['President'].votes.sum() == 1334872
    assert dft.loc['U.S. House'].votes.sum() == 1325935

    df.to_csv('../2012/20121106__ok__general__county.csv', index=False)

if __name__ == '__main__':
    parse_2012()
