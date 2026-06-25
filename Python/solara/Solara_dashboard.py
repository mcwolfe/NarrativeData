import solara
import numpy as np
import matplotlib.figure

n    = solara.reactive(1000)
mean = solara.reactive(0.0)
sd   = solara.reactive(1.0)

@solara.component
def Page():
    with solara.Sidebar():
        solara.Markdown("## Controls")
        solara.SliderInt("Sample size", value=n, min=100, max=5000)
        solara.SliderFloat("Mean", value=mean, min=-5, max=5)
        solara.SliderFloat("Std dev", value=sd, min=0.1, max=5)

    fig = matplotlib.figure.Figure()
    ax = fig.subplots()
    rng = np.random.default_rng(42)
    data = rng.normal(mean.value, sd.value, n.value)
    ax.hist(data, bins=40)
    solara.FigureMatplotlib(fig)