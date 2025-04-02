import streamlit as st
import altair as alt

from nutri_checker.models.food import NutriRecap


def render():
    if st.session_state.portions:
        recap = NutriRecap(st.session_state.portions)
        ddf_pct_ajr = recap.get_nutri_summary_by_alim_in_ajr_pct()
        df_long = ddf_pct_ajr.reset_index().melt(id_vars="name_fr", var_name="Nutrient", value_name="Value")
        chart = (
            alt.Chart(df_long)
            .mark_bar()
            .encode(y="Nutriment:N", x="Value:Q", color="name_fr:N")
            .properties(width=600, height=800)
        )
        st.altair_chart(chart, use_container_width=True)
