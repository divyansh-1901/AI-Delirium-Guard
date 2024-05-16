import streamlit as st
import joblib
import pandas as pd

st.write("# AI-Delirium Guard")

st.write("\n")
st.write("Gender")
sex = st.selectbox("Gender", ["Male", "Female"],label_visibility='collapsed')

st.write("\n")
st.write("Whether the patient was admitted as an inpatient or treated as an outpatient")
inout = st.selectbox("Whether the patient was admitted as an inpatient or treated as an outpatient",
                     ["Inpatient", "Outpatient"],label_visibility='collapsed')

st.write("\n")
st.write("Whether the patient was transferred")
transt = st.selectbox("Whether the patient was transferred",
                      ['Not transferred (admitted from home)', 'From acute care hospital inpatient',
                       'Outside emergency department', 'Other'],label_visibility='collapsed')

st.write("\n")
st.write("Age")
age = st.number_input("Age", step=1,label_visibility='collapsed')       # unit: years

st.write("\n")
st.write("Destination after discharge from the hospital")
dischdest = st.selectbox("Destination after discharge from the hospital",
                         ['Home', 'Other', 'Rehab', 'Skilled Care, Not Home'],label_visibility='collapsed')

st.write("\n")
st.write("Type of anesthesia used during the procedure")
anesthes = st.selectbox("Type of anesthesia used during the procedure",
                        ['General', 'MAC/IV Sedation', 'Spinal', 'Other'],label_visibility='collapsed')

st.write("\n")
st.write("Type of Surgery Performed")
surgspec = st.selectbox("Type of Surgery Performed",
                        ['Urology Surgery', 'Orthopaedic Surgery', 'General Surgery',
                         'Neurosurgery', 'Thoracic Surgery', 'Head and Neck Surgery (ENT)',
                         'Vascular Surgery', 'Plastic Surgery', 'Cardiac Surgery', 'Gynecology Surgery'],
                        label_visibility='collapsed')

st.write("\n")
st.write("Duration of Surgery")
optime = st.number_input("Duration of Surgery", step=1,label_visibility='collapsed')    # units ?

st.write("\n")
st.write("Whether the surgery was elective (planned) or not")
electsurg = st.selectbox("Whether the surgery was elective (planned) or not", ['Yes', 'No'],label_visibility='collapsed')


st.write("\n")
st.write("Height ")
col1,col2,col3,col4 = st.columns([3,1,3,1])
feet = col1.number_input("Height_feet ", step=1,min_value=0,label_visibility='collapsed',format='%i')
col2.write("Feet")
inches = col3.number_input("Height_inches ", step=1,label_visibility='collapsed',min_value=0,max_value=11,format='%i')
col4.write("Inches")
height = 12*feet + inches

st.write("\n")
st.write("Weight")
col1,col2 = st.columns([7,1])
weight_type = col1.selectbox("Weight_type", ['Pounds', 'Kg'],label_visibility='collapsed')
if weight_type=='Kg':
    col1,col2 = st.columns([7,1])
    weight_kg = col1.number_input("Weight_kg", step=1.0,min_value=0.0,label_visibility='collapsed',)
    col2.write("Kg")
    weight = 2.20462*weight_kg
elif weight_type=='Pounds':
    col1,col2 = st.columns([7,1])
    weight_pounds = col1.number_input("Weight_kg", step=1.0,min_value=0.0,label_visibility='collapsed')
    col2.write("Pounds")
    weight = weight_pounds


st.write("\n")
st.write("Whether the patient has diabetes? If yes, is the patient on Insulin?")
diabetes = st.selectbox("Whether the patient has diabetes? If yes, is the patient on Insulin?",
                        ['NO', 'NON-INSULIN', 'INSULIN'],label_visibility='collapsed')

st.write("\n")
st.write("Whether the patient is a smoker")
smoke = st.selectbox("Whether the patient is a smoker", ['Yes', 'No'],label_visibility='collapsed')

st.write("\n")
st.write("Difficulty in breathing, if present or not. If yes, is it on moderate excretion or at rest?")
dyspnea = st.selectbox("Difficulty in breathing, if present or not. If yes, is it on moderate excretion or at rest?",
                       ['NO', 'MODERATE EXERTION', 'AT REST'],label_visibility='collapsed')

st.write("\n")
st.write("Has the patient been diagnosed with cancer?")
discancr = st.selectbox("Has the patient been diagnosed with cancer?", ['Yes', 'No'],label_visibility='collapsed')

st.write("\n")
st.write("Classification of wound type (e.g., clean, contaminated)")
wndclas = st.selectbox("Classification of wound type (e.g., clean, contaminated)",
                       ['2-Clean/Contaminated', '1-Clean', '4-Dirty/Infected', '3-Contaminated'],label_visibility='collapsed')

st.write("\n")
st.write("Presence of wound infection")
wndinf = st.selectbox("Presence of wound infection", ['Yes', 'No'],label_visibility='collapsed')

st.write("\n")
st.write("Use of steroids as part of treatment")
steroid = st.selectbox("Use of steroids as part of treatment", ['Yes', 'No'],label_visibility='collapsed')

st.write("\n")
st.write("Presence of sepsis")
prsepis = st.selectbox("Presence of sepsis", ['Yes', 'No'],label_visibility='collapsed')

st.write("\n")
st.write("Blood test result for sodium levels")
dprna = st.number_input("Blood test result for sodium levels", step=1,label_visibility='collapsed')

st.write("\n")
st.write("Blood test result for albumin levels")
dpralbum = st.number_input("Blood test result for albumin levels", step=1,label_visibility='collapsed')

st.write("\n")
st.write("Blood test result for hematocrit levels")
dprhct = st.number_input("Blood test result for hematocrit levels", step=1,label_visibility='collapsed')

st.write("\n")
st.write("Whether the procedure was performed as an emergency")
emergncy = st.selectbox("Whether the procedure was performed as an emergency", ['Yes', 'No'],label_visibility='collapsed')

st.write("\n")
st.write("Deep renal insufficiency")
drenainsf = st.number_input("Deep renal insufficiency", step=1,label_visibility='collapsed')

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
    x = {'Urology Surgery': '0',
         'Orthopaedic Surgery': '1',
         'General Surgery': '2',
         'Neurosurgery': '3',
         'Thoracic Surgery': '4',
         'Head and Neck Surgery (ENT)': '5',
         'Vascular Surgery': '6',
         'Plastic Surgery': '7',
         'Cardiac Surgery': '8',
         'Gynecology Surgery': '9'}
    return int(x[data])


def diabetes_transform(data):
    x = {'NO': '0',
         'NON-INSULIN': '1',
         'INSULIN': '2'}
    return int(x[data])


def dyspnea_transform(data):
    x = {'NO': '0',
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
