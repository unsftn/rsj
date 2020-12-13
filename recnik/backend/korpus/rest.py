from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from concurrency.exceptions import RecordModifiedError
from .models import *
from .serializers import *


class VrstaImeniceList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = VrstaImenice.objects.all()
    serializer_class = VrstaImeniceSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['naziv']


class VrstaImeniceDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = VrstaImenice.objects.all()
    serializer_class = VrstaImeniceSerializer


class ImenicaList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Imenica.objects.all()
    serializer_class = ImenicaSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['vrsta_id', 'nomjed', 'vreme']


class ImenicaDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Imenica.objects.all()
    serializer_class = ImenicaSerializer


class GlagolList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Glagol.objects.all()
    serializer_class = GlagolSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['vid', 'rod', 'infinitiv']


class GlagolDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Glagol.objects.all()
    serializer_class = GlagolSerializer


class PridevList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Pridev.objects.all()
    serializer_class = PridevSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['tekst']


class PridevDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Pridev.objects.all()
    serializer_class = PridevSerializer


JSON = 'application/json'


@api_view(['POST', 'PUT'])
def api_save_imenica(request):
    if request.method == 'POST':
        serializer = CreateImenicaSerializer(data=request.data)
    elif request.method == 'PUT':
        try:
            obj_id = request.data['id']
            imenica = Imenica.objects.get(id=obj_id)
            serializer = CreateImenicaSerializer(imenica, data=request.data)
        except (KeyError, Imenica.DoesNotExist) as ex:
            return Response({'error': 'invalid or missing object id'}, status=status.HTTP_404_NOT_FOUND,
                            content_type=JSON)
    else:
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED, content_type=JSON)

    if serializer.is_valid():
        try:
            imenica = serializer.save(user_id=request.user.id)
        except RecordModifiedError as ex:
            return Response({'error': 'optimistic lock exception'}, status=status.HTTP_409_CONFLICT, content_type=JSON)
        if request.method == 'POST':
            return Response(ImenicaSerializer(imenica).data, status=status.HTTP_201_CREATED, content_type=JSON)
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST', 'PUT'])
def api_save_glagol(request):
    if request.method == 'POST':
        serializer = CreateGlagolSerializer(data=request.data)
    elif request.method == 'PUT':
        try:
            obj_id = request.data['id']
            glagol = Glagol.objects.get(id=obj_id)
            serializer = CreateGlagolSerializer(glagol, data=request.data)
        except (KeyError, Glagol.DoesNotExist) as ex:
            return Response({'error': 'invalid or missing object id'}, status=status.HTTP_404_NOT_FOUND,
                            content_type=JSON)
    else:
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED, content_type=JSON)

    if serializer.is_valid():
        try:
            glagol = serializer.save(user_id=request.user.id)
        except RecordModifiedError as ex:
            return Response({'error': 'optimistic lock exception'}, status=status.HTTP_409_CONFLICT, content_type=JSON)
        if request.method == 'POST':
            return Response(GlagolSerializer(glagol).data, status=status.HTTP_201_CREATED, content_type=JSON)
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)


@api_view(['POST', 'PUT'])
def api_save_pridev(request):
    if request.method == 'POST':
        serializer = CreatePridevSerializer(data=request.data)
    elif request.method == 'PUT':
        try:
            obj_id = request.data['id']
            pridev = Pridev.objects.get(id=obj_id)
            serializer = CreatePridevSerializer(pridev, data=request.data)
        except (KeyError, Pridev.DoesNotExist) as ex:
            return Response({'error': 'invalid or missing object id'}, status=status.HTTP_404_NOT_FOUND,
                            content_type=JSON)
    else:
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED, content_type='application/json')

    if serializer.is_valid():
        try:
            pridev = serializer.save(user_id=request.user.id)
        except RecordModifiedError as ex:
            return Response({'error': 'optimistic lock exception'}, status=status.HTTP_409_CONFLICT, content_type=JSON)
        if request.method == 'POST':
            return Response(PridevSerializer(pridev).data, status=status.HTTP_201_CREATED, content_type=JSON)
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT, content_type=JSON)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type=JSON)
