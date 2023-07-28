# Seed(Fake Data Generator) file.
from django_seed import Seed
from authentication.models import CustomUser
from assetTracker.settings import SEED_SETTINGS

def seed_data():
    # Generate Fake data
    seeder = Seed.seeder()
    
    seeder.add_entity(CustomUser, SEED_SETTINGS, {
        'email': lambda x: seeder.faker.email(),
        'password': lambda x: seeder.faker.password(),
        'is_system_admin': lambda x: seeder.faker.boolean(),
    })

    seeder.execute()
