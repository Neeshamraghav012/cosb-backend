from csv import DictReader
from django.core.management import BaseCommand
import random

from courses.models import Course


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from children.csv"

    def handle(self, *args, **options):
    
        """
        # Show this if the data already exist in the database
        if Course.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        """
            
        # Show this before loading the data into the database
        print("Loading childrens data")


        #Code to load the data into database
        for row in DictReader(open('./Udemy_Courses.csv')):


            link = f"https://www.udemy.com{row['link']}"
            tags = row['name'].lower().split(' ')

            filtered_tag = []

            for i in tags:
                if i.isalpha():
                    filtered_tag.append(i)

            course = Course(name = row['name'], overall_rating = random.randint(0, 5), enrolls = random.randint(10000, 1000000), platform = row['platform'], author = row["author"], link = link, price = 500, image = row['image'], image_mobile = row['image_mobile'], description = row['description'])
            course.save()
            course.tags.add(*filtered_tag)  
            course.save()
