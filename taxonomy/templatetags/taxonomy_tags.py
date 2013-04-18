import logging
from django import template
from django.contrib.contenttypes.models import ContentType

from taxonomy.models import *

register = template.Library()
logger = logging.getLogger(__name__)

def get_taxonomy_for_object(parser, token):
    try:
        bits = tuple(token.split_contents())
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents.split()[0]
            )

    if len(bits) == 3:
        #sort of duplicate due to default value on TaxonomyMembers.__init__()
        var_name = "taxonomies"
    elif len(bits) == 5 and bits[3] == "as":
        var_name = bits[4]

    return TaxonomyForObject(bits[1], bits[2], var_name)

class TaxonomyForObject(template.Node):
    def __init__(self, taxonomy_group, obj, var_name="taxonomies"):
        # Most examples set variables using template.Variable here
        # and then resolve() in render().  I am doing both in render due to the
        # method call to easily deal with the potential for an arg being
        # a variable or a literal value.
        self.taxonomy_group = taxonomy_group
        self.obj = obj
        self.variable_name = var_name

    def render(self, context):
        resolved_obj = resolve_variable(self.obj, context)
        # resolved_name = resolve_variable(self.taxonomy_item, context)
        resolved_group = resolve_variable(self.taxonomy_group, context)
        ctype = ContentType.objects.get_for_model(resolved_obj)

        qs = TaxonomyMap.objects.filter(content_type=ctype)

        qs = qs.filter(object_id=resolved_obj.pk)
        taxonomy_items = TaxonomyItem.objects\
                .filter(pk__in=qs.values_list('taxonomy_item', flat=True))

        # taxonomy_item = TaxonomyItem.objects.get(name=resolved_name,
        #                                          taxonomy_group__name=resolved_group)
        context[self.variable_name] = taxonomy_items
        return ''

def get_taxonomy_members(parser, token):
    try:
        bits = tuple(token.split_contents())
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents.split()[0]
            )

    if len(bits) == 3:
        #sort of duplicate due to default value on TaxonomyMembers.__init__()
        var_name = "members"
    elif len(bits) == 5 and bits[3] == "as":
        var_name = bits[4]

    return TaxonomyMembers(bits[1], bits[2], var_name)

class TaxonomyMembers(template.Node):
    def __init__(self, taxonomy_group, taxonomy_item, var_name="members"):
        # Most examples set variables using template.Variable here
        # and then resolve() in render().  I am doing both in render due to the
        # method call to easily deal with the potential for an arg being
        # a variable or a literal value.
        self.taxonomy_group = taxonomy_group
        self.taxonomy_item = taxonomy_item
        self.variable_name = var_name

    def render(self, context):
        resolved_name = resolve_variable(self.taxonomy_item, context)
        resolved_group = resolve_variable(self.taxonomy_group, context)

        taxonomy_item = TaxonomyItem.objects.get(name=resolved_name,
                                                 taxonomy_group__name=resolved_group)
        context[self.variable_name] = taxonomy_item.get_members()
        return ''

def resolve_variable(arg, context):
    """Attempt to resolve a template param to a template variable value
    or return the param as is if it can't be resolved because it's a real value
    and not a variable"""

    try:
        value = template.Variable(arg).resolve(context)
    except template.VariableDoesNotExist:
        value = arg

    return value

register.tag('taxonomy_members', get_taxonomy_members)
register.tag('taxonomy_for_object', get_taxonomy_for_object)
