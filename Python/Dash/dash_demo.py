from dash import Dash, dcc, html, Input, Output
import numpy as np
import plotly.express as px

app = Dash()

app.layout = html.Div([
    html.H1("Synthetic data explorer"),
    dcc.Slider(10, 500, value=50, id="n-slider"),
    dcc.Graph(id="scatter"),
])

@app.callback(
    Output("scatter", "figure"),
    Input("n-slider", "value"),
)
def update(n):
    rng = np.random.default_rng(42)
    x = rng.normal(0, 1, n)
    y = rng.normal(0, 1, n)
    return px.scatter(x=x, y=y)

if __name__ == "__main__":
    app.run(debug=True)