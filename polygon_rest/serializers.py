from rest_framework import serializers
from rest_framework.response import Response

from .models import Dot, FRectangle, Rectangle
from polygon_rest.extansions import insert_in
from polygon_rest.models import NUMBER_OF_GRAND


class DotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dot
        fields = ('pk', 'x', 'y', 'desc')

    def create(self, validated_data):

        dot = Dot(x=validated_data['x'],
                  y=validated_data['y'],
                  desc=validated_data['desc'])

        grand_node = Rectangle.objects.select_related('children_a').get(pk=NUMBER_OF_GRAND)

        if insert_in(grand_node, dot):
            return True
        else:
            return False

    def update(self, instance, validated_data):

        instance.frectangle = None
        instance.save()

        instance.x = validated_data.get('x', instance.x)
        instance.y = validated_data.get('y', instance.y)
        instance.desc = validated_data.get('desc', instance.desc)
        grand_node = Rectangle.objects.get(pk=NUMBER_OF_GRAND)

        if insert_in(grand_node, instance):
            return Response(instance)
        else:
            return Response(instance)

