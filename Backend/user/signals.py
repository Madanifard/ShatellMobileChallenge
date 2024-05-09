from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def create_default_group(sender, **kwargs):
    '''
    if signal post migrate of user app 
    create 3 group: super_user, admin_user, user
    super_user: access all project
    admin_user: access user section
    client_user: access profile app
    '''
    if sender.name == 'django.contrib.auth':
        
        group_super_user, create_super_user = Group.objects.get_or_create(name='super_user')
        if create_super_user:
            permissions = Permission.objects.all()
            group_super_user.permissions.add(*permissions)


        group_admin, created_admin = Group.objects.get_or_create(name='admin_user')
        if created_admin:
            permissions = Permission.objects.filter(content_type__app_label='user')
            group_admin.permissions.add(*permissions)
        
        # group_client, created_admin = Group.objects.get_or_create(name='client_user')

        # if group_client:
        #     # Retrieve permissions you want to assign (replace 'app_label' with your app's label)
        #     permissions = Permission.objects.filter(content_type__app_label='profile')
        #     # Add permissions to the group
        #     group_admin.permissions.add(*permissions)


