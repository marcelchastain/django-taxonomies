from rest_framework import viewsets, response, status, permissions, parsers
from core.permissions import IsAdminUserOrReadOnly
from .serializers import TaxonomyItemSerializer, TaxonomyGroupSerializer
from .models import TaxonomyGroup, TaxonomyItem


class ShowroomMixin(object):
    def pre_save(self, obj):
        """Force showroom to the current user's on save"""
        showroom = self.request.user.get_showroom()
        showroom_id = self.request.user.get_showroom().pk
        obj.showroom = showroom
        obj.showroom_id = showroom_id

        return super(ShowroomMixin, self).pre_save(obj)

    def get_queryset(self):
        """force showroom to the current user's on query"""
        cls = self.serializer_class.Meta.model
        showroom_id = self.request.user.get_showroom().pk
        qs = cls.objects.filter(showroom_id=showroom_id)
        if getattr(self, 'queryset_filter', None):
            qs = qs.filter(**self.queryset_filter)
        return qs


class TaxonomyGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = TaxonomyGroupSerializer
    model = TaxonomyGroup
    filter_fields = ('name',)


class TaxonomyItemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = TaxonomyItemSerializer
    model = TaxonomyItem
