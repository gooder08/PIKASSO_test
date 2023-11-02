from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from files_upload.models import File
from files_upload.serializers import FileSerializer
from .tasks import process_file

@api_view(['POST'])
def upload_file(request):
    serializer = FileSerializer(data=request.data)
    if serializer.is_valid():
        file_instance = serializer.save()
        process_file.delay(file_instance.id)
        # Здесь вы можете выполнить дополнительные действия с загруженным файлом
        # и запустить асинхронную задачу с использованием Celery
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_files(request):
    files = File.objects.all()
    serializer = FileSerializer(files, many=True)
    return Response(serializer.data)

def upload_file_page(request):
    return render(request, 'upload.html')
