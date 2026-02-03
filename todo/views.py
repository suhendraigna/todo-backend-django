from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from todo.models import Todo
from todo.services import TodoService
from todo.serializers import(
    TodoBuatSerializer,
    TodoUbahStatusSerializer,
    TodoResponseSerializer,
)
from label.models import Label
from common.exceptions import DomainException



class TodoBuatAPIView(APIView):
    def post(self, request):
        serializer = TodoBuatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        labels = []
        if "label_ids" in data:
            labels = list(
                Label.objects.filter(id__in=data["label_ids"])
            )

        service = TodoService()
        
        todo = service.buat_todo(
            judul=data["judul"],
            deskripsi=data.get("deskripsi", ""),
            prioritas=data["prioritas"],
            tanggal_jatuh_tempo=data.get("tanggal_jatuh_tempo"),
            labels=labels,
        )
        
        response_serializer = TodoResponseSerializer(todo)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class TodoUbahStatusAPIView(APIView):
    def post(self, request, todo_id):
        serializer = TodoUbahStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            todo = Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            return Response(
                {"error": {"kode": e.kode, "pesan": e.pesan}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = TodoResponseSerializer(todo)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
