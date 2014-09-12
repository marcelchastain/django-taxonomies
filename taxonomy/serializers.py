from rest_framework import serializers, pagination
from .models import (TaxonomyGroup, TaxonomyItem)


class RecursiveField(serializers.Serializer):
    def to_native(self, value):
        return self.parent.to_native(value)

class TaxonomyItemSerializer(serializers.ModelSerializer):
    taxonomy_group_name = serializers.Field(source='taxonomy_group.name')
    taxonomy_group_display_name = serializers.Field(source='taxonomy_group.display_name')
    parent_name = serializers.Field(source='parent.name')
    parent_display_name = serializers.Field(source='parent.display_name')
    map_count = serializers.SerializerMethodField('get_map_count')

    class Meta:
        model = TaxonomyItem
        fields = ('id', 'taxonomy_group', 'parent', 'name', 'map_count',
                'taxonomy_group_name', 'taxonomy_group_display_name',
                'parent_name', 'parent_display_name')

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
        fields = ('id', 'taxonomy_group', 'parent', 'display_name', 'name', 'children')


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

