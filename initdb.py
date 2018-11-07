import os
from config import db
from models import LabTest

"""
Script to manually initialize Database

"""



# Data to initialize database with
labTests = [
    {
        "name": "S-TSH",
        "unit": "umg/ml",
        "value_min": "1,5",
        "value_max": "4"
    },
    {
        "name": "Hemoglobiini",
        "unit": "g/l",
        "value_min": "134",
        "value_max": "167"
    },
    {
        "name": "LDL-kolesteroli",
        "unit": "mmol/l",
        "value_min": "0",
        "value_max": "3"
    }
]

# Delete database file if it exists currently
if os.path.exists('rest_api.db'):
    os.remove('rest_api.db')

# Create the database
db.create_all()

# Itfdsafdadfa
for labTest in labTests:
    row = LabTest(name=labTest['name'],
                  unit=labTest['unit'],
                  value_min=labTest['value_min'],
                  value_max=labTest['value_max'])
    db.session.add(row)

db.session.commit()
