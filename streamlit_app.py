# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == 0).collect()
# st.dataframe(data=my_dataframe, use_container_width = True)
editable_df = st.data_editor(my_dataframe)

submitted = st.button("Submit")

if submitted:
    st.success("Someone clicked the button.", icon = '👍')

    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)

    try:
        og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
    except:
        st.write("Something went wrong")
else:
    st.sucess("There are no pending orders right now")
