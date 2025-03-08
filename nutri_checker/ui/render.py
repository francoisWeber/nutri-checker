import streamlit as st
from typing import List
from nutri_checker.models.food import Dish
from nutri_checker.ui import food_register, analytics

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

if "current_dish" not in st.session_state:
    st.session_state.current_dish = None

if "current_ingredients" not in st.session_state:
    st.session_state.current_ingredients = []

if "ingredient_id" not in st.session_state:
    st.session_state.ingredient_id = 0

if "portions" not in st.session_state:
    st.session_state.portions: List[Dish] = []

if "current_typed_alim_str" not in st.session_state:
    st.session_state.current_typed_alim_str: str = None


food_register.render()

analytics.render()
