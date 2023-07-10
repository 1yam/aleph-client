"""
Aleph Client command-line interface.
"""

import typer

from .commands import account, aggregate, files, message, program

app = typer.Typer()

app.add_typer(account.app, name="account", help="Manage account")
app.add_typer(
    aggregate.app, name="aggregate", help="Manage aggregate messages on aleph.im"
)

app.add_typer(
    files.app, name="file", help="File uploading and pinning on IPFS and aleph.im"
)
app.add_typer(
    message.app,
    name="message",
    help="Post, amend, watch and forget messages on aleph.im",
)
app.add_typer(
    program.app, name="program", help="Upload and update programs on aleph.im VM"
)


if __name__ == "__main__":
    app()
