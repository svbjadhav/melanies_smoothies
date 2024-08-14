# Import python packages
import streamlit as st
import requests
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(":cup_with_straw: My Parents New Healthy Dinner :cup_with_straw:")
st.write(
    """Breakfast Menu
    """)

Name_on_Order = st.text_input("Name On Smoothie:")
st.write("The name on your smoothie will be:", Name_on_Order)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients: ',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
        ingredients_string = ''
    
        for fruit_chosen in ingredients_list:
                ingredients_string += fruit_chosen + ' '
                st.subheader(fruit_chosen + ' Nutrition Information')
                fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
                fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width = True)
        

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + Name_on_Order + """')"""

    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit Order')


    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


