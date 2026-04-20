from rest_framework import filters

class RoleBasedFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if hasattr(queryset, 'visible_for'):
            return queryset.visible_for(request.user)
        return queryset