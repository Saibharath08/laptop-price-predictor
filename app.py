import streamlit as st
import pickle
import numpy as np

pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

st.title("Laptop Price Predictor")

st.info("""
Tips:
• Ultrabook = lightweight premium laptop
• Notebook = regular laptop
• Gaming = high-performance laptop
• Typical weight = 1kg to 3kg
• Higher PPI = better display quality
""")

company = st.selectbox('Brand', df['Company'].unique())
type_name = st.selectbox('Type', df['TypeName'].unique())
ram = st.selectbox('RAM (GB)', [2,4,8,16,32,64])
weight = st.slider('Weight (kg)', 0.8, 4.5, 1.5)
touchscreen = st.selectbox('Touchscreen', ['No','Yes'])
ips = st.selectbox('IPS DISPLAY',['No','Yes'])
ppi = st.slider('PPI (Screen Quality)', 90, 350, 141)
cpu = st.selectbox('CPU Brand', df['Cpu brand'].unique())
hdd = st.selectbox('HDD Storage (GB)', [0,128,256,500,1000,2000])
ssd = st.selectbox('SSD (GB)', [0,8,128,256,512,1024,2048])
gpu = st.selectbox('GPU Brand', df['Gpu brand'].unique())
os = st.selectbox('Operating System', df['os'].unique())

if st.button('Predict Price'):

    touchscreen = 1 if touchscreen == 'Yes' else 0
    ips = 1 if ips == 'Yes' else 0

    # Common sense validations
    if company == "Apple" and os != "Mac":
        st.error("Apple laptops usually run on Mac OS.")

    elif company == "Apple" and hdd > 0:
        st.warning("Most Apple laptops don't use HDD storage.")

    elif hdd == 0 and ssd == 0:
        st.error("Laptop must have at least one storage option.")

    elif type_name == "Gaming" and gpu == "Intel":
        st.warning("Gaming laptops usually have NVIDIA or AMD GPU.")

    elif type_name == "Ultrabook" and weight > 2:
        st.warning("Ultrabooks are usually lightweight (<2kg).")

    else:
        query = np.array([
            company, type_name, ram, weight,
            touchscreen, ips, ppi, cpu,
            hdd, ssd, gpu, os
        ])

        query = query.reshape(1,12)

        prediction = int(np.exp(pipe.predict(query)[0]))

        st.success("Predicted Price: ₹" + str(prediction))