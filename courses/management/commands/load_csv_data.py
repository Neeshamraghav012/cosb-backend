from csv import DictReader
from django.core.management import BaseCommand


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
    
        # Show this if the data already exist in the database
        if Course.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading childrens data")


        #Code to load the data into database
        for row in DictReader(open('./coursea_data.csv')):

            link = f"https://www.coursera.org/search?query={str(row['name'])}"
            tags = row['name'].lower().split(' ')

            filtered_tag = []

            for i in tags:
                if i.isalpha():
                    filtered_tag.append(i)

            course = Course(name = row['name'], university = row['university'], overall_rating = row['overall_rating'], enrolls = row['enrolls'], platform = "Coursera", author = row["university"], link = link)
            course.save()
            course.tags.add(*filtered_tag)  
            course.save()
