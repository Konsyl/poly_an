from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from polygon_rest.models import Dot, Rectangle
from polygon_rest.serializers import DotSerializer
from polygon_rest import extansions


# Create your views here.


class is_ok(View):

    def get(self, request):
        return HttpResponse("OK")


class DotsController(APIView):
    def get(self, request):
        dots = Dot.objects.all()
        serializer = DotSerializer(dots, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DotSerializer(data=request.data, many=False)
        if serializer.is_valid():
            if serializer.create(validated_data=serializer.validated_data):
                return Response(serializer.data)
            else:
                return Response('BAD REQUEST')
        else:
            return Response('BAD REQUEST')


class DotController(APIView):
    def get(self, request, pk, format=None):
        dot = get_object_or_404(Dot.objects.all(), pk=pk)
        serializer = DotSerializer(dot, many=False)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        dot = Dot.objects.get(pk=pk)
        if dot.frectangle is not None:
            dot.delete()
            return Response('complete')
        else:
            return Response("not allowed delete rectangel's dots")

    def put(self, request, pk, format=None):
        dot = get_object_or_404(Dot.objects.all(), pk=pk)
        if dot.frectangle is not None:
            serializer = DotSerializer(data=request.data)
            if serializer.is_valid():
                serializer.update(validated_data=serializer.validated_data, instance=dot)

                return Response(DotSerializer(dot).data)
        else:
            return Response("not allowed update rectangle's dots")

    def post(self, request):
        dot = Dot()
        dot.x = request.data['x']
        dot.y = request.data['y']
        R = request.data['R']
        K = request.data['K']
        grand_node = Rectangle.objects.get(pk=20)
        extansions.temp_res = []
        extansions.search(node=grand_node, R=R, K=K, dot=dot)
        res = []
        for i in extansions.temp_res:
            res.append(i[1])
        serializer = DotSerializer(res, many=True)
        print(extansions.temp_res)
        return Response(serializer.data)
