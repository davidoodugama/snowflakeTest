# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingrediant_list = st.multiselect('Choose up to 5 ingrediants:',
                                 my_dataframe,
                                 max_selections = 5
                                )
if ingrediant_list:
    ingrediant_string = ''

    for fruit_chosen in ingrediant_list:
        ingrediant_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    st.write(ingrediant_string)

    my_insert_stmt = f"""
    INSERT INTO SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER)
    VALUES ('{ingrediant_string}', '{name_on_order}')
    """
    st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered", icon="✅")
