from argparse import ArgumentParser
from typing import Any

from django.core.management.base import BaseCommand

from cashviz.importer.update_database import update_database


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, _parser: ArgumentParser) -> None:
        pass

    def handle(self, *_args: tuple[Any], **_options: dict[Any, Any]) -> None:
        update_database()
