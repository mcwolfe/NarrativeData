import solara

@solara.component
def Page():
    with solara.Column():

        # top row of small stat cards
        with solara.Row():
            with solara.Card("Agents"):
                solara.Markdown("## 1000")
            with solara.Card("Steps"):
                solara.Markdown("## 50")
            with solara.Card("Gini"):
                solara.Markdown("## 0.38")

        # main split below
        with solara.Columns([1, 2]):
            with solara.Card("Controls"):
                solara.Button("Run")
            with solara.Card("Results"):
                solara.Markdown("charts go here")