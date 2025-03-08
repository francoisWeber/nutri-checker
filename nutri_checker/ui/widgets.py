from itertools import cycle
from typing import Any
import streamlit as st
from nutri_checker.models.food import Aliment, Ingredient, Dish
from uuid import uuid4


class IngredientWidget:
    @staticmethod
    @st.fragment
    def display(ingredient: Ingredient):
        st.write(f"{ingredient.aliment.name_fr}, {ingredient.quantity_g} g")
    
class DishWidget:
    @staticmethod
    def display(dish: Dish):
        with st.container(border=True):
            st.markdown(f"## {dish.name}")
            columns = st.columns([1, 1, 1, 1, 2, 1])
            with st.container(border=True):
                DishWidget._grid_of_ingredient(dish, columns[:-2])
            with st.container(border=True):
                with columns[-2]:
                    qt = st.slider("quantité", 0, dish.final_weight_g, step=10, key=f"portion-{dish._id}")
                with columns[-1]:
                    if st.button("take", key=f"take-{dish._id}"):
                        st.session_state.portions.append(dish.get_portion(qt))
                        st.session_state.current_dish = None
                        st.session_state.current_ingredients = []
                        st.write(f"portion {qt}g")
                        st.rerun()
                
    @staticmethod
    @st.fragment
    def display_wip(dish: Dish, columns: list | None = None):
            if dish.name:
                st.markdown(f"## {dish.name}")
            else:
                name = st.text_input("Nom du plat ?")
                dish.name = name
            columns = columns if columns else st.columns(5)
            DishWidget._grid_of_ingredient(dish, columns)
                    
    @staticmethod
    def _grid_of_ingredient(dish: Dish, columns: list):
        for col, ingredient in zip(cycle(columns), dish.ingredients):
            with col:
                IngredientWidget.display(ingredient)
                
    @staticmethod
    @st.fragment
    def display_as_portion(dish: Dish):
        st.markdown(f"{dish.name} {dish.get_total_weight_g()}g")
                
    

# class Widget:
#     @staticmethod
#     @st.fragment
#     def display(element: Any):
#         if isinstance(element, Ingredient):
#             Widget._display_ingredient(element)
#         elif isinstance(element, Dish):
#             Widget._display_dish(element)

#     @staticmethod
#     def _display_ingredient(ingredient: Ingredient):
#         st.write(f"{ingredient.aliment.name_fr}, {ingredient.quantity_g} g")

#     @st.fragment
#     @staticmethod
#     def _display_dish(dish: Dish):
#         uid = str(dish._id)

#         st.markdown(f"## {dish.name} {uid}")
#         columns = st.columns(5)
#         for col, ingredient in zip(cycle(columns), dish.ingredients):
#             with col:
#                 Widget.display(ingredient)
#         columns = st.columns(2)
#         with columns[0]:
#             qt = st.slider("quantité", 0, dish.final_weight_g, step=10, key=f"portion-{uid}")
#         with columns[1]:
#             if st.button("take", key=f"take-{uid}"):
#                 st.write(f"portion {qt}g")
#                 st.session_state.portions.append(dish.get_portion(qt))
#                 st.session_state.dishes.append(dish)
#                 st.session_state.current_dish = None
#                 st.session_state.current_ingredients = []
#                 st.rerun()
