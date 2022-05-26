import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner")

# displays favorite menu items
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

# interactive menu for customers
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

# Simplifies later code by adding a function, gets the data from the Fruityvice API
def get_fruityvice_data(this_fruit_choice):
	fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + this_fruit_choice)
	fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
	return fruityvice_normalized

# show fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
try :
	fruit_choice = streamlit.text_input("What fruit would you like information about?", "kiwi")
	if not fruit_choice :
		streamlit.error("Please select a fruit to get information.")
	else :
		back_from_function = get_fruityvice_data(fruit_choice)
		streamlit.dataframe(back_from_function)
except URLError as e:
	streamlit.error()

# Queries Snowflake PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST
streamlit.header("View our fruit list - add your favorites!")
def get_fruit_load_list():
	with my_cnx.cursor() as my_cur:
		my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
		return my_cur.fetchall()
	
# Add button for generating the queried list
if streamlit.button("Get fruit list"):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	my_data_rows = get_fruit_load_list()
	my_cnx.close()   # closes the connection to the Snowflake database
	streamlit.dataframe(my_data_rows)

# Solicits user input for fruit they want to add to the queried list
def insert_row_snowflake(new_fruit):
	with my_cnx.cursor() as my_cur:
		my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('"+ new_fruit +"')")
		return "Thanks for adding " + add_my_fruit
	
add_my_fruit = streamlit.text_input("Which fruit would you like to add?")
if streamlit.button("Add a fruit to the list"):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	back_from_function = insert_row_snowflake(add_my_fruit)
	my_cnx.close()
	streamlit.text(back_from_function)
	
streamlit.stop()
# executes a query of the FRUIT_LOAD_LIST table and returns a data frame
streamlit.header("View our fruit list - add your favorites!")
# added function for generating list of fruits from Snowflake
def get_fruit_load_list():
	with my_cnx.cursor as my_cur:
		my_cur.execute("select * from fruit_load_list")
		return my_cur.fetchall()
	
if streamlit.button('Get Fruit List'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	my_data_rows = get_fruit_load_list()
	streamlit.dataframe(my_data_rows)


# Allows user to add fruit to the list
def insert_row_snowflake(new_fruit):
	with my_cnx.cursor() as my_cur:
		my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')")
		return "Thanks for adding" + new_fruit

add_my_fruit = streamlit.text_input("What fruit would you like to add?")
if streamlit.button('Add a fruit to the list'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	back_from_function = insert_row_snowflake(add_my_fruit)
	streamlit.text(back_from_function)
