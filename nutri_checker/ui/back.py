import streamlit as st
from typing import List


def suggest_aliments_from_index(input_: str) -> List[str]:
    return st.session_state.index.retrieve(input_, k=5).name_fr.tolist()
