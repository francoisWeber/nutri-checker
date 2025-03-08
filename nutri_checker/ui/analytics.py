import pandas as pd
import streamlit as st
from nutri_checker.data.loader import COLUMNS_QUANTI
from nutri_checker.data.ajr import DAILY_RECOMMENDATION

import altair as alt


def render():
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
