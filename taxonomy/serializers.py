from rest_framework import serializers, pagination
from .models import (TaxonomyGroup, TaxonomyItem)


class TaxonomyItemSerializer(serializers.ModelSerializer):
    taxonomy_group_name = serializers.Field(source='taxonomy_group.name')
    parent_name = serializers.Field(source='parent.name')
    map_count = serializers.SerializerMethodField('get_map_count')

    class Meta:
        model = TaxonomyItem
        fields = ('id', 'taxonomy_group', 'parent', 'name', 'map_count',
                'taxonomy_group_name', 'parent_name')

    def get_map_count(self, obj):
        return obj.taxonomymap_set.count()


class MinimalTaxonomyItemSerializer(serializers.ModelSerializer):
    children = MinimalTaxonomyItemSerializer(source='taxonomyitem_set', many=True, read_only=True)

    class Meta:
        model = TaxonomyItem
        fields = ('id', 'taxonomy_group', 'parent', 'name', 'children')

    def get_map_count(self, obj):
        return obj.taxonomymap_set.count()



class TaxonomyGroupSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField('get_item_count')
    taxonomy_items = MinimalTaxonomyItemSerializer(source='taxonomyitem_set', many=True, read_only=True)

    class Meta:
        model = TaxonomyGroup
        fields = ('id', 'name', 'item_count', 'taxonomy_items')

    def get_item_count(self, obj):
        return obj.taxonomyitem_set.count()

