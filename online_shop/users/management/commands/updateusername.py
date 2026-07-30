from django.core.management.base import BaseCommand
from django.db import transaction

from online_shop.users.models import BaseUserModel


class Command(BaseCommand):
    """
    Update usernames for all users using bulk_update.
    """

    help = "Bulk update usernames."

    def add_arguments(self, parser) -> None:
        """
        Register command arguments.
        """
        parser.add_argument(
            "--prefix",
            type=str,
            required=True,
            help="Username prefix.",
        )

        parser.add_argument(
            "--batch-size",
            type=int,
            default=5000,
            help="Bulk update batch size.",
        )

    def handle(self, *args, **options) -> None:
        """
        Execute command.
        """
        prefix: str = options["prefix"]
        batch_size: int = options["batch_size"]

        queryset = BaseUserModel.objects.order_by("id")

        users_to_update = []

        for index, user in enumerate(queryset.iterator(chunk_size=batch_size), start=1):
            user.username = f"{prefix}{user.id}"
            users_to_update.append(user)

            if len(users_to_update) >= batch_size:
                self._bulk_update(users_to_update)
                self.stdout.write(
                    self.style.SUCCESS(f"{index} users updated.")
                )
                users_to_update.clear()

        if users_to_update:
            self._bulk_update(users_to_update)

        self.stdout.write(
            self.style.SUCCESS("Finished.")
        )

    @staticmethod
    @transaction.atomic
    def _bulk_update(users: list[BaseUserModel]) -> None:
        """
        Bulk update usernames.
        """
        BaseUserModel.objects.bulk_update(
            objs=users,
            fields=["username"],
        )