import csv
import os


class TopUsCities(object):
    """ Returns a name of a US city and state. e.g. "New York, NY".  """

    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.cities = []
        with open(os.path.join(path, 'US_Top5000Population.csv'), 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                self.cities.append(unicode('%s, %s' %(row[0], row[1].strip()), 'utf-8'))

    def __call__(self):
        return self.cities

class UKCounties(object):
    """ Returns a list of UK Counties. e.g. "Yorkshire".  """

    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.cities = []
        with open(os.path.join(path, 'uk_counties.txt'), 'rb') as txtfile:
            self.counties = txtfile.readlines()

    def __call__(self):
        return self.counties

class LondonBoroughs(object):
    """ Returns a list of London Boroughs. e.g. "Lambeth".  """

    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.cities = []
        with open(os.path.join(path, 'london_boroughs.txt'), 'rb') as txtfile:
            self.boroughs = txtfile.readlines()

    def __call__(self):
        return self.boroughs