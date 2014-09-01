from rest_framework import serializers, pagination
from .models import (TaxonomyGroup, TaxonomyItem)


class TaxonomyGroupSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField('get_item_count')

    class Meta:
        model = TaxonomyGroup
        fields = ('id', 'name', 'item_count')

    def get_item_count(self, obj):
        return obj.taxonomyitem_set.count()

class TaxonomyItemSerializer(serializers.ModelSerializer):
    taxonomy_group_name = serializers.Field(source='taxonomy_group__name')
    parent_name = serializers.Field(source='parent__name')
    map_count = serializers.SerializerMethodField('get_map_count')

    class Meta:
        model = TaxonomyItem
        fields = ('id', 'taxonomy_group', 'parent', 'name', 'map_count')

    def get_map_count(self, obj):
        return obj.taxonomymap_set.count()
