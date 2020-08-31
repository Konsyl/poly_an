from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from polygon_rest.models import Dot, Rectangle
from polygon_rest.serializers import DotSerializer
from polygon_rest import extansions


# Create your views here.


class is_ok(View):

    def get(self, request):
        return HttpResponse("OK")


class DotController(APIView):

    def get(self, request):
        dots = Dot.objects.all()
        serializer = DotSerializer(dots, many=True)
        return Response(serializer.data)

    def post(self, request):
        dot = DotSerializer(data=request.data)
        if dot.is_valid():
            dot.save()
            return Response(status=201)


class DotController(APIView):

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
