from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from todo.models import Todo
from todo.services import TodoService
from todo.serializers import(
    TodoBuatSerializer,
    TodoUbahStatusSerializer,
    TodoResponseSerializer,
    TodoUbahSerializer,
    TodoTambahLabelSerializer,
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
        return Response(response_serializer.data, status=status.HTTP_201_CREATED
                )

    def get(self, request):
        status_filter = request.query_params.get("status")
        
        service = TodoService()
        todos = service.ambil_semua(status=status_filter)

        serializer = TodoResponseSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

        service = TodoService()

        try:
            todo = service.ubah_status(
                todo=todo,
                status_baru=serializer.validated_data["status"],
            )
        except DomainException as e:
            return Response(
                {"error": {"kode": e.kode, "pesan": e.pesan}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = TodoResponseSerializer(todo)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class TodoDetailAPIView(APIView):

    def put(self, request, todo_id):
        serializer = TodoUbahSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            todo = Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            return Response(
                {"error":{"pesan": "Todo tidak ditemukan."}},
                status=status.HTTP_404_NOT_FOUND,
            )

        service = TodoService()
        try:
            todo = service.ubah_todo(
                todo=todo,
                judul=serializer.validated_data["judul"],
                deskripsi=serializer.validated_data.get("deskripsi", ""),
                prioritas=serializer.validated_data["prioritas"],
            )
        except DomainException as e:
            return Response(
                {"error": {"kode": e.kode, "pesan": e.pesan}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = TodoResponseSerializer(todo)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, todo_id):
        try:
            todo = Todo.objects.get(id=todo_id)
        except Todo.DoestNotExist:
            return Response(
                {"error": {"pesan": "Todo tidak ditemukan."}},
                status=status.HTTP_404_NOT_FOUND,
                )

        service = TodoService()
        hasil = service.hapus_todo(todo=todo)

        return Response(hasil, status=status.HTTP_200_OK)

    def post(self, request, todo_id):
        serializer = TodoTambahLabelSerializer(data=request.data)
        serializer.is_valid()

        try:
            todo = Todo.objects.get(id=todo_id)
        except Todo.DoesNotExist:
            return Response(
                {"error": {"pesan": "Todo tidak ditemukan."}},
                status=status.HTTP_404_NOT_FOUND,
            )

        service = TodoService()
        try:
            todo = service.tambah_label(
                todo=todo,
                label_id = serializer.validated_data["label_id"],
            )
        except DomainException as e:
            return Response(
                {"error": {"kode": e.kode, "pesan": e.pesan}},
                status=status.HTTP_400_BAD_REQUEST
            )

        response_serializer = TodoResponseSerializer(todo)
        return Response(reponse_serializer.data, status=status.HTTP_200_OK)
