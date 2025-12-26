from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def list(self, request, *args, **kwargs):
        students = self.get_queryset()
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

