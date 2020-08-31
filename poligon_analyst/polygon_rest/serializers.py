from rest_framework import serializers
from .models import Dot, FRectangle, Rectangle
from polygon_rest.extansions import insert_in


class DotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dot
        fields = ('x', 'y', 'desc')

    def create(self, validated_data):
        dot = Dot(x=validated_data['x'],
                  y=validated_data['y'],
                  desc=validated_data['desc'])

        grand_node = Rectangle.objects.get(pk=20)

        if insert_in(grand_node, dot):
            return dot
        else:
            return None
        pass
