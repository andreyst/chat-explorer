from django.core.management.base import BaseCommand, CommandError
from explorer.models import Chat
from explorer.tasks import sync_telegram_chat

class Command(BaseCommand):
    help = 'Send manual command to sync chat'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--user-id', required=True, type=int)
        parser.add_argument('-a', '--account-id', required=True, type=int)
        parser.add_argument('-r', '--remote-id', required=True, type=int)

    def handle(self, *args, **options):
        chat = Chat.objects.get(
          user=options['user_id'],
          account_id=options['account_id'],
          remote_id=options['remote_id'],
        )

        sync_telegram_chat.delay(chat.id, chat.update_generation)

        # for poll_id in options['poll_ids']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
