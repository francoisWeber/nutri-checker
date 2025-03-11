import pandas as pd
import streamlit as st
from streamlit_searchbox import st_searchbox
from typing import List
from nutri_checker.models.food import Aliment, Ingredient, Dish
from nutri_checker.data.loader import COLUMNS_QUANTI
from nutri_checker.data.ajr import DAILY_RECOMMENDATION

from streamlit_option_menu import option_menu

from nutri_checker.data.loader import (
    load_nutri_data,
)
from nutri_checker.search.bm25 import NutriIndex
import altair as alt
from pathlib import Path

from nutri_checker.ui import home

st.set_page_config(layout="wide")

with st.sidebar:
    def on_change(key):
        selection = st.session_state[key]
        st.write(f"Selection changed to {selection}")
        
    selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
        icons=['house', 'cloud-upload', "list-task", 'gear'], 
        menu_icon="cast", default_index=0, orientation="vertical", on_change=on_change, key="menu")


st.title("Nutri checker")
if st.session_state["menu"] == "Home":
    home.render()
    

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


def suggest_aliments_from_index(input_: str) -> List[str]:
    return st.session_state.index.retrieve(input_, k=5).name_fr.tolist()


def ask_for_new_ingredient():
    name = st_searchbox(suggest_aliments_from_index, key="add_alim_search")
    quantity_g = st.slider("quantité (g)", min_value=10, max_value=1000, step=10, key="add_alim_quantity")
    if st.button(":+1:", key=f"add-ingr-{st.session_state.ingredient_id}"):
        ingredient = IngredientWidget(
            Aliment.from_name_in_nutridata(name, st.session_state.index),
            quantity_g,
        )
        st.session_state.current_ingredients.append(ingredient)
        st.session_state.ingredient_id += 1
        st.rerun()


class IngredientWidget(Ingredient):
    def display(self):
        st.write(self.aliment.name_fr)
        st.write(f"{self.quantity_g} g")


class DishWidget(Dish):
    def display(self):
        st.markdown(f"## {self.name}")
        columns = st.columns(len(self.ingredients) + 1)
        for col, ingredient in zip(columns, self.ingredients):
            with col:
                ingredient.display()
        with columns[-1]:
            with st.form(key=f"dish portion {self.name}"):
                qt = st.slider("quantité", 0, self.final_weight_g, step=10)
                take = st.form_submit_button("take")
                if take:
                    st.session_state.portions.append(self.get_portion(qt))
                    st.rerun()


st.divider()

with st.container(border=True):
    st.write("Ajouter un plat")

    ask_for_new_ingredient()

    if st.session_state.current_ingredients:
        dish_name = st.text_input("Nom du plat")
        if dish_name:
            if st.button(":+1:"):
                dish_id = 1 + len(st.session_state.dishes)
                dish = DishWidget(dish_name, ingredients=st.session_state.current_ingredients)
                st.session_state.dishes.append(dish)
                st.session_state.current_ingredients = []
                st.rerun()

        columns = st.columns(len(st.session_state.current_ingredients))
        for col, ingredient in zip(columns, st.session_state.current_ingredients):
            with col:
                ingredient.display()


for dish in st.session_state.dishes:
    dish.display()

if st.session_state.portions:
    df = pd.concat([portion.get_nutri() for portion in st.session_state.portions])
    ddf = df.groupby("name_fr")[COLUMNS_QUANTI].sum()
    ddf_pct_ajr = ddf.div(pd.Series(DAILY_RECOMMENDATION)).dropna(axis=1)
    df_long = ddf_pct_ajr.reset_index().melt(id_vars="name_fr", var_name="Nutrient", value_name="Value")
    chart = (
        alt.Chart(df_long)
        .mark_bar()
        .encode(x="Nutrient:N", y="Value:Q", color="name_fr:N")
        .properties(width=600, height=400)
    )
    st.altair_chart(chart, use_container_width=True)
