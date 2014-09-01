from rest_framework import serializers, pagination
from .models import (TaxonomyGroup, TaxonomyItem)


class TaxonomyGroupSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField('get_item_count')

    class Meta:
        model = TaxonomyGroup
        fields = ('id', 'name')

    def get_item_count(self, obj):
        return obj.taxonomyitem_set.count()

class TaxonomyItemSerializer(serializers.ModelSerializer):
    map_count = serializers.SerializerMethodField('get_map_count')

    class Meta:
        model = TaxonomyItem
        fields = ('id', 'taxonomy_group', 'parent', 'name')

    def get_map_count(self, obj):
        return obj.taxonomymap_set.count()
