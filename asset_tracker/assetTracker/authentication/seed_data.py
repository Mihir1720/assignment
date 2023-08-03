# Seed(Fake Data Generator) file.
from django_seed import Seed
from authentication.models import CustomUser
from assetTracker.settings import SEED_SETTINGS
from django.contrib.auth.hashers import make_password

def seed_data():
    # Generate Fake data
    seeder = Seed.seeder()

    seeder.add_entity(CustomUser, 1, {
        'email': "admin@example.com",
        'password': make_password("admin@123"),
        'is_system_admin': True,
        'is_super_user': True
    })
    
    seeder.add_entity(CustomUser, SEED_SETTINGS, {
        'email': lambda x: seeder.faker.email(),
        'password': lambda x: make_password(seeder.faker.password()),
        'is_system_admin': lambda x: seeder.faker.boolean(),
    })

    seeder.execute()
