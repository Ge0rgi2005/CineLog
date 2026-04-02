from django.db import migrations


def create_groups(apps, schema_editor):
    group = apps.get_model('auth', 'Group')
    permission = apps.get_model('auth', 'Permission')

    # Create Critics group
    critics_group, _ = group.objects.get_or_create(name='Critics')
    critic_permissions = permission.objects.filter(
        codename__in=[
            'add_review', 'change_review', 'delete_review',
            'add_film', 'change_film',
            'add_castmember', 'change_castmember',
        ]
    )
    critics_group.permissions.set(critic_permissions)

    members_group, _ = group.objects.get_or_create(name='Members')
    member_permissions = permission.objects.filter(
        codename__in=[
            'add_review', 'change_review', 'delete_review',
            'add_watchlist', 'change_watchlist', 'delete_watchlist',
        ]
    )
    members_group.permissions.set(member_permissions)


def delete_groups(apps, schema_editor):
    group = apps.get_model('auth', 'Group')
    group.objects.filter(name__in=['Critics', 'Members']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]