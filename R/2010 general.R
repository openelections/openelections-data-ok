library(tidyverse)
library(pdftools)

### Goal: county, office, candidate, party, precinct, mail_votes, early_votes, elec_day_votes, total_votes, district ####
open2018 <- read_csv("../openelections-data-ok/2018/20181106__ok__general__precinct.csv")

d <- read.fwf("../110210.DAT", 
                widths = c(4, 4, 6, 4, 5, 3,
                           7, 56, 38, 13, 30, 20, 
                           25, 6))
names(d) <- c("race_num",
              "cand_num",
              "filler",
              "precinct_num", 
              "votes",
              "party",
              "district",
              "race",
              "cand_name",
              "filler2",
              "precinct_name",
              "party_name",
              "district_name",
              "election_date")

names(open2018)

open2010 <- d %>% 
  mutate(county = str_extract(precinct_name, ".*(?= CO\\.)") %>%
           str_to_title(), 
         office = str_squish(race) %>% 
           str_remove_all("^FOR |,.*| AND INSPECTOR| VOTING") %>% 
           str_to_title() %>% 
           str_replace_all("Of", "of"),
         candidate = cand_name %>%
           str_squish %>%
           str_to_title,
         party = str_squish(party),
         precinct = str_extract(precinct_name, "\\d{6}|ABSENTEE.*(\\d{1,2}|$)") %>%
           str_remove("PCT\\.") %>%
           str_squish(),
         district = str_extract(district, "\\d{1,3}") %>% 
           as.numeric) %>%
  mutate(office = case_when(office == "United States Senator" ~ "U.S. Senate",
                            office == "U.s. Representative" ~ "U.S. House",
                            office == "State Representative" ~ "State House",
                            office == "State Senator" ~ "State Senate",
                            TRUE ~ office)
         ) %>% 
  select(county, office, candidate, party, precinct, votes, district) %>%
  filter(!str_detect(office, "State Question|District Attorney|Court|Judge"))

unique(open2018$office)  
unique(open2010$office)







