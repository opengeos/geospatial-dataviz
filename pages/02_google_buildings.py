import leafmap
import solara
import ipywidgets as widgets
import pandas as pd
import geopandas as gpd

zoom = solara.reactive(2)
center = solara.reactive((20, 0))


def get_datasets(m):
    url = 'https://raw.githubusercontent.com/opengeos/ee-tile-layers/main/datasets.tsv'
    df = pd.read_csv(url, sep='\t')
    setattr(m, 'df', df)
    return df


def add_widget(m, position="topright"):
    building_url = "https://sites.research.google/open-buildings/tiles.geojson"
    country_url = (
        "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    )

    building_gdf = gpd.read_file(building_url)
    country_gdf = gpd.read_file(country_url)
    countries = country_gdf["NAME"].values.tolist()
    countries.sort()

    style = {"description_width": "initial"}
    padding = "0px 0px 0px 5px"

    country = widgets.Dropdown(
        options=countries,
        description="Country:",
        style=style,
        layout=widgets.Layout(padding=padding, width="275px"),
    )
    country.value = None

    m.add_gdf(building_gdf, layer_name="Coverage", zoom_to_layer=True, info_mode=None)

    def country_changed(change):
        if change["new"]:
            selected = change["new"]
            selected_gdf = country_gdf[country_gdf["NAME"] == selected]
            gdf_style = {
                "color": "#000000",
                "weight": 2,
                "opacity": 1,
                "fill": False,
                "fillColor": "#3388ff",
            }
            if selected not in m.get_layer_names():
                m.add_gdf(
                    selected_gdf,
                    layer_name=selected,
                    zoom_to_layer=True,
                    info_mode=None,
                    style=gdf_style,
                )

    country.observe(country_changed, names="value")

    m.add_ee_layer('GOOGLE/open-buildings', name='Buildings')

    m.add_widget(country, position=position)


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
