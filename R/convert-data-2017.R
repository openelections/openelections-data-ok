library(tidyverse)
library(rvest)
library(lubridate)

OUTPUT_DIR = '../2017/'

if (!exists('electionDfs')) {
  electionsPage <- read_html('https://www.ok.gov/elections/Election_Info/Election_Results/2017-Election_Results.html')
  electionsTable <- electionsPage %>% html_nodes(xpath='//table') %>% .[[1]] %>% html_table()
  electionDates <- paste0(electionsTable$X1, ', 2017') %>% mdy() %>% format('%Y%m%d')
  
  outputDir <- tempdir()
  dir.create(outputDir, showWarnings = FALSE)
  
  electionDfs <- map(electionDates, function(dateString) {
    fn <- paste0(dateString, '_prec_csv.zip')
    url <- paste0('http://www.ok.gov/elections/support/', fn)
    writeLines(paste0('Downloading dataset ', url))
    outputFile <- paste0(outputDir, '/', fn)
    download.file(url, destfile=outputFile, method='curl', extra='-L', quiet=TRUE)
    suppressMessages(read_csv(outputFile))
  })
  
  names(electionDfs) <- electionDates
  
}

processElectionDf <- function(electionDf, electionDate) {
  
  electionDf <- electionDf %>%
    select(county=county_name, race_description, party=cand_party,
           candidate=cand_name, precinct=precinct_code, ends_with('_votes')) %>%
    mutate(
      race_description=gsub(x=race_description, pattern='^FOR (.+)', replacement='\\1'),
      race_description=gsub(x=race_description, pattern=' [ ]+', replacement=' '),
      office=gsub(x=race_description, pattern='STATE SENATOR.+', replacement='State Senator'),
      office=gsub(x=office, pattern='STATE REPRESENTATIVE.+', replacement='State Representative'),
      district=gsub(x=race_description, pattern='STATE (?:SENATOR|REPRESENTATIVE) DISTRICT ([0-9]+).+', replacement='\\1', perl=TRUE),
      district=case_when(grepl(x=district, pattern='[0-9]+') ~ district, TRUE ~ NA_character_),
      party=case_when(
        party=='REP' ~ 'Republican',
        party=='DEM' ~ 'Democratic',
        party=='IND' ~ 'Independent',
        party=='LIB' ~ 'Libertarian',
        TRUE ~ party
      )
    ) %>%
    select(county, office, candidate, party, precinct, mail_votes=cand_absmail_votes, early_votes=cand_early_votes, elec_day_votes=cand_elecday_votes, votes=cand_tot_votes, district)
  
  fn <- paste0(OUTPUT_DIR, electionDate, '__ok__special__general__precinct.csv')
  writeLines(paste0('Writing output csv to ', fn))
  write_csv(electionDf, fn, na='')
  
  electionDf
  
}

outputDfs <- map2(electionDfs, names(electionDfs), processElectionDf)
