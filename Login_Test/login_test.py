import streamlit as st
import pandas as pd
import plotly.express as px
import Analytics_test
import FinLiteracy_Test
import yfinance as yf
import plotly.graph_objects as go



PAGES = {
	"Analytics": Analytics_test,
	"You Should Know":FinLiteracy_Test
}



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
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data


def main():
	placeholder = st.empty()

	st.sidebar.title("FinLit")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		placeholder.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				placeholder.empty()
				st.success("Logged In as {}".format(username))

				#task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
				selection = st.sidebar.radio("Go to", list(PAGES.keys()))
				page = PAGES[selection]
				page.app()
# 				if task == "Add Post":
# 					st.subheader("Add Your Post")

# 				elif task == "Analytics":
# 					st.subheader("Analytics")
# 					analytics()
# 				elif task == "Profiles":
# 					st.subheader("User Profiles")
# 					user_result = view_all_users()
# 					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
# 					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')
		n = len(new_password)
		if st.button("Signup") and n>=6:
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")
		else:
			st.warning("Password should contain 6 or more characters")



if __name__ == '__main__':
	main()
