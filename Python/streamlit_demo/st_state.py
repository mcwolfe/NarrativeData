import streamlit as st

class CounterModel:
    def __init__(self):
        self.step_num = 0
        self.value = 100
    def step(self):
        self.step_num += 1
        self.value = self.value * 1.05

# guard: build the model once, keep the SAME instance across reruns
if "model" not in st.session_state:
    st.session_state.model = CounterModel()

model = st.session_state.model          # grab the persistent instance

if st.button("Step"):
    model.step()                        # mutate it — advances and persists

# read its current state
st.metric("Step", model.step_num)
st.metric("Value", f"{model.value:.1f}")