import solara


@solara.component
def Page():
    with solara.Column(align="center"):
        markdown = """
        ## An interactive web app for visualizing geospatial data
        
        ### Introduction

        - Web App: <https://giswqs-geospatial-dataviz.hf.space>
        - GitHub: <https://github.com/opengeos/geospatial-dataviz>
        - Hugging Face: <https://huggingface.co/spaces/giswqs/geospatial-dataviz>

        """

        solara.Markdown(markdown)
