from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from polygon_rest.models import Dot, Rectangle, NUMBER_OF_GRAND
from polygon_rest.serializers import DotSerializer
from polygon_rest import extansions


class IsOk(View):
    def get(self, request):
        return HttpResponse("WORKING")


class DotsController(APIView):
    def get(self, request):
        dots = Dot.objects.filter(frectangle_id__isnull=False)
        serializer = DotSerializer(dots, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DotSerializer(data=request.data, many=False)
        if serializer.is_valid():

            if serializer.create(validated_data=serializer.validated_data):

                return Response(serializer.data)
            else:
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=400)


class DotController(APIView):
    def get(self, request, pk, format=None):
        dot = get_object_or_404(Dot.objects.all(), pk=pk)
        serializer = DotSerializer(dot, many=False)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        dot = get_object_or_404(Dot.objects.all(), pk=pk)
        if dot.frectangle is not None:
            dot.delete()
            return HttpResponse(status=200)
        else:
            return HttpResponse('NOT ALLOWED DELETE BASE DOT', status=400)

    def put(self, request, pk, format=None):
        dot = get_object_or_404(Dot.objects.all(), pk=pk)
        if dot.frectangle is not None:
            serializer = DotSerializer(data=request.data)
            if serializer.is_valid():
                serializer.update(validated_data=serializer.validated_data, instance=dot)

                return Response(DotSerializer(dot).data)
        else:
            return HttpResponse(status=400)

    def post(self, request):
        dot = Dot()
        dot.x = float(request.data['x'])
        dot.y = float(request.data['y'])
        r = float(request.data['R'])
        k = int(request.data['K'])
        grand_node = Rectangle.objects.select_related('children_a').get(pk=NUMBER_OF_GRAND)
        extansions.temp_res = []
        extansions.search(node=grand_node, R=r, K=k, dot=dot)
        res = []
        for i in extansions.temp_res:
            res.append(i[1])
        serializer = DotSerializer(res, many=True)

        return Response(serializer.data)
