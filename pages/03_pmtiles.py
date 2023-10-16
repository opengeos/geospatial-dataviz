import leafmap
import solara


zoom = solara.reactive(2)
center = solara.reactive((20, 0))


class Map(leafmap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add what you want below

        self.add_basemap('CartoDB.DarkMatter')
        url = "https://storage.googleapis.com/ahp-research/overture/pmtiles/overture.pmtiles"

        style={
            "version": 8,
            "sources": {
                "example_source": {
                    "type": "vector",
                    "url": "pmtiles://" + url,
                    "attribution": 'PMTiles',
                }
            },
            "layers": [
                {
                    "id": "admins",
                    "source": "example_source",
                    "source-layer": "admins",
                    "type": "fill",
                    "paint": {"fill-color": "#BDD3C7", "fill-opacity": 0.1},
                },
                {
                    "id": "buildings",
                    "source": "example_source",
                    "source-layer": "buildings",
                    "type": "fill",
                    "paint": {"fill-color": "#FFFFB3", "fill-opacity": 0.5},
                },
                {
                    "id": "places",
                    "source": "example_source",
                    "source-layer": "places",
                    "type": "fill",
                    "paint": {"fill-color": "#BEBADA", "fill-opacity": 0.5},
                },
                {
                    "id": "roads",
                    "source": "example_source",
                    "source-layer": "roads",
                    "type": "line",
                    "paint": {"line-color": "#FB8072"},
                },
            ],
        }

        self.add_pmtiles(url, name='PMTiles', style=style)

        legend_dict = {
            'admins': 'BDD3C7',
            'buildings': 'FFFFB3',
            'places': 'BEBADA',
            'roads': 'FB8072',
        }

        self.add_legend(legend_dict=legend_dict)


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
