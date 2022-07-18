import pandas as pd
import numpy as np

ecg = pd.read_csv("EKG_baseline_final_new.csv")[["idcode", "idx", "exp_filepath", "ekg_d", "AcquisitionDateTime"]]
stroke = pd.read_csv("LIST_stroke_v5.csv")

stroke_id_list = set(stroke["IDCODE"])
ecg1 = ecg[ecg["idcode"].isin(stroke_id_list)]
ecg_id_list = set(ecg1["idcode"])

ecg1["AcquisitionDateTime"] = pd.to_datetime(ecg1["AcquisitionDateTime"], format = "%d%b%y:%H:%M:%S")
stroke["IN_DATE"] = pd.to_datetime(stroke["IN_DATE"])
stroke["OUT_DATE"] = pd.to_datetime(stroke["OUT_DATE"])

test = 0
ecg4 = pd.DataFrame()
for i in ecg_id_list:
    test = test+1
    print(test, len(ecg_id_list))
    ecg2 = ecg1[ecg1["idcode"] == i]
    stroke1 = stroke[stroke["IDCODE"] == i]
    for u in stroke1["IN_DATE"]:
        stroke2 = stroke1[stroke1["IN_DATE"] == u]
        ecg3 = ecg2[(ecg2["AcquisitionDateTime"].values > stroke2["IN_DATE"].values) & (ecg2["AcquisitionDateTime"].values < stroke2["OUT_DATE"].values)]
        #ecg3 = ecg2[(ecg2["AcquisitionDateTime"].values > (stroke2["IN_DATE"] - np.timedelta64(3,'D')).values) & (ecg2["AcquisitionDateTime"].values < stroke2["OUT_DATE"].values)]
        ecg4 = ecg4.append(ecg3)

ecg5 = ecg4.sort_values(by=['idcode', 'AcquisitionDateTime'], ascending=True)
ecg6 = ecg5.drop_duplicates(subset=['idcode', "ekg_d"], keep = "last")

stroke_merged = pd.merge(stroke, ecg6, left_on="IDCODE", right_on="idcode", how='left')

test = 0
stroke_merged3 = pd.DataFrame()
for i in stroke_id_list:
    test = test + 1
    print(test, len(stroke_id_list))
    stroke_merged1 = stroke_merged[stroke_merged["IDCODE"] == i]
    stroke_merged2 = stroke_merged1[(stroke_merged1["AcquisitionDateTime"].values > stroke_merged1["IN_DATE"].values) & (stroke_merged1["AcquisitionDateTime"].values < stroke_merged1["OUT_DATE"].values)]
    #stroke_merged2 = stroke_merged1[(stroke_merged1["AcquisitionDateTime"].values > (stroke_merged1["IN_DATE"] - np.timedelta64(3,'D')).values) & (stroke_merged1["AcquisitionDateTime"].values < stroke_merged1["OUT_DATE"].values)]
    stroke_merged3 = stroke_merged3.append(stroke_merged2)

stroke_merged4 = stroke_merged3.sort_values(by=['idcode', 'AcquisitionDateTime'], ascending=True)
stroke_merged5 = stroke_merged4.drop_duplicates(subset=['idcode', "IN_DATE"], keep = "last")

stroke_merged6 = pd.merge(stroke, stroke_merged5, on=['LOC', 'IDCODE', 'IN_DATE', 'OUT_DATE', 'IN_YEAR', 'DXKD1', 'SEQ', 'RE_STROKE', 'REG_FOLLOWUP', 'IV_tPA', 'IA', 'stroke_type'], how='left')
stroke_merged7 = stroke_merged6.drop(["idcode", "ekg_d", "AcquisitionDateTime"], axis = 1)
stroke_merged7.to_csv("stroke_with_last_ecg_record.csv", index = False)
#stroke_merged7.to_csv("stroke_with_last_ecg_record_minus_3Days.csv", index = False)