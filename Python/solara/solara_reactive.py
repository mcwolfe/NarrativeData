import solara
import time
import threading

class CounterModel:
    def __init__(self):
        self.step_num = 0
        self.value = 100
    def step(self):
        self.step_num += 1
        self.value *= 1.05

model = CounterModel()
tick = solara.reactive(0)
playing = solara.reactive(False)

@solara.component
def Page():
    tick.value

    def do_step():
        model.step()
        tick.set(tick.value + 1)

    def run(cancel: threading.Event):
        while playing.value and not cancel.is_set():
            model.step()
            tick.set(tick.value + 1)
            time.sleep(0.3)

    solara.use_thread(run, dependencies=[playing.value])

    with solara.Row():
        solara.Button("Step", on_click=do_step)
        solara.Button(
            "Pause" if playing.value else "Play",
            on_click=lambda: playing.set(not playing.value),
        )

    solara.Markdown(f"Step: {model.step_num}")
    solara.Markdown(f"Value: {model.value:.1f}")