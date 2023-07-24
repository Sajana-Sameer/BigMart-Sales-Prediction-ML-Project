import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import base64


from src.pipeline.predict_pipeline import CustomData, PredictPipeline
# Function to load and cache the background image
def load_background_image(image_path):
    image = Image.open(image_path)
    return image



# Function to disable options based on Item Fat Content selection
def disable_options_based_on_fat_content(item_fat_content, item_type_select):
    non_food_types = ["Health and Hygiene", "Household", "Others"]
    if item_fat_content == "Non-Edible":
        item_type_select.options = [item_type for item_type in item_type_select.options if item_type not in non_food_types]
    else:
        item_type_select.options = item_type_select.options

# Function to validate Item Visibility input
def validate_item_visibility(value):
    try:
        float_value = float(value)
        if not 0 < float_value < 1:
            raise ValueError
    except ValueError:
        raise st.StreamlitAPIException("Please enter a value between 0 (exclusive) and 1 (exclusive).")

def show_index():
 
    # Display the logo image within the header
    st.image("static/log1.jpg", use_column_width=True)
    
    st.title("BigMart Sale Prediction")

    st.write("Please enter the following details to predict the Item Outlet Sales:")

    item_weight = st.text_input("Item Weight:")
    item_fat_content = st.selectbox("Item Fat Content:", ["Low Fat", "Regular", "Non-Edible"])
    item_visibility = st.text_input("Item Visibility (enter between 0 and 1):", "")
    
    if item_fat_content == "Non-Edible":
        item_type_options = [
            "Health and Hygiene",
            "Household",
            "Others",
        ]
    else:
        item_type_options = [
            "Baking Goods",
            "Breads",
            "Breakfast",
            "Canned",
            "Dairy",
            "Frozen Foods",
            "Fruits and Vegetables",
            "Hard Drinks",
            "Meat",
            "Seafood",
            "Snack Foods",
            "Soft Drinks",
            "Starchy Foods",
        ]
    
    item_type = st.selectbox("Item Type:", item_type_options)
        
    item_mrp = st.text_input("Item MRP:")

    # Custom Outlet Location Type dropdown select using html
   # st.markdown("<label for='outlet_location_type'>Outlet Location Type:</label>", unsafe_allow_html=True)
    outlet_location_type_dict = {"Tier 1": 0, "Tier 2": 1, "Tier 3": 2}
    outlet_location_type = st.selectbox(
        "Outlet Location Type:",
        list(outlet_location_type_dict.keys()),
        key="outlet_location_type"  # Use a unique key to avoid issues with duplicate widgets
    )

    outlet_size_dict = {"High": 0, "Medium": 1, "Small": 2}
    outlet_size = st.selectbox("Outlet Size:", list(outlet_size_dict.keys()))

    # Custom Outlet Type dropdown select using html
  #  st.markdown("<label for='outlet_type'>Outlet Type:</label>", unsafe_allow_html=True)
    outlet_type_dict = {
        "Grocery Store": 0,
        "Supermarket Type1": 1,
        "Supermarket Type2": 2,
        "Supermarket Type3": 3
    }
    outlet_type = st.selectbox(
        "Outlet Type:",
        list(outlet_type_dict.keys()),
        key="outlet_type"  # Use a unique key to avoid issues with duplicate widgets
    )

    if st.button("Submit"):
        try:
            # Validate Item Visibility
            float_value = float(item_visibility)
            if not 0 < float_value < 1:
                raise ValueError("Please enter a value between 0 (exclusive) and 1 (exclusive) for item visibility.")

            # Process the data and make predictions
            data = CustomData(
                Item_Weight=float(item_weight),
                Item_Fat_Content=item_fat_content,
                Item_Visibility=float(item_visibility),
                Item_Type=item_type,
                Item_MRP=float(item_mrp),
                Outlet_Establishment_Year=2023,  # Change this to the appropriate year
                Outlet_Size=outlet_size_dict[outlet_size],
                Outlet_Location_Type=outlet_location_type_dict[outlet_location_type],
                Outlet_Type=outlet_type_dict[outlet_type]
            )
            pred_df = data.get_data_as_data_frame()
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            prediction = round(results[0], 2)
            st.markdown(
                f"""
                <p style="color: blue; font-size: 24px; font-weight: bold; text-align: center;">
                The prediction of ITEM OUTLET SALES is {prediction}
                </p>
                """,
                unsafe_allow_html=True,
            )
        except ValueError as e:
            st.error(str(e))

if __name__ == "__main__":
    show_index()
