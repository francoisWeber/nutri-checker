import streamlit as st
from streamlit_searchbox import st_searchbox
from nutri_checker.models.food import Aliment, Ingredient, Dish
from nutri_checker.ui.back import suggest_aliments_from_index
from nutri_checker.ui import widgets


class FoodAdder:
    """Add new raw aliment or dish to the list"""

    @staticmethod
    def search_new_ingredient():
        cols = st.columns([3, 1])
        with cols[0]:
            name = st_searchbox(suggest_aliments_from_index, key="add_alim_search")
        with cols[1]:
            quantity_g = st.slider("quantité (g)", min_value=10, max_value=1000, step=10, key="add_alim_quantity")
        return name, quantity_g

    @staticmethod
    def register_raw_aliment(name, quantity_g):
        aliment = Aliment.from_name_in_nutridata(name, st.session_state.index)
        ingredient = Ingredient(aliment, quantity_g)
        dish = Dish(name=name, ingredients=[ingredient])
        st.session_state.portions.append(dish)

    @staticmethod
    def register_aliment_to_currnt_dish(name, quantity_g):
        if st.session_state.current_dish is None:
            st.session_state.current_dish = Dish()
        aliment = Aliment.from_name_in_nutridata(name, st.session_state.index)
        ingredient = Ingredient(aliment, quantity_g)
        st.session_state.current_ingredients.append(ingredient)
        st.session_state.current_dish.ingredients = st.session_state.current_ingredients
        
    @staticmethod
    def display_current_dish_state():
        if st.session_state.current_dish:
            widgets.DishWidget.display_wip(st.session_state.current_dish)
            
    @staticmethod
    def validate_current_dish():
        if st.session_state.current_dish:
            valid_btn = st.button(":arrow_double_down: terminer le plat :arrow_double_down:")
            if valid_btn:
                st.session_state.dishes.append(st.session_state.current_dish)
                st.session_state.current_dish = None
                st.session_state.current_ingredients = []
                st.rerun()

    @staticmethod
    def render():
        name, quantity_g = FoodAdder.search_new_ingredient()
        cols = st.columns([3, 2, 2])
        with cols[1]:
            register_dish = st.button(":bento: :heavy_plus_sign: ajouter au plat :arrow_double_down:")
        with cols[2]:
            register_alim = st.button(":apple: :heavy_plus_sign: ajouter l'aliment :arrow_forward:")
        if register_alim:
            FoodAdder.register_raw_aliment(name, quantity_g)
        if register_dish:
            FoodAdder.register_aliment_to_currnt_dish(name, quantity_g)

        FoodAdder.display_current_dish_state()
        FoodAdder.validate_current_dish()

