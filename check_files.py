import pandas as pd

check_df = pd.read_csv("file_names.csv")

ecg_df = pd.read_csv("ukb_ecg_1yrDeath.csv")

ecg_id_list = []
for i in ecg_df["exp_filepath"]:
    ecg_id_list.append(i[12:])
ecg_df["exp_filepath_short"] = ecg_id_list
ecg_df_1 = ecg_df[ecg_df["exp_filepath_short"].isin(check_df["csv_name"])]
ecg_df_2 = ecg_df_1.drop(["exp_filepath_short"], axis = 1)
ecg_df_2.to_csv("ukb_ecg_1yrDeath_refined.csv", index = False)