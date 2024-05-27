from django.core.management.base import BaseCommand
from testapp.models import User  # 替换为你的应用程序中的 User 模型

class Command(BaseCommand):
    help = 'Delete all users'

    def handle(self, *args, **kwargs):
        # 删除所有用户
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all users.'))

