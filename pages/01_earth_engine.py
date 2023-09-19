import leafmap
import solara
import ipywidgets as widgets
import pandas as pd


zoom = solara.reactive(2)
center = solara.reactive((20, 0))


def get_datasets(m):
    url = 'https://raw.githubusercontent.com/opengeos/ee-tile-layers/main/datasets.tsv'
    df = pd.read_csv(url, sep='\t')
    setattr(m, 'df', df)
    return df


def add_widget(m, position="topright"):
    get_datasets(m)
    df = m.df
    datasets = df['id'].values.tolist()

    style = {"description_width": "initial"}
    padding = "0px 0px 0px 5px"

    dataset = widgets.Dropdown(
        options=datasets,
        description="Dataset:",
        style=style,
        layout=widgets.Layout(padding=padding, width="275px"),
    )
    dataset.value = None

    def dataset_changed(change):
        if change["new"]:
            selected = change["new"]
            if selected not in m.get_layer_names():
                m.add_ee_layer(selected)

    dataset.observe(dataset_changed, names="value")

    m.add_widget(dataset, position=position)


class Map(leafmap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add what you want below
        self.add_basemap("SATELLITE", shown=False)
        self.find_layer("Google Satellite").visible = False
        self.add_layer_manager()
        add_widget(self)


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        # solara components support reactive variables
        # solara.SliderInt(label="Zoom level", value=zoom, min=1, max=20)
        # using 3rd party widget library require wiring up the events manually
        # using zoom.value and zoom.set
        Map.element(  # type: ignore
            zoom=zoom.value,
            on_zoom=zoom.set,
            center=center.value,
            on_center=center.set,
            scroll_wheel_zoom=True,
            toolbar_ctrl=False,
            data_ctrl=False,
            height="780px",
        )
        solara.Text(f"Zoom: {zoom.value}")
        solara.Text(f"Center: {center.value}")
