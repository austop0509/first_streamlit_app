import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLerror
		
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

# show fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
try :
	fruit_choice = streamlit.text_input("What fruit would you like information about?", "kiwi")
	if not fruit_choice :
		streamlit.error("Please select a fruit to get information.")
	else :
		fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + fruit_choice)
		fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
		streamlit.dataframe(fruityvice_normalized)
except URLerror as e:
	streamlit.error()

# testing connection to Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

# executes a query of the FRUIT_LOAD_LIST table and returns a data frame
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# add a new entry box for fruits the user would like to see added to the list
add_my_fruit = streamlit.text_input("What fruit would you like to see?")
streamlit.write("Thanks for adding", add_my_fruit)
