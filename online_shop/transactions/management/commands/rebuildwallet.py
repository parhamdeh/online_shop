from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    command for return true transactions
    """
    help = "calculate balance for wallets"

    def add_arguments(self, parser) -> None:
            """
            Register command arguments.
            """
            parser.add_argument(
                "--user-id",
                type=int,
                required=True,
                help="user id",
            )

    def handle(self, *args, **options):
        ...