import logging
import os
from pathlib import Path
from typing import Optional

import typer
from aleph.sdk.account import _load_account
from aleph.sdk.chains.common import generate_key
from aleph.sdk.types import AccountFromPrivateKey

from aleph_client.commands import help_strings
from aleph_client.commands.utils import setup_logging
from aleph_client.conf import settings

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def create(
    from_private_key: Optional[str] = typer.Option(None, help=help_strings.PRIVATE_KEY),
    debug: bool = False,
):
    """Create or import a private key."""

    setup_logging(debug)

    typer.echo("Generating private key file.")
    private_key_file = typer.prompt(
        "Enter file in which to save the key", settings.PRIVATE_KEY_FILE
    )

    if os.path.exists(private_key_file):
        typer.echo(f"Error: key already exists: '{private_key_file}'")
        exit(1)

    private_key = None
    if from_private_key is not None:
        account: AccountFromPrivateKey = _load_account(private_key_str=from_private_key)
        private_key = from_private_key.encode()
    else:
        private_key = generate_key()

    if private_key is None:
        typer.echo("An unexpected error occurred!")
        exit(1)

    os.makedirs(os.path.dirname(private_key_file), exist_ok=True)
    with open(private_key_file, "wb") as prvfile:
        prvfile.write(private_key)
        typer.echo(f"Private key created => {private_key_file}")


@app.command()
def address(
    private_key: Optional[str] = typer.Option(
        settings.PRIVATE_KEY_STRING, help=help_strings.PRIVATE_KEY
    ),
    private_key_file: Optional[Path] = typer.Option(
        settings.PRIVATE_KEY_FILE, help=help_strings.PRIVATE_KEY_FILE
    ),
):
    """
    Display your public address.
    """

    if private_key is not None:
        private_key_file = None
    elif private_key_file and not private_key_file.exists():
        typer.echo("No private key available", color=typer.colors.RED)
        raise typer.Exit(code=1)

    account: AccountFromPrivateKey = _load_account(private_key, private_key_file)
    typer.echo(account.get_address())


@app.command()
def private_key(
        private_key: Optional[str] = typer.Option(
            settings.PRIVATE_KEY_STRING, help=help_strings.PRIVATE_KEY
        ),
        private_key_file: Optional[Path] = typer.Option(
            settings.PRIVATE_KEY_FILE, help=help_strings.PRIVATE_KEY_FILE
        ),
):
    """
        Display your private key.
        """

    if private_key is not None:
        private_key_file = None
    elif private_key_file and not private_key_file.exists():
        typer.echo("No private key available", color=typer.colors.RED)
        raise typer.Exit(code=1)

    account: AccountFromPrivateKey = _load_account(private_key, private_key_file)
    typer.echo(account.)


@app.command()
def path():
    if settings.PRIVATE_KEY_FILE:
        print(settings.PRIVATE_KEY_FILE)
