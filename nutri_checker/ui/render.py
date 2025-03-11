import streamlit as st
from typing import List
from nutri_checker.models.food import Dish
from nutri_checker.ui import widgets
from nutri_checker.ui import analytics
from nutri_checker.ui.food_register import FoodAdder
from nutri_checker.data.loader import (
    load_nutri_data,
)
from nutri_checker.search.bm25 import NutriIndex
from pathlib import Path

st.set_page_config(layout="wide")

NUTRIDATA_PATH = Path(__file__).parent.parent.parent / "data" / "table_Ciqual_2020_FR_20200707.xls"
MISSING_DATA = Path(__file__).parent.parent.parent / "data" / "missing_values.json"

if "df" not in st.session_state:
    st.session_state.df = load_nutri_data(NUTRIDATA_PATH, MISSING_DATA)

if "index" not in st.session_state:
    st.session_state.index = NutriIndex(st.session_state.df)

if "dishes" not in st.session_state:
    st.session_state.dishes = []

if "current_ingredients" not in st.session_state:
    st.session_state.current_ingredients = []

if "current_dish" not in st.session_state:
    st.session_state.current_dish = None

if "ingredient_id" not in st.session_state:
    st.session_state.ingredient_id = 0

if "portions" not in st.session_state:
    st.session_state.portions: List[Dish] = []

if "current_typed_alim_str" not in st.session_state:
    st.session_state.current_typed_alim_str: str = None

if "food_adder" not in st.session_state:
    st.session_state.food_adder = FoodAdder()

cols = st.columns(2)
with cols[0]:
    with st.container(border=True):
        st.session_state.food_adder.render()

    # display every registered dishes
    for dish in st.session_state.dishes:
        widgets.DishWidget.display(dish)


with cols[1]:
    with st.container(border=True):
        analytics.render()

        # display every portions
    with st.container(border=True):
        for portion in st.session_state.portions:
            widgets.DishWidget.display_as_portion(portion)
