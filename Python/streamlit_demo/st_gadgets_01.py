import streamlit as st




left, right = st.columns(2)

with left:
    choice = st.selectbox("Pick one", ["A", "B", "C"])

with right:
    st.write("You picked:", choice)
    st.metric(label="Active models", value=42, delta=5)

st.write('---')

a, b, c = st.columns(3)

with a:
    st.metric("Agents", 1000)
with b:
    st.metric("Steps", 50, delta=10)
with c:
    st.metric("Gini", 0.38, delta=-0.04)