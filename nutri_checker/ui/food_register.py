import streamlit as st
from streamlit_searchbox import st_searchbox
from nutri_checker.models.food import Aliment, Ingredient, Dish
from nutri_checker.ui.back import suggest_aliments_from_index


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


def render():
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
