from django.core.management.base import BaseCommand
from api.models import Message


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Clear existing data
        Message.objects.all().delete()

        # Create seed data
        messages = [
            "Hello World from Django Backend!",
            "This is a seeded message for development",
            "Database connection is working perfectly",
            "CI/CD pipeline is configured and ready",
            "PostgreSQL integration successful",
        ]

        for content in messages:
            Message.objects.create(content=content)
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {content[:50]}...'))

        total = Message.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully seeded {total} messages'))
