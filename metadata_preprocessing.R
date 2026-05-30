library(readxl)
library(dplyr)
library(stringr)
library(readr)

# BURGOS DBGAP
BD_metadata <- read_excel("burgos_dbgap/burgos_dbgap_metadata.xlsx") %>%
    rename(
        subject_id = submitted_subject_id,
        sample_id = biospecimen_repository_sample_id,
        sex = `gender.M.1`,
        age = expired_age,
        apoe = ApoE,
        group = AD
    ) %>% mutate(
        apoe = str_replace_all(apoe, "/", ""),
        sex = case_when(
            sex == 1 ~ "male", 
            sex == 2 ~ "female"
        ), group = case_when(
            group == "yes" ~ "AD", 
            group == "no" ~ "control"
        ), type = case_when(
            str_detect(sample_id, "CSF") ~ "CSF",
            str_detect(sample_id, "SER") ~ "serum"
        ), study = "burgos_dbgap"
    )

# SILVER SEQ
SS_sample_metadata <- read_excel("silver_seq/silver_seq_metadata.xlsx") %>%
    rename(
        subject_id = donor_id_alias,
        sample_id = sample_id_alias,
        group = donor_group
    )
 
SS_patient_metadata <- read_excel("silver_seq/silver_seq_patient_metadata.xlsx") %>%
    rename(
        subject_id = donor_id_alias,
        age = expired_age
    )
 
SS_metadata <- inner_join(SS_sample_metadata, SS_patient_metadata, by = "subject_id") %>%
    mutate(
        apoe = as.character(apoe),
        sex = case_when(
            sex == "M" ~ "male", 
            sex == "F" ~ "female"
        ), group = case_when(
            group == "AD" ~ "AD", 
            group == "N" ~ "control"
        ), type = "plasma",
        study = "silver_seq"
    )

# TODEN
TD_metadata <- read_excel("toden/toden_metadata.xlsx", na = c("", "None")) %>%
    rename(
        sample_id = Run,
        subject_id = PatientID,
        age = Age,
        sex = Gender,
        group = Disease,
        apoe = `Apoe.status`
    ) %>% mutate(
        subject_id = as.character(subject_id),
        apoe = apoe %>% 
            str_replace_all("/", "") %>% 
            str_replace_all("E", ""),
        group = case_when(
            group == "AD" ~ "AD", 
            group == "NCI" ~ "control"
        ), sex = str_to_lower(sex),
        type = "plasma",
        study = "toden"
    )

# COMBINED
columns <- c("study", "sample_id", "subject_id", "group", "type",
             "sex", "age", "apoe", "apoe_carrier", "apoe_dose")
 
metadata <- bind_rows(
  BD_metadata %>% select(all_of(columns)),
  SS_metadata %>% select(all_of(columns)),
  TD_metadata %>% select(all_of(columns))
)
 
write_tsv(metadata, "combined_metadata.tsv", na = "")