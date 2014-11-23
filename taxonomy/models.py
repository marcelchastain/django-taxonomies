'''
Flexible generic models for grouping/relating objects into taxonomic structures
Notes:

TODO:
    - need to add some showroom ownership in this
    - need to make sure that erasing taxonomies won't nuke the objects
    - need some way to add meta information to a taxonomy, like "display name"
'''
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save


class TaxonomyGroup(models.Model):
    """
    Highest level of taxonomy.  This is the name assigned to the list of
    related taxonomy items

    >>> tgroup = TaxonomyGroup.objects.create(name='age')
    """
    name = models.CharField(max_length=75, db_index=True)
    display_name = models.CharField(max_length=150, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        #Seems the most likely wanted ordering for anyone... and it's what I want
        ordering = ['display_name']

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.name
        return super(TaxonomyGroup, self).save(*args, **kwargs)


class TaxonomyItem(models.Model):
    """
    An actual categorization which would be assigned to some instance

    >>> tgroup = TaxonomyGroup.objects.create(name='age')
    >>> item = TaxonomyItem.objects.create(taxonomy_group=tgroup, name='baby')
    """
    taxonomy_group = models.ForeignKey(TaxonomyGroup, db_index=True)
    parent = models.ForeignKey('TaxonomyItem', blank=True, null=True, db_index=True)
    name = models.CharField(max_length=75, db_index=True)

    def __unicode__(self):
        if self.parent:
            return u"%s's %s" % (self.parent.name.title(), self.name)
        return u'%s' % self.name

    def get_children(self):
        return (TaxonomyItem.objects\
                .filter(taxonomy_group=self.taxonomy_group)
                .filter(parent=self))

    def get_members(self):
        """Returns a list of objects that have this item as
        part of their taxonomy.  This returns the actual models and not
        the TaxonomyMap item."""

        tmap = self.taxonomymap_set.all()
        return [i.content_object for i in tmap]

    def add_member(self, instance):
        """Add a mapping of this taxon to the instance.
        This is a shortcut to avoid messing with the TaxonomyMap objects
        and the extra complexities of setting the correct values for
        GenericForeignKey."""

        #Need to throw exception if model is missing, etc
        model_type = ContentType.objects.get_for_model(instance)
        tmap, created = TaxonomyMap.objects.get_or_create(
                    content_type=model_type,
                    object_id=instance.id,
                    taxonomy_item=self)
        return tmap

    class Meta:
        #Again, seems the most likely wanted ordering for anyone and it's what I want
        ordering = ['name']

class TaxonomyMap(models.Model):
    """
    Map instances to a TaxonomyItem

    >>> tgroup = TaxonomyGroup.objects.create(name='age')
    >>> item = TaxonomyItem.objects.create(taxonomy_group=tgroup, name='baby')
    >>> instance = ContactRecord.objects.first()
    >>> ctype = ContentType.objects.get_for_model(instance)
    >>> tmap = TaxonomyMap.objects.create(taxonomy_item=item,
                    content_type=ctype, object_id=instance.pk)
    """
    taxonomy_item = models.ForeignKey(TaxonomyItem, db_index=True)
    content_type = models.ForeignKey(ContentType, db_index=True)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type','object_id')

    def __unicode__(self):
        return u'%s - %s' %(self.taxonomy_item, self.content_object)

    @classmethod
    def post_save(cls, sender, instance, created, raw, **kwargs):
        ''' send post_save signal on the related object'''
        if raw:
            # loading data from a fixture or something unsafe
            return

        obj = instance.content_object
        post_save.send(sender=obj.__class__, instance=obj)

class TaxonomyMember(models.Model):
    """An abstract class that models can inherit from to be taxonomized."""
    def get_taxonomies(self, group):
        """Get a list of TaxonomyItem objects for an object and TaxonomyGroup"""
        #Throw exception for missing model or group?
        type = ContentType.objects.get_for_model(self)
        tmap = TaxonomyMap.objects.filter(object_id=self.pk,
                                          taxonomy_item__taxonomy_group=group)

        return [i.taxonomy_item for i in tmap]

    def get_taxonomy_items_by_group(self, group_name):
        ctype = ContentType.objects.get_for_model(self)
        tgroup = TaxonomyGroup.objects.get(name=group_name)
        return TaxonomyItem.objects.filter(taxonomy_group=tgroup,
                                    taxonomymap__content_type=ctype,
                                    taxonomymap__object_id=self.pk)

    def get_taxonomy_groups(self):
        """Get a list of TaxonomyGroup objects that the
        subclassed object belongs to."""
        tgroups = TaxonomyGroup.objects.filter(
                    taxonomyitem__taxonomymap__object_id=self.pk,
                    content_type=ContentType.objects.get_for_model(self)).distinct()
        return list(tgroups)

    class Meta:
        abstract = True



post_save.connect(TaxonomyMap.post_save, sender=TaxonomyMap)
