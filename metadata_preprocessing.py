import pandas as pd

BD_metadata = pd.read_excel("burgos_dbgap/burgos_dbgap_metadata.xlsx")
BD_metadata.rename(columns = {"submitted_subject_id": "subject_id",
                    "biospecimen_repository_sample_id": "sample_id",
                    "gender.M.1": "sex", "expired_age": "age",
                    "ApoE": "apoe", "AD": "group"}, inplace = True)
BD_metadata["apoe"] = BD_metadata["apoe"].str.replace("/", "")
BD_metadata["sex"] = BD_metadata["sex"].map({1: "male", 2: "female"})
BD_metadata["group"] = BD_metadata["group"].map({"yes": "AD", "no": "control"})
BD_metadata.loc[BD_metadata["sample_id"].str.contains("CSF"), "type"] = "CSF"
BD_metadata.loc[BD_metadata["sample_id"].str.contains("SER"), "type"] = "serum"
BD_metadata["study"] = "burgos_dbgap"


SS_sample_metadata = pd.read_excel("silver_seq/silver_seq_metadata.xlsx")
SS_sample_metadata.rename(columns = {"donor_id_alias": "subject_id",
                            "sample_id_alias": "sample_id",
                            "donor_group": "group"}, inplace = True)
SS_patient_metadata = pd.read_excel("silver_seq/silver_seq_patient_metadata.xlsx")
SS_patient_metadata.rename(columns = {"donor_id_alias": "subject_id", 
                            "expired_age": "age"}, inplace = True)
SS_metadata = pd.merge(SS_sample_metadata, SS_patient_metadata, on = "subject_id")
SS_metadata["sex"] = SS_metadata["sex"].map({"M": "male", "F": "female"})
SS_metadata["group"] = SS_metadata["group"].map({"AD": "AD", "N": "control"})
SS_metadata["type"] = "plasma"
SS_metadata["study"] = "silver_seq"

TD_metadata = pd.read_excel("toden/toden_metadata.xlsx")
TD_metadata.rename(columns = {"Run": "sample_id", "PatientID": "subject_id",
                    "Age": "age", "Gender": "sex", "Disease": "group", 
                    "Apoe.status": "apoe"}, inplace = True)
TD_metadata["apoe"] = TD_metadata["apoe"].str.replace("/", "").str.replace("E", "")
TD_metadata["group"] = TD_metadata["group"].map({"AD": "AD", "NCI": "control"})
TD_metadata["sex"] = TD_metadata["sex"].str.lower()
TD_metadata["type"] = "plasma"
TD_metadata["study"] = "toden"

columns = ["study", "sample_id", "subject_id", "group", "type", 
           "sex", "age", "apoe", "apoe_carrier", "apoe_dose"]
dfs = [BD_metadata[columns], SS_metadata[columns], TD_metadata[columns]]
metadata = pd.concat(dfs, axis = 0)
metadata.to_csv("combined_metadata.tsv", sep = "\t")