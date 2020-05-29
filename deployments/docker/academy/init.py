import os 
from django.contrib.auth.models import User
from accounting.models import Plans
import logging
import getpass

def init_script():
    plans = [
        {
        'name' : 'Basic',
        'price' : 'Free',
        'description': 'Access to Academy',
        'option1': 'Free Meetings',
        'option2': '1 Pynote',
        'option3': '5 hourse services',
        },

        {
        'name' : 'Pro',
        'price' : '24.99',
        'description': 'Acccess to Academy',
        'option1': 'Access to FuchiCorp Meetings',
        'option2': '5 Pynote',
        'option3': 'Unlimuted Service',
        },

        {
        'name' : 'Premium',
        'price' : '49.99',
        'description': 'Access to Academy',
        'option1': 'Access to all Videos',
        'option2': 'Unlimited Pynote',
        'option3': 'Custom domain name',
        },
        ]

    for plan in plans:
        if db_table_exists('accounting_plans'):
            if not Plans.objects.filter(name=plan['name']).exists():
                plan_class = Plans(
                    name=plan['name'], 
                    price=plan['price'],
                    description=plan['description'],
                    option1=plan['option1'],
                    option2=plan['option2'],
                    option3=plan['option3'],
                    )
                plan_class.save()

    ## Init script which is responsible to create admin user
    if os.environ.get('ADMIN_USER') and os.environ.get('ADMIN_PASSWORD'):

        ## If table is exist in system 
        if db_table_exists('auth_user'):
            
            ## IF user not created in system init script will go ahead and try to create
            if not User.objects.filter(username=os.environ.get('ADMIN_USER')).exists():
                super_user = User.objects.create_user(os.environ.get('ADMIN_USER'), password=os.environ.get('ADMIN_PASSWORD'))
                super_user.is_superuser=True
                super_user.is_staff=True
                super_user.save()
                logging.warning(f"admin user <{os.environ.get('ADMIN_USER')}> has been created !!")

    ## Setting up the kube config file for academy
    if os.path.isfile('bash/kube-confiig-setup.sh'):
        if str(getpass.getuser()).lower() == 'root':
            if not os.path.isdir('/root/.kube'):
                os.mkdir('/root/.kube')
            os.system("bash bash/kube-confiig-setup.sh")
        else:
            logging.warning("Skiping the kube config set up!!")

def db_table_exists(table_name, cursor=None):
    ## Function to check table exist or not
    try:
        
        ## Trying to connect to DB 
        if not cursor:
            from django.db import connection
            cursor = connection.cursor()
        if not cursor:
            raise Exception
        return table_name in connection.introspection.table_names()
    except:
        raise Exception("unable to determine if the table '%s' exists" % table_name)