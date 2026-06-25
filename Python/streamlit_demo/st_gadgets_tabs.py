import streamlit as st
import numpy as np
import pandas as pd

if "count" not in st.session_state:
    st.session_state.count = 0

if "log" not in st.session_state:
    st.session_state.log = []

with st.sidebar:
    st.header("Controls")
    n    = st.slider("Sample size", 100, 5000, 1000, step=100)
    mean = st.slider("Mean", -5.0, 5.0, 0.0, 0.1)
    seed = st.number_input("Seed", value=42, step=1)
    if st.button("Add one"):
        st.session_state.count += 1
    entry = st.text_input("Add an entry")
    if st.button("Save"):
        st.session_state.log.append(entry)

# main area — uses the values the sidebar produced
rng = np.random.default_rng(seed)
data = pd.DataFrame({"x": rng.normal(mean, 1.0, n)})

st.title("Synthetic data explorer")
st.line_chart(data)


st.write("Count:", st.session_state.count)
st.write(f"You have {len(st.session_state.log)} entries.")
st.dataframe(pd.DataFrame({"entry": st.session_state.log}))