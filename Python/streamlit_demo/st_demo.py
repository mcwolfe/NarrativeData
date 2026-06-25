import streamlit as st
import numpy as np
import pandas as pd

st.title("Synthetic data explorer")

@st.cache_data
def make_data(n, mean, sd, seed):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "x": rng.normal(mean, sd, n),
        "y": rng.normal(mean, sd, n),
    })

with st.sidebar:
    st.header("Controls")
    n    = st.slider("Sample size", 100, 5000, 1000, step=100)
    mean = st.slider("Mean", -5.0, 5.0, 0.0, 0.1)
    sd   = st.slider("Std dev", 0.1, 5.0, 1.0, 0.1)
    seed = st.number_input("Random seed", value=42, step=1)

data = make_data(n, mean, sd, seed)

left, right = st.columns(2)
with left:
    st.metric("Mean of x", f"{data['x'].mean():.3f}")
    st.metric("Std of x",  f"{data['x'].std():.3f}")
with right:
    st.scatter_chart(data, x="x", y="y")