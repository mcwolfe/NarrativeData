import solara
import pandas as pd
import matplotlib.figure

data = pd.DataFrame({
    "step": [1, 2, 3, 4, 5],
    "value": [10, 14, 13, 18, 22],
})

@solara.component
def Page():
    with solara.lab.Tabs():
        with solara.lab.Tab("Chart"):
            fig = matplotlib.figure.Figure()
            ax = fig.subplots()
            ax.plot(data["step"], data["value"])
            solara.FigureMatplotlib(fig)
        with solara.lab.Tab("Data"):
            solara.DataFrame(data)