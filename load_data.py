import csv
from datetime import date, datetime

from db_connect import db
from models import LibraryBook

session = db.session

with open('library.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:

        db.session.add(libraryBook)
    db.session.commit()
