from rest_framework import serializers, pagination
from .models import (TaxonomyGroup, TaxonomyItem)


class TaxonomyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxonomyGroup
        fields = ('id', 'name')

class TaxonomyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxonomyItem
        fields = ('id', 'taxonomy_group', 'parent', 'name')
