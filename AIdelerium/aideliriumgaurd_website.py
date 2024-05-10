import streamlit as st
import joblib
import pandas as pd

st.write("# AI-Delirium Guard")

sex = st.selectbox("Enter patient's gender", ["Male", "Female"])

inout = st.selectbox("Whether the patient was admitted as an inpatient or treated as an outpatient",
                     ["Inpatient", "Outpatient"])

transt = st.selectbox("Whether the patient was transferred from some hospital?",
                      ['Not transferred (admitted from home)', 'From acute care hospital inpatient',
                       'Outside emergency department', 'Other'])

age = st.number_input("Enter patient's age", step=1)

dischdest = st.selectbox("Destination after discharge from the hospital",
                         ['Home', 'Other', 'Rehab', 'Skilled Care, Not Home'])

anesthes = st.selectbox("Type of anesthesia used during the procedure",
                        ['General', 'MAC/IV Sedation', 'Spinal', 'Other'])

surgspec = st.selectbox("Medical specialty of the surgeon performing the procedure",
                        ['Urology', 'Orthopedics', 'General Surgery',
                         'Neurosurgery', 'Thoracic', 'Otolaryngology (ENT)',
                         'Vascular', 'Plastics', 'Cardiac Surgery', 'Gynecology'])

electsurg = st.selectbox("Whether the surgery was elective (planned) or not", ['Yes', 'No'])

height = st.number_input("Enter patient's height", step=1)

weight = st.number_input("Enter patient's weight", step=1)

diabetes = st.selectbox("Whether the patient has diabetes",
                        ['NO', 'NON-INSULIN', 'INSULIN'])

smoke = st.selectbox("Whether the patient is a smoker", ['Yes', 'No'])

dyspnea = st.selectbox("Difficulty in breathing, if present or not",
                       ['No', 'MODERATE EXERTION', 'AT REST'])

discancr = st.selectbox("Diagnosis of cancer", ['Yes', 'No'])

wndinf = st.selectbox("Presence of wound infection", ['Yes', 'No'])

steroid = st.selectbox("Use of steroids as part of treatment", ['Yes', 'No'])

wndclas = st.selectbox("Classification of wound type (e.g., clean, contaminated)",
                       ['2-Clean/Contaminated', '1-Clean', '4-Dirty/Infected', '3-Contaminated'])

prsepis = st.selectbox("Presence of sepsis", ['Yes', 'No'])

dprna = st.number_input("Blood test result for sodium levels", step=1)

dpralbum = st.number_input("Blood test result for albumin levels", step=1)

dprhct = st.number_input("Blood test result for hematocrit levels", step=1)

emergncy = st.selectbox("Whether the procedure was performed as an emergency", ['Yes', 'No'])

optime = st.number_input("Duration of the operation (surgery time)", step=1)

drenainsf = st.number_input("Deep renal insufficiency", step=1)

df_pred = pd.DataFrame([[sex, inout, transt, age, dischdest, anesthes, surgspec, electsurg, height, weight, diabetes,
                         smoke, dyspnea, discancr, wndinf, steroid, wndclas, prsepis, dprna, dpralbum, dprhct, emergncy,
                         optime, drenainsf]],
                       columns=['sex', 'inout', 'transt', 'age', 'dischdest', 'anesthes', 'surgspec', 'electsurg',
                                'height', 'weight', 'diabetes', 'smoke', 'dyspnea', 'discancr', 'wndinf', 'steroid',
                                'wndclas', 'prsepis', 'dprna', 'dpralbum', 'dprhct', 'emergncy', 'optime', 'drenainsf'])


# Encoding for prediction
def transt_transform(data):
    x = {'Not transferred (admitted from home)': '0',
         'From acute care hospital inpatient': '1',
         'Outside emergency department': '2',
         'Other': '3'}
    return int(x[data])


def dischdest_transform(data):
    x = {'Home': '0',
         'Other': '1',
         'Rehab': '2',
         'Skilled Care, Not Home': '3'}
    return int(x[data])


def anesthes_transform(data):
    x = {'General': '0',
         'MAC/IV Sedation': '1',
         'Spinal': '2',
         'Other': '3'}
    return int(x[data])


def surgspec_transform(data):
    x = {'Urology': '0',
         'Orthopedics': '1',
         'General Surgery': '2',
         'Neurosurgery': '3',
         'Thoracic': '4',
         'Otolaryngology (ENT)': '5',
         'Vascular': '6',
         'Plastics': '7',
         'Cardiac Surgery': '8',
         'Gynecology': '9'}
    return int(x[data])


def diabetes_transform(data):
    x = {'NO': '0',
         'NON-INSULIN': '1',
         'INSULIN': '2'}
    return int(x[data])


def dyspnea_transform(data):
    x = {'No': '0',
         'MODERATE EXERTION': '1',
         'AT REST': '2'}
    return int(x[data])


def wndclas_transform(data):
    x = {'2-Clean/Contaminated': '0',
         '1-Clean': '1',
         '4-Dirty/Infected': '2',
         '3-Contaminated': '3'}
    return int(x[data])


df_pred['sex'] = df_pred['sex'].apply(lambda x: 0 if x == 'Male' else 1)
df_pred['inout'] = df_pred['inout'].apply(lambda x: 0 if x == 'Inpatient' else 1)
df_pred['transt'] = df_pred['transt'].apply(transt_transform)
df_pred['dischdest'] = df_pred['dischdest'].apply(dischdest_transform)
df_pred['anesthes'] = df_pred['anesthes'].apply(anesthes_transform)
df_pred['surgspec'] = df_pred['surgspec'].apply(surgspec_transform)
df_pred['electsurg'] = df_pred['electsurg'].apply(lambda x: 0 if x == 'No' else 1)
df_pred['diabetes'] = df_pred['diabetes'].apply(diabetes_transform)
df_pred['smoke'] = df_pred['smoke'].apply(lambda x: 0 if x == 'No' else 1)
df_pred['dyspnea'] = df_pred['dyspnea'].apply(dyspnea_transform)
df_pred['discancr'] = df_pred['discancr'].apply(lambda x: 0 if x == 'No' else 1)
df_pred['wndinf'] = df_pred['wndinf'].apply(lambda x: 0 if x == 'No' else 1)
df_pred['steroid'] = df_pred['steroid'].apply(lambda x: 0 if x == 'No' else 1)
df_pred['wndclas'] = df_pred['wndclas'].apply(wndclas_transform)
df_pred['prsepis'] = df_pred['prsepis'].apply(lambda x: 0 if x == 'No' else 1)
df_pred['emergncy'] = df_pred['emergncy'].apply(lambda x: 0 if x == 'No' else 1)


std_scaler = joblib.load('std_scaler.save')
df = std_scaler.transform(df_pred)

model = joblib.load('model.joblib')
prediction = model.predict(df)

if st.button("Predict"):
    if prediction[0] == 0:
        st.write('#### You likely will not experience postoperative delirium after surgery.')

    else:
        st.write('#### You are likely to experience postoperative delirium after surgery.')
