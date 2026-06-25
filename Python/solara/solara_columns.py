import solara

@solara.component
def Page():
    with solara.Columns([1, 2]):

        # left pane (proportion 1) — a vertical stack of controls
        with solara.Column():
            solara.Markdown("### Controls")
            solara.Button("Run")
            solara.Button("Reset")

        # right pane (proportion 2) — the wider results area
        with solara.Column():
            solara.Markdown("### Results")
            solara.Markdown("charts go here")