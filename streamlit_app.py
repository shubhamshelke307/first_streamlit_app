import pandas
import snowflake.connector
import requests
import streamlit
from urllib.error import URLError
streamlit.title('My Parent New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑 Avocado')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)



def get_fruitvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice )
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error('Please select the fruit to get informations')
  else:
    # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    back_from_function = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

# import snowflake.connector

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * from fruit_load_list")
# my_data_rows = my_cur.fetchall()
# streamlit.header("The fruit load list contains:")
# streamlit.dataframe(my_data_rows)


streamlit.header("The fruit load list contains:")
def get_fruit_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

# Add a button to load the fruit

if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_list()
  streamlit.dataframe(my_data_rows)
streamlit.stop()
  
streamlit.header("Fruityvice Fruit Advice!")

# fruit_choice = streamlit.text_input('What fruit would you like to add?','canteloupe')
# streamlit.write('The user entered ', fruit_choice)

# my_cur.execute("insert into fruit_load_list values('from streamlit')")



def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur: 
    my_cur.execute("insert into fruit_load_list values ('from streamlit')") 
    return "Thanks for adding " + new_fruit


add_my_fruit = streamlit.text_input('What fruit would you like to add?') 
if streamlit.button('Add a Fruit to the List'): 
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
  back_from_function = insert_row_snowflake(add_my_fruit) 
  streamlit.text(back_from_function)
