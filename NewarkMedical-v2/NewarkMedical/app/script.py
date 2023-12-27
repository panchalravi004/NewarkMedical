from app.models import *

dept = [
    'Emergency',
    'Intensive Care',
    'Surgery',
    'Radiology',
    'Laboratory',
    'Physical',
    'Pharmacy',
    'Mental',
    'Oncology',
    'Orthopedics',
    'Neurology',
    'Cardiology',
    'Endocrinology',
    'Gastroenterology',
    'Dermatology',
    'Ophthalmology',
    'Rheumatology',
    'Pulmonology',
    'Infectious',
    'Nephrology',
    'General'
    ]

def create():
    newDept = []
    for d in dept:
        record = Department(
            name=str(d) 
        )
        newDept.append(record)
    Department.objects.bulk_create(newDept)