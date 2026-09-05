from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create default admin user (admin@mmust.ac.ke). Idempotent.'

    def handle(self, *args, **options):
        User = get_user_model()
        email = 'admin@mmust.ac.ke'
        password = 'mmust1234'
        user = User.objects.filter(email=email).first()
        if user:
            self.stdout.write(self.style.WARNING(f'Admin user already exists: {email}'))
            # ensure flags are set
            updated = False
            if not user.is_staff:
                user.is_staff = True
                updated = True
            if not user.is_superuser:
                user.is_superuser = True
                updated = True
            if getattr(user, 'role', None) != 'admin':
                try:
                    user.role = 'admin'
                    updated = True
                except Exception:
                    pass
            if updated:
                user.save()
                self.stdout.write(self.style.SUCCESS('Admin user flags updated.'))
            return

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name='System',
            last_name='Administrator',
        )
        try:
            user.role = 'admin'
        except Exception:
            pass
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Created admin user: {email}'))
