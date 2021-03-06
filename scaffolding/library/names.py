# -*- coding: utf-8 -*-
import os
import random
import codecs

ENGLISH_MALE_NAMES = ['Jacob', 'Ethan', 'Michael', 'Alexander', 'William', 'Joshua', 'Daniel',
                 'Jayden', 'Noah', 'Anthony', 'Jonathan', 'David', 'John', 'Mark', 'Calvin',
                 'Jeremy', 'Ethan', 'Phillip', 'Brian', 'Isaac', 'Abraham', 'Jesse', 'Lawrence',
                 'Jeffrey', 'Steve', 'Paul', 'Robert', 'Winston', 'Ken', 'Caleb', 'George',
                 'Brent', 'Joseph', 'Ian', 'Peter', 'Luke', 'Ted', 'Andrew', 'Joe', 'Dennis',
                 'Bill', 'Felix', 'Don', 'Oliver', 'Harry', 'Samuel', 'Justin', 'Brooks', 'Nathan']

ENGLISH_FEMALE_NAMES = ['Isabella', 'Emma', 'Olivia', 'Sophia', 'Ava', 'Emily', 'Madison',
                   'Abigail', u'Chloe', 'Mia', 'Alice', 'Helen', 'Grace', 'Joanna', 'Ann',
                   'Lisa', 'Lily', 'May', 'June', 'April', 'Jane', 'Elise', 'Kristy',
                   'Katie', 'Kathy', 'Julie', 'Jamie', 'Carol', 'Carrie', 'Elizabeth',
                   'Robin', 'Sally', 'Jackie', 'Sherry', 'Christine', 'Angela', 'Judy', 
                   'Ruth', 'Brooke', 'Megan', 'Dawn', 'Rebecca', 'Esther', 'Claire']

class FirstNames(object):
    """ can iterate over names for the given gender.
    """
    def __init__(self, gender=None, male_names=ENGLISH_MALE_NAMES,
                 female_names=ENGLISH_FEMALE_NAMES, *args, **kwargs):
        self.gender = gender
        if gender in ['male', 'm']:
            self.first_names = male_names
        elif gender in ['female', 'f']:
            self.first_names = female_names
        else:
            self.first_names = male_names + female_names
            random.shuffle(self.first_names)
        self.index = 0
        self.length = len(self.first_names)

    def __iter__(self):
        return self

    def next(self):
        self.index += 1
        return self.first_names[self.index % self.length]


GERMAN_LAST_NAMES = [u'Müller', u'Schmid', u'Schneider', u'Fischer', u'Weber', u'Meyer',
                     u'Wagner', u'Becker', u'Schutz', u'Hoffmann', u'Schäfer',
                     u'Koch', u'Bauer', u'Richter', u'Bächler', u'Kestenholz']
                     
ASIAN_LAST_NAMES = ['Wang', 'Chen', 'Chou', 'Tang', 'Huang', 'Liu', 'Shih', 'Su', 'Song',
                    'Lin', 'Yu', 'Yang', 'Chan', 'Tsai', 'Wong', 'Hsu', 'Chang', 'Cheng',
                    'Park', 'Kim', 'Choi', 'Kang', 'Hwang']

ENGLISH_LAST_NAMES = ['Smith', 'Walker', 'Conroy', 'Stevens', 'Jones', 'Armstrong', 'Johnson',
                 'White', 'Olson', 'Ellis', 'Mitchell', 'Forrest', 'Baker', 'Portman',
                 'Davis', 'Clark', 'Roberts', 'Jackson', 'Marshall', 'Decker', 'Brown']

SPANISH_LAST_NAMES = [u'Rodríguez', u'González', u'Hernández', 'Morales', u'Rojas', u'López',
                      u'García', u'Fernández', u'Martínez', u'Sánchez', u'Álvarez', u'Moreno',
                      u'Martín', u'Abrego', u'Castillo', u'Diaz', u'Perez',]

FRENCH_LAST_NAMES = [u'Martin', u'Bernard', u'Dubois', u'Thomas', u'Robert', u'Richard', u'Petit',
                     u'Durand', u'Leroy', u'Moreau', u'Simon', u'Laurent', u'Lefebvre', u'Michel',
                     u'Garcia', u'David', u'Bertrand', u'Roux', u'Vincent', u'Fournier', u'Morel',
                     u'Girard', u'André', u'Lefèvre', u'Mercier', u'Dupont', u'Lambert', u'Bonnet',
                     u'François']

class LastNames(object):
    """ Keeps returning last names
    """
    def __init__(self, last_names=GERMAN_LAST_NAMES+ASIAN_LAST_NAMES+ENGLISH_LAST_NAMES+
                                  SPANISH_LAST_NAMES+FRENCH_LAST_NAMES, *args, **kwargs):
        self.last_names = last_names
        self.index = 0
        self.length = len(self.last_names)

    def __iter__(self):
        return self

    def next(self):
        self.index += 1
        return self.last_names[self.index % self.length]

class Companies(object):

    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.companies = []
        with codecs.open(os.path.join(path, 'companies.txt'), encoding='utf-8', mode='rb') as txtfile:
            self.companies = [line.rstrip() for line in txtfile]

    def __call__(self):
        return self.companies


PRODUCT_CATEGORIES = ['Cameras', 'Lighting', 'Lenses', 'Grips', 'Playback', 'Power', 'Tripods', 'Accessories', 'Amplifiers', 'Mixers', 'Monitors']

class ProductCategories(object):
    def __init__(self, categories=PRODUCT_CATEGORIES, *args, **kwargs):
        self.categories = categories
        self.index = 0
        self.length = len(self.categories)

    def __iter__(self):
        return self

    def next(self):
        self.index += 1
        return self.categories[self.index % self.length]
