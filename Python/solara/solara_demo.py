import solara

count = solara.reactive(0)
count2 = solara.reactive(0)
name = solara.reactive("")
n = solara.reactive(0)


@solara.component
def Page():
    solara.Button("Add one", on_click=lambda: count.set(count.value + 1))
    solara.Button("Add two", on_click=lambda: count2.set(count2.value + 2))
    solara.Markdown(f"Count: {count.value}")
    solara.Markdown(f"Count2: {count2.value}")    
    solara.InputText("Your name", value=name)
    solara.Markdown(f"Hello, {name.value or 'stranger'}")
    solara.SliderInt("Pick a number", value=n, min=0, max=100)
    solara.Markdown(f"{n.value} squared is {n.value ** 2}")

