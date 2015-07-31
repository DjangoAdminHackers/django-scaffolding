from __future__ import absolute_import

import os
import random
import re
import urllib
import datetime
import string
import time
import pytz

from scaffolding.library import lorem_ipsum
from scaffolding.library.london_postcodes import postcodes
from django.core.files import File
from scaffolding.library.names import ENGLISH_MALE_NAMES, ENGLISH_FEMALE_NAMES
from scaffolding.library.url import TopUrl


class Tube(object):
    """ The base class for scaffolding objects.
    """
    def __init__(self, **kwargs):
        pass

    def __iter__(self):
        return self
    
    def set_up(self, cls, count, **kwargs):
        """ This is a hook for doing validations 
            kwargs for future compatibility.
        """

    def next(self):
        raise NotImplementedError('You need to implement your own next method.')

#---------- custom classes -----------------

class StaticValue(Tube):
    """Always returns the same value"""

    def __init__(self, value):
        self.value = value
    def next(self):
        return self.value


class RandomValue(Tube):
    """Returns random values from the passed list"""
    def __init__(self, lst):
        self.lst = lst
    def next(self):
        return random.choice(self.lst)


class EveryValue(Tube):
    """
    Yields values from the passed iterable in order, looping into infinity.
    """
    def __init__(self, values, **kwargs):
        self.index = -1
        self.values = list(values)
        self.length = len(self.values)

    def next(self):
        if self.length == 0:
            raise StopIteration
        self.index += 1
        return self.values[self.index % self.length]


class OrNone(Tube):
    """
    Yields values from the passed class or None.
    """
    def __init__(self, cls, split=0.5, *args, **kwargs):
        self.split = split
        self.cls = cls(*args, **kwargs)


    def next(self):
        if random.random() > self.split:
            return None
        else:
            return self.cls.next()


class OrBlank(Tube):
    """
    Yields values from the passed class or "".
    """
    def __init__(self, cls, split=0.5, *args, **kwargs):
        self.split = split
        self.cls = cls(*args, **kwargs)


    def next(self):
        if random.random() > self.split:
            return ""
        else:
            return self.cls.next()


class Name(Tube):
    """ Generates a random name. <gender> can be 'male', 'female', 'm' or 'f'.
    """
    def __init__(self, max_length=30, gender=None, **kwargs):
        from scaffolding.library import names
        super(Name, self).__init__(**kwargs)
        self.max_length = max_length
        self.first_names = names.FirstNames(gender=gender)
        self.last_names = names.LastNames()

    def next(self):
        return u'%s %s'[:self.max_length] % (self.first_names.next(), self.last_names.next())


class ProductCategory(Tube):
    def __init__(self, max_length=30, **kwargs):
        from scaffolding.library import names
        super(ProductCategory, self).__init__(**kwargs)
        self.max_length = max_length
        self.categories = names.ProductCategories()

    def next(self):
        return u'%s'[:self.max_length] % (self.categories.next())


class FirstName(Name):
    """ Only returns first names. """
    def next(self):
        return u'%s'[:self.max_length] % self.first_names.next()


class LastName(Name):
    """ Only returns last names. """
    def next(self):
        return u'%s'[:self.max_length] % self.last_names.next()


class ProductName(Tube):
    """ Generates some plausible product names. """

    def __init__(self, **kwargs):
        from scaffolding.library import names
        from .library.names import Companies
        from scaffolding.library.booktitles import NOUNS
        super(ProductName, self).__init__(**kwargs)
        self.nouns = NOUNS
        self.companies = Companies()
        self.last_names = names.LastNames()

    def get_letter(self, count):
        return ''.join([chr(random.randrange(65, 65 + 26)) for x in range(0,count)])

    def get_number(self, count):
        return ''.join([chr(random.randrange(48, 48 + 10)) for x in range(0,count)])

    def get_name(self):
        return self.last_names.next()

    def get_noun(self):
        return random.choice(self.nouns)

    def get_company(self):
        return random.choice(self.companies())

    def get_code(self):
        return random.choice([
            self.get_letter(2)+self.get_number(4),
            self.get_letter(2)+self.get_number(1),
            self.get_letter(2),
            self.get_number(2)+self.get_letter(2),
        ])

    def next(self):
        return random.choice([
            '%s %s' % (self.get_company(), self.get_code()),
            # '%s %s %s' % (self.get_name(), self.get_noun(), self.get_code()),
            # '%s %s %s' % (self.get_name(), self.get_code(), self.get_noun()),
        ])


class CompanyName(Name):
    """ Generates some plausible company names. """

    def get_name(self):
        return u'%s' % self.last_names.next()

    def next(self):
        return random.choice([
            '%s and %s' % (self.get_name(), self.get_name())[:self.max_length],
            '%s-%s' % (self.get_name(), self.get_name())[:self.max_length],
            '%s Ltd.' % (self.get_name(),)[:self.max_length],
            '%s and Son' % (self.get_name())[:self.max_length],
            '%s Inc.' % (self.get_name())[:self.max_length],
            random.choice(lorem_ipsum.LOREM_IPSUM[0].split()).title(),
        ])


class RealCompanyName(RandomValue):
    def __init__(self):
        from .library.names import Companies
        companies = Companies()
        self.lst = companies()


class StreetAddress(Name):
    """ Generates some plausible street addresses. """

    def get_name(self):
        return u'%s' % self.last_names.next()

    def get_int(self):
        return str(random.randint(1,100))

    def next(self):
        return random.choice([
            '%s %s Street' % (self.get_int(), self.get_name())[:self.max_length],
            '%s %s Road' % (self.get_int(), self.get_name())[:self.max_length],
            '%s High Street' % (self.get_int(), )[:self.max_length],
            '%s %s Hill' % (self.get_int(), self.get_name())[:self.max_length],
            '%s Upper %s Street' % (self.get_int(), self.get_name())[:self.max_length],
            '%s %s House, %s Road' % (self.get_int(), self.get_name(), self.get_name())[:self.max_length],
        ])


class Noun(Tube):
    def __init__(self, **kwargs):
        from scaffolding.library.booktitles import NOUNS
        self.nouns = NOUNS

    def next(self):
        return random.choice(self.nouns)


class Verb(Tube):
    def __init__(self, **kwargs):
        from scaffolding.library.booktitles import VERBS
        self.verbs = VERBS

    def next(self):
        return random.choice(self.verbs)


class Word(Tube):
    def __init__(self, **kwargs):
        from scaffolding.library.booktitles import VERBS, NOUNS
        self.words = VERBS + NOUNS

    def next(self):
        return random.choice(self.words)


class RandomEmail(Tube):
    """ Return a random email. """

    def __init__(self, length=8, domains=None):
        self.index = -1
        self.length = length
        self.domains = domains or TopUrl()()
        self.names = ENGLISH_MALE_NAMES + ENGLISH_FEMALE_NAMES
        self.num_names = len(self.names)
        self.num_domains = len(self.names)
        random.shuffle(self.names)
        random.shuffle(self.domains)

    def next(self):
        if self.length == 0:
            raise StopIteration
        self.index += 1
        return u'{}@{}'.format(
            self.names[self.index % self.num_names].lower(),
            self.domains[self.index % self.num_domains],
        )


class BookTitle(Tube):
    def __init__(self, **kwargs):
        from scaffolding.library import booktitles
        super(BookTitle, self).__init__(**kwargs)
        self.title = booktitles.Title()

    def next(self):
        return self.title.next()


class LoremIpsum(Tube):
    """ Generates a Lorem Ipsum Text. The number of paragraphs is defined in paragraphs.
    """
    def __init__(self, paragraphs=7, max_length=None, text=lorem_ipsum.LOREM_IPSUM, **kwargs):
        super(LoremIpsum, self).__init__(**kwargs)
        self.text = text
        self.max_length = max_length
        self.paragraphs = paragraphs
        #  TODO: Loop paragraphs.
        if self.paragraphs > len(self.text):
            raise AttributeError('The Text %s only has %s paragraphs' %(text, len(text)))

    def next(self):
        if self.paragraphs < len(self.text):
            late_start = len(self.text) - self.paragraphs - 1
            start = random.randint(0, late_start)
        else:
            start = 0
        text = u'\n\n'.join(self.text[start:(start+self.paragraphs)])
        if self.max_length:
            return text[:self.max_length]
        return text


class RandomLoremIpsum(Tube):
    """ Generates a Lorem Ipsum Text. The number of paragraphs is defined in paragraphs.
    """
    def __init__(self, paragraphs=7, max_length=None, text=lorem_ipsum.LOREM_IPSUM, **kwargs):
        super(RandomLoremIpsum, self).__init__(**kwargs)
        random.shuffle(text)
        self.text = text
        for item in self.text:
            sentences = re.split(r' *[\.\?!][\'"\)\]]* *', item)
            random.shuffle(sentences)
            item = ''.join(sentences)

        self.max_length = max_length
        self.paragraphs = paragraphs
        #  TODO: Loop paragraphs.
        if self.paragraphs > len(self.text):
            raise AttributeError('The Text %s only has %s paragraphs' %(text, len(text)))

    def next(self):
        if self.paragraphs < len(self.text):
            late_start = len(self.text) - self.paragraphs - 1
            start = random.randint(0, late_start)
        else:
            start = 0
        text = u'\n\n'.join(self.text[start:(start+self.paragraphs)])
        if self.max_length:
            return text[:self.max_length]
        return text


class RandInt(Tube):
    """ Generates a random integer between min and max """
    def __init__(self, min, max, **kwargs):
        super(RandInt, self).__init__(**kwargs)
        self.min = min
        self.max = max

    def next(self):
        return random.randint(self.min, self.max)


class RandFloat(Tube):
    """ Generates a random float between min and max """
    def __init__(self, min, max, **kwargs):
        super(RandFloat, self).__init__(**kwargs)
        self.min = min
        self.max = max

    def next(self):
        return random.uniform(self.min, self.max)


class Contrib(object):
    """ Crates a Custom Object. The backend class is the first parameter.
        The backend class has to inherit from Tube.
    """
    def __init__(self, backend, **kwargs):
        self.backend = backend(**kwargs)

    def __iter__(self):
        return self.backend

    def next(self):
        return self.backend.next()

    def set_up(self, cls, count, **kwargs):
        if hasattr(self.backend, 'set_up'):
            self.backend.set_up(cls, count, **kwargs)
        else:
            pass


class AlwaysTrue(StaticValue):
    """ Always returns True."""
    def __init__(self):
        self.value = True


class AlwaysFalse(StaticValue):
    """ Always returns False."""
    def __init__(self):
        self.value = False


class TrueOrFalse(RandomValue):
    """ Randomly returns true or false.
        You can set a ratio for true or false by specifying true and false:
        e.g. true=1, false=3 returns 3 times as many False than Trues.
    """
    def __init__(self, true=1, false=1):
        self.lst = [True for i in range(true)]
        self.lst.extend([False for i in range(false)])


class RandomInternetImage(Tube):
    """ Creates a random image for an ImageField using an internet source.
    """
    def __init__(self, backend, **kwargs):
        super(RandomInternetImage, self).__init__(**kwargs)
        self.backend = backend(**kwargs)

    def next(self):
        # returns a filename and File object, ready to be fed to the image.save() method.
        url = self.backend.next()
        temp_image = urllib.urlretrieve(url)
        return os.path.basename(url), File(open(temp_image[0]))


class ForeignKey(EveryValue):
    """ Creates a foreign key assigning items from the queryset.
    """
    def __init__(self, queryset, chunksize=100, **kwargs):
        self.index = -1
        self.queryset = queryset[:chunksize]

    def next(self):
        length = self.queryset.count()
        if length == 0:
            raise StopIteration
        self.index += 1
        return self.queryset[self.index % length]


class ForeignKeyOrNone(OrNone):
    """ Maybe creates a foreign key, otherwise None.
        split is the weight for positives. 0.2 yields 80% None.
    """
    def __init__(self, **kwargs):
        super(ForeignKeyOrNone, self).__init__(cls=ForeignKey, **kwargs)


class RandomDate(Tube):
    """ Creates a date between startdate and enddate  """
    def __init__(self, startdate, enddate, **kwargs):
        super(RandomDate, self).__init__(**kwargs)
        if not (isinstance(startdate, datetime.date) and
                isinstance(enddate, datetime.date)):
            raise AttributeError(
                "startdate and enddate must be instances of datetime.date")
        if enddate < startdate:
            raise AttributeError(
                "enddate must be after startdate"
            )
        self.startdate = startdate
        self.enddate = enddate

    def next(self):
        delta = (self.enddate - self.startdate).days
        return self.startdate + datetime.timedelta(random.randint(0, delta))


class RandomDateTime(RandomDate):

    def next(self):
        new_date = super(RandomDateTime, self).next()
        new_datetime = datetime.datetime.combine(new_date, datetime.time())
        new_datetime += datetime.timedelta(minutes=random.randint(0, 3)*15)
        return pytz.utc.localize(new_datetime)


def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Converts an integer to a base36 string."""
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    base36 = ''
    sign = ''
    if number < 0:
        sign = '-'
        number = -number
    if 0 <= number < len(alphabet):
        return sign + alphabet[number]
    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36
    return sign + base36


class UniqueCode(Tube):
    """ Generates a (probably) unique uppercase alphanumeric code. max length is 9"""
    def __init__(self, max_length=9):
        self.max_length = max_length if max_length<=9 else 9

    def next(self):
        t = int(time.time()*10000)
        str = base36encode(t)
        return str[-self.max_length:]


class USCity(RandomValue):
    def __init__(self):
        from .library.geo import TopUsCities
        top_us = TopUsCities()
        self.lst = top_us()


class UKCounty(RandomValue):
    def __init__(self):
        from .library.geo import UKCounties
        uk_counties = UKCounties()
        self.lst = uk_counties()


class LondonBorough(RandomValue):
    def __init__(self):
        from .library.geo import LondonBoroughs
        london_boroughs = LondonBoroughs()
        self.lst = london_boroughs()


class UKPhone(Tube):
    """ Generates a valid UK phone number without the country code
    London only at the moment
    """
    def __init__(self):
        self.max_length = 13

    def next(self):
        return '020 {:04d} {:04d}'.format(random.randint(0, 9999), random.randint(0, 99))


class LondonPostcode(Tube):
    """ Returns a list of London Postcodes (i.e. WC1)"""

    def __init__(self):
        self.postcodes = postcodes

    def next(self):
        letters = string.ascii_letters[26:]
        return "%s %s%s%s" % (
            random.choice(self.postcodes),
            random.randint(1,9),
            random.choice(letters),
            random.choice(letters)
        )


class URL(RandomValue):
    def __init__(self, prefix='http://'):
        from .library.url import TopUrl
        urls = TopUrl(prefix=prefix)
        self.lst = urls()


class Callable(Tube):
    """ Sets a field based on the value of another field """
    def __init__(self, fn, param=None):
        self.fn = fn
        self.param = param
    def next(self):
        return (self.fn(self.param))


class OtherField(Tube):
    """ Sets a field based on the value of another field """
    def __init__(self, field, fn):
        self.field = field
        self.fn = fn
    def next(self):
        return (self.field, self.fn)
