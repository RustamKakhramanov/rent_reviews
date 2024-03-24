import random
from faker import Faker
from django.core.management.base import BaseCommand
from app.apps.core.models import TariffPlan, TelegramUser, Search
from django.utils import timezone

fake = Faker()

class Command(BaseCommand):
    help = 'Seed random test data into the database for another project'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding data for another project...'))

        # # Create Tariff Plans
        # for _ in range(5):  # Adjust the number based on how many Tariff Plans you want
        #     self.create_tariff_plan()

        # Create Telegram Users and associated Search Lists
        for _ in range(20):  # Adjust the number based on how many Telegram Users you want
            user = self.create_telegram_user()
            self.create_search_list(user)

        self.stdout.write(self.style.SUCCESS('Seed data for another project complete.'))

    def create_tariff_plan(self):
        name = fake.word()
        group_quantity = random.randint(1, 10)
        keyword_quantity = random.randint(1, 5)
        old_messages_offset = random.randint(1, 100)
        daemon_hours_quantity = random.randint(1, 24)

        TariffPlan.objects.create(
            name=name,
            group_quantity=group_quantity,
            keyword_quantity=keyword_quantity,
            old_messages_offset=old_messages_offset,
            daemon_hours_quantity=daemon_hours_quantity,
        )

    def create_telegram_user(self):
        telegram_username = fake.user_name()
        telegram_name = fake.name()
        phone_number = fake.phone_number()
        tariff_plan = TariffPlan.objects.order_by('?').first()  # Select a random Tariff Plan
        expired_at = timezone.now() + timezone.timedelta(days=random.randint(30, 365))

        return TelegramUser.objects.create(
            telegram_username=telegram_username,
            telegram_name=telegram_name,
            phone_number=phone_number,
            tariff_plan=tariff_plan,
            expired_at=expired_at,
            last_activity_at=timezone.now(),
        )

    def create_search_list(self, user):
        status = random.choice(['in_process', 'error', 'finished'])
        table_link = fake.url()

        Search.objects.create(
            user=user,
            status=status,
            table_link=table_link,
            searched_at=timezone.now(),
        )
