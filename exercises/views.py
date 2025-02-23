from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models  # اضافه شد
from .models import Muscle, Exercise
from .serializers import MuscleSerializer, ExerciseSerializer

class MuscleViewSet(viewsets.ModelViewSet):
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer

    @action(detail=True, methods=['get'])  # اصلاح شد
    def exercises(self, request, pk=None):
        muscle = self.get_object()
        exercises = Exercise.objects.filter(muscle=muscle)
        serializer = ExerciseSerializer(exercises, many=True, context={'request': request})
        return Response(serializer.data)

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        queryset = Exercise.objects.all()
        search = self.request.query_params.get('search', None)  # اصلاح شد

        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(tags__icontains=search)
            )
        return queryset