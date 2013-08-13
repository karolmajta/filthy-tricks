'''
Created on 23-07-2013

@author: kamil
'''  
from rest_framework.relations import PrimaryKeyRelatedField

from filthy.views import TrackDependencyMixin


class TrackDependencyPrimaryKeyField(PrimaryKeyRelatedField):
    
    errors = {
        "no_context": u"Serializers using TrackDependencyPrimaryKeyField must get context.",
        "no_view": u"Serializers using TrackDependencyPrimaryKeyField must"
                   " receive current view passed as `view` in context.",
        "wrong_view": u"Serializers using TrackDependencyPrimaryKeyField must"
                   " be used by views that mix in TrackDependenciesMixin"
    }
    
    def initialize(self, parent, field_name):
        """
        Called to set up a field prior to field_to_native or field_from_native.

        parent - The parent serializer.
        model_field - The model field this field corresponds to, if one exists.
        """
        super(TrackDependencyPrimaryKeyField, self).initialize(parent, field_name)
        assert "view" in self.root.context, self.__class__.errors["no_view"]
        assert isinstance(self.root.context["view"], TrackDependencyMixin)
    
    def field_to_native(self, obj, field_name):
        tracked = getattr(obj, self.source or field_name)
        res = super(TrackDependencyPrimaryKeyField, self).field_to_native(
            obj,
            field_name
        )
        key = tracked.__class__
        self.root.context["view"].track(key, res)
        return res