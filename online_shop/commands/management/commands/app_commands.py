from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run all project commands."

    def handle(self, *args, **options) -> None:
        self.stdout.write("Running command 1...")
        call_command("command1")

        self.stdout.write("Running command 2...")
        call_command("command2")

        self.stdout.write("Running command 3...")
        call_command("command3")

        self.stdout.write(self.style.SUCCESS("All commands finished."))