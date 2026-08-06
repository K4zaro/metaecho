from typer import Typer

import metaecho

app = Typer()


@app.command()
def version() -> None:
    print(f"MetaEcho version {metaecho.__version__}")
