# coding=utf-8

from collections import OrderedDict

from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.db.models import loading

import scaffolding


import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = '<app_label.model_name> <count>'
    help = 'Creates placeholder data for your models.'

    def handle(self, *args, **options):

        if not args or len(args) != 2:
            raise CommandError('Do: scaffold <app_label.model_name> <count>')

        app_label, separator, model_name = args[0].partition('.')
        count = int(args[1])

        do_scaffold(app_label, model_name, count)


def do_scaffold(app_label, model_name, count):

    if model_name:
        # We've specified a single model
        model = loading.get_model(app_label, model_name)

        if not isinstance(model, models.base.ModelBase):
            raise CommandError('%s is not a Django model.' % model)

        models_list = [model]

    else:
        # No model specified. Scaffold all of them.
        scaffolds = scaffolding.all_scaffolds()
        app = loading.get_app(app_label)
        app_models = loading.get_models(app)
        models_list = []
        for key, value in scaffolds.items():
            if key in app_models:
                models_list.append(key)


    for model in models_list:

        print u'Creating %s\n' % model

        factory = make_factory(model, count)

        if factory.get('_initialize_all', False):
            factory['_initialize_all'](model)

        new_objects = []

        for i in range(count):
            if i%100==0 and i>0:
                print u'Created %s\n' % i
            new_objects.append(make_object(model, factory))

        if factory.get('_finalize_all', False):
            factory['_finalize_all'](model, new_objects)

        print u'\nCreated %s %s\n' % (count, model._meta.verbose_name_plural)

def make_factory(cls, count):
    """ Get the generators from the Scaffolding class within the model.
    """
    factory = OrderedDict()
    text = []
    scaffold = scaffolding.scaffold_for_model(cls)
    try:
        field_names = scaffold.field_order
    except AttributeError:
        field_names = cls._meta.get_all_field_names()

    for field_name in field_names:
        generator = getattr(scaffold, field_name, None)
        if generator:
            if hasattr(generator, 'set_up'):
                generator.set_up(cls, count)
            factory[field_name] = generator
            text.append(u'%s: %s; ' % (field_name, factory[field_name]))

    if hasattr(scaffold, 'initialize_all') and hasattr(scaffold.initialize_all, '__call__'):
        factory['_initialize_all'] = scaffold.initialize_all

    if hasattr(scaffold, 'initialize') and hasattr(scaffold.initialize, '__call__'):
        factory['_initialize'] = scaffold.initialize

    if hasattr(scaffold, 'finalize') and hasattr(scaffold.finalize, '__call__'):
        factory['_finalize'] = scaffold.finalize

    if hasattr(scaffold, 'finalize_all') and hasattr(scaffold.finalize_all, '__call__'):
        factory['_finalize_all'] = scaffold.finalize_all

    return factory

def make_object(cls, fields):

    obj = cls()
    initialize = fields.get('_initialize', None)
    finalize = fields.get('_finalize', None)

    if initialize:
        initialize(obj)

    for field_name, generator in fields.items():
        if not field_name in ['_initialize_all', '_initialize', '_finalize', '_finalize_all']:
            # Some custom processing
            field = cls._meta.get_field(field_name)
            value = generator.next()
            if isinstance(field, models.fields.related.ForeignKey) and isinstance(value, int):
                field_name = u'%s_id' % field_name
            if isinstance(generator, scaffolding.OtherField):
                # Special handling for OtherField tube
                source_field = value[0]
                fn = value[1]
                calc_value = fn(getattr(obj, source_field))
                setattr(obj, field_name, calc_value)
            else:
                # Normal tube handling
                if isinstance(field, models.fields.files.FileField):
                    getattr(obj, field_name).save(*value, save=False)
                else:
                    setattr(obj, field_name, value)

    obj.save()

    if finalize:
        finalize(obj)

    return obj
