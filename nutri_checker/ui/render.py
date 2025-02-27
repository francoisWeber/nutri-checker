import pandas as pd
import streamlit as st
from typing import List
from nutri_checker.models.food import Aliment, Ingredient, Dish
from nutri_checker.data.loader import COLUMNS_QUANTI
from nutri_checker.data.ajr import DAILY_RECOMMENDATION

from nutri_checker.data.loader import (
    load_nutri_data,
)
from nutri_checker.search.bm25 import NutriIndex

st.title("Nutri checker")

NUTRIDATA_PATH = (
    "/Users/francois.weber/code/nutri-checker/data/table_Ciqual_2020_FR_20200707.xls"
)

if "df" not in st.session_state:
    st.session_state.df = load_nutri_data(NUTRIDATA_PATH)

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


def ask_for_new_ingredient():
    with st.form(key="next_ingredient"):
        name = st.text_input("ingrédient", "")
        quantity_g = st.slider("quantité (g)", min_value=10, max_value=1000, step=10)
        submitted = st.form_submit_button(":+1:")
        if submitted:
            ingredient = IngredientWidget(
                Aliment.from_name_in_nutridata(name, st.session_state.index),
                quantity_g,
            )
            st.session_state.current_ingredients.append(ingredient)
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
                qt = st.slider("quantité", 0, 500, step=10)
                take = st.form_submit_button("take")
                if take:
                    st.session_state.portions.append(self.get_portion(qt))
                    st.rerun()


st.divider()

ask_for_new_ingredient()

if st.session_state.current_ingredients:
    columns = st.columns(1 + len(st.session_state.current_ingredients))
    for col, ingredient in zip(columns, st.session_state.current_ingredients):
        with col:
            ingredient.display()
    with columns[-1]:
        btn = st.button(":+1:")
        if btn:
            dish_id = 1 + len(st.session_state.dishes)
            dish = DishWidget(
                f"plat {dish_id}", ingredients=st.session_state.current_ingredients
            )
            st.session_state.dishes.append(dish)
            st.session_state.current_ingredients = []
            st.rerun()


for dish in st.session_state.dishes:
    dish.display()

if st.session_state.portions:
    df = pd.concat([portion.get_nutri() for portion in st.session_state.portions])
    daily_input = df[COLUMNS_QUANTI].sum(axis=0) / 100
    pct_ajr = daily_input / pd.Series(DAILY_RECOMMENDATION) * 100
    pct_ajr = pct_ajr[pd.notna(pct_ajr)]
    st.bar_chart(pct_ajr)
    pd.DataFrame(daily_input).T
