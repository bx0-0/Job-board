from blog.models import Category
jobs = [
    "Agriculture, Food, and Natural Resources",
    "Architecture and Construction",
    "Arts, Audio/Video Technology, and Communication",
    "Business and Finance",
    "Education and Training",
    "Government and Public Administration",
    "Health Science",
    "Hospitality and Tourism",
    "Human Services",
    "Information Technology",
    "Law, Public Safety, Corrections, and Security",
    "Manufacturing",
    "Marketing, Sales, and Service",
    "Science, Technology, Engineering, and Mathematics",
    "Transportation, Distribution, and Logistics",
    "other",
]
for job in jobs:
    Category.objects.create(name=job)
