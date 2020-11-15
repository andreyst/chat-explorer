from django.core.management.base import BaseCommand, CommandError
from explorer.models import Chat
from explorer.tasks import sync_telegram_chat

class Command(BaseCommand):
    help = 'Send manual command to sync chat'

    def add_arguments(self, parser):
        parser.add_argument('--id', required=True, type=int)

    def handle(self, *args, **options):
        chat = Chat.objects.get(pk=options['id'])

        sync_telegram_chat.delay(chat.id, chat.update_generation)
