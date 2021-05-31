from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import File
from .serializers import UploadSerializer,FileSerializer
from rest_framework.response import Response
from .utils import MultipartJsonParser
from .views import check_uploaded_file_hash


class FileManage(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultipartJsonParser]

    def post(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UploadSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            title = request.data['title']
            description = request.data['description']
            upload = request.data['upload']
            real_file_id = check_uploaded_file_hash(upload)
            File.objects.create(user=user, title=title, description=description,
                                user_file_title=upload.name, upload=real_file_id)
        else:
            data = serializer.errors
        return Response(data)

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        files = File.objects.filter(user=user)
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

