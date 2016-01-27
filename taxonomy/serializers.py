from rest_framework import serializers, pagination
from .models import (TaxonomyGroup, TaxonomyItem, TaxonomyMap)


class RecursiveField(serializers.Serializer):
    def to_native(self, value):
        return self.parent.to_native(value)

class TaxonomyItemSerializer(serializers.ModelSerializer):
    taxonomy_group_name = serializers.Field(source='taxonomy_group.name')
    taxonomy_group_display_name = serializers.Field(source='taxonomy_group.display_name')
    parent_name = serializers.Field(source='parent.name')
    map_count = serializers.SerializerMethodField('get_map_count')

    class Meta:
        model = TaxonomyItem
        fields = ('id', 'taxonomy_group', 'parent', 'name', 'map_count',
                'taxonomy_group_name', 'taxonomy_group_display_name',
                'parent_name',)

    def get_map_count(self, obj):
        return obj.taxonomymap_set.count()


class MinimalTaxonomyItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaxonomyItem
        fields = ('id', 'taxonomy_group', 'parent', 'name')


class RecursiveTaxonomyItemSerializer(serializers.ModelSerializer):
    children = RecursiveField(source='taxonomyitem_set', many=True, read_only=True)

    class Meta:
        model = TaxonomyItem
        fields = ('id', 'taxonomy_group', 'parent', 'name', 'children')


class TaxonomyGroupSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField('get_item_count')
    taxonomy_items = MinimalTaxonomyItemSerializer(source='taxonomyitem_set', many=True, read_only=True)

    class Meta:
        model = TaxonomyGroup
        fields = ('id', 'name', 'display_name', 'item_count', 'taxonomy_items')

    def get_item_count(self, obj):
        return obj.taxonomyitem_set.count()

class MinimalTaxonomyGroupSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField('get_item_count')
    # taxonomy_items = MinimalTaxonomyItemSerializer(source='taxonomyitem_set', many=True, read_only=True)

    class Meta:
        model = TaxonomyGroup
        fields = ('id', 'name', 'display_name', 'item_count')

    def get_item_count(self, obj):
        return obj.taxonomyitem_set.count()


class TaxonomyMapSerializer(serializers.ModelSerializer):
    taxonomy_group = serializers.Field(source='taxonomy_item.taxonomy_group.pk')
    taxonomy_group_name = serializers.Field(source='taxonomy_item.taxonomy_group.name')
    taxonomy_item_name = serializers.Field(source='taxonomy_item.name')
    content_type_model = serializers.Field(source='content_type.model')

    class Meta:
        model = TaxonomyMap
        exclude = ()
