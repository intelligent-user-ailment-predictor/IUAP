# -*- coding: utf-8 -*-
"""heart_disease_app.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/157YVvd-cLgE9x9ydXcyYP4kA8KcOW_CF
"""

import numpy as np
import pickle
import streamlit as st
import pandas as pd
from bokeh.plotting import figure
import matplotlib.pyplot as plt
import numpy as np
import smtplib


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def create_userhealth():
	c.execute('CREATE TABLE IF NOT EXISTS usershealth(username TEXT,age integer,sex text,chest_pain text,rest_bp real,serum_cl real,fast_bs integer,rest_ecg text,max_hr integer,st_dep real,ex_ag text,slope text,ves_nm integer,tha text)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()
	
def add_userhealth_data(username,age,sex,chest_pain,rest_bp,serum_cl,fast_bs,rest_ecg,max_hr,st_dep,ex_ag,slope,ves_nm,tha):
	c.execute('INSERT INTO usershealth (username,age,sex,chest_pain,rest_bp,serum_cl,fast_bs,rest_ecg,max_hr,st_dep,ex_ag,slope,ves_nm,tha) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) ',(username,age,sex,chest_pain,rest_bp,serum_cl,fast_bs,rest_ecg,max_hr,st_dep,ex_ag,slope,ves_nm,tha))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users(user):
	c.execute('SELECT * FROM usershealth')
	data = c.fetchall()
	return data



# Load ML model
model = pickle.load(open('model.pkl', 'rb')) 

def predict(age,sex,chest_pain,rest_bp,serum_cl,fast_bs,rest_ecg,max_hr,st_dep,ex_ag,slope,ves_nm,tha):
    if sex == "Male":
        sex = 1
    else:
        sex = 0

    if fast_bs == False:
        fast_bs = 0
    else:
        fast_bs = 1
 
    if rest_ecg == "left ventricular hypertrophy":
        rest_ecg = 0
    elif rest_ecg == "normal":
        rest_ecg = 1 
    else:
        rest_ecg = 2

    if slope == "downsloping":
        slope = 0
    elif slope == "flat":
        slope = 1
    else:
        slope = 2
    
    if ex_ag == "No":
        ex_ag = 0
    else:
        ex_ag = 1

    if tha == "fixed defect":
        tha = 1
    elif tha == "normal":
        tha = 2
    else:
        tha = 3
     
    if chest_pain == "asymptomatic":
        chest_pain = 0
    elif chest_pain == "atypical angina":
        chest_pain = 1    
    elif chest_pain == "non-anginal pain":
        chest_pain = 2
    else:
    	chest_pain = 3


    values=[age,sex,chest_pain,rest_bp,serum_cl,fast_bs,rest_ecg,max_hr,st_dep,ex_ag,slope,ves_nm,tha]
    
    # Put all form entries values in a list 
    features = [float(i) for i in values]
    # Convert features to array
    array_features = [np.array(features)]
    # Predict features
    prediction = model.predict(array_features)    
    output = prediction    
    # Check the output values and retrive the result with html tag based on the value
    if output == 1:
        st.text("The patient is not likely to have heart disease!")
    else:
        st.text("The patient is likely to have heart disease!")
        sender = "iupacwecare@gmail.com"
        receiver = "iupacwecare@gmail.com"
        password= "iupac@123"
        message = "Please rush to your friend's aid asap"
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(sender,password)
        server.sendmail(sender,receiver,message)
def main():

	menu = ["Heart","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Heart":
		st.subheader("Please login or signup to continue")
		

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Check Heart","Analytics","Profiles"])
				if task == "Check Heart":
					st.subheader("Check Heart")
					age = st.number_input('Age')
					sex = st.selectbox('Gender',("Male","Female"))
					chest_pain = st.selectbox('Chest Pain Type',("asymptomatic","typical angina","typical angina","non-anginal pain"))
					rest_bp = st.number_input("Resting Blood Pressure in mm Hg")
					serum_cl = st.number_input("Serum Cholesterol in mg/dl")
					fast_bs = st.selectbox("Fasting Blood Sugar",(False,True))
					rest_ecg = st.selectbox("Resting ECG Results",("normal","Having ST-T wave abnormality","left ventricular hypertrophy"))
					max_hr = st.number_input("Maximum Heart Rate")
					st_dep = st.number_input("ST Depression Induced")
					ex_ag = st.selectbox("Exercise Induced Angina ",("No","Yes"))
					slope = st.selectbox("Slope of the Peak Exercise ST Segment",("unsloping","flat","downsloping"))
					ves_nm = st.selectbox("Number of Vessels Colored by Flourosopy",(0,1,2,3))
					tha = st.selectbox("Thalassemia",("fixed defect","normal","reversable defect"))
					
					if st.button("Predict"):
						predict(age,sex,chest_pain,rest_bp,serum_cl,fast_bs,rest_ecg,max_hr,st_dep,ex_ag,slope,ves_nm,tha)	
						create_userhealth()					
						add_userhealth_data(username,age,sex,chest_pain,rest_bp,serum_cl,fast_bs,rest_ecg,max_hr,st_dep,ex_ag,slope,ves_nm,tha)

				elif task == "Analytics":
					st.subheader("Analytics")
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users(username)
					clean_db = pd.DataFrame(user_result,columns=["username","age","sex","chest_pain","rest_bp","serum_cl","fast_bs","rest_ecg","max_hr","st_dep","ex_ag","slope","ves_nm","tha"])
					select_user=clean_db.loc[clean_db["username"]==username]

					select_user2=select_user[["age","rest_bp","serum_cl","max_hr","st_dep","ves_nm"]]
					st.dataframe(select_user2)
					
					
					
					
					grp_slt = st.selectbox("Graphs",["Age vs Resting BP","Age vs Serum Cholesterol","Age vs Maximum Heartrate"])
					if grp_slt=="Age vs Resting BP":
						#st.line_chart(select_user2[["age","rest_bp"]])
						x=select_user[["age"]]
						y=select_user[["rest_bp"]]
						fig = plt.figure()
						ax = fig.add_subplot(1,1,1)
						ax.plot(x,y)
						ax.set_xlabel("Age")
						ax.set_ylabel("Resting BP")
						st.write(fig)
						
					elif grp_slt=="Age vs Serum Cholesterol":
						#st.line_chart(select_user2[["age","serum_cl"]])
						x=select_user[["age"]]
						y=select_user[["serum_cl"]]
						p.line(x, y, legend_label='Trend', line_width=2)
						st.bokeh_chart(p, use_container_width=True)
					else:
						#st.line_chart(select_user2[["age","max_hr"]])
						x=select_user[["age"]]
						y=select_user[["max_hr"]]
						p.line(x, y, legend_label='Trend', line_width=2)
						st.bokeh_chart(p, use_container_width=True)
					
					
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")






if __name__ == '__main__':
#Run the application
    main()
