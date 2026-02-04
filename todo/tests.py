from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from todo.models import Todo, StatusTodo, PrioritasTodo
from todo.services import TodoService
from todo.error_codes import ErrorTodo
from common.exceptions import DomainException


class TodoServiceTest(TestCase):

    def setUp(self):
        self.service = TodoService()
        self.todo = Todo.objects.create(
            judul="Belajar Django",
            deskripsi="Belajar service layer",
            prioritas=PrioritasTodo.SEDANG
        )

    def test_ubah_status_dari_todo_ke_selesai(self):
        hasil = self.service.ubah_status(
            todo=self.todo,
            status_baru=StatusTodo.SELESAI,
        )

        self.assertEqual(hasil.status, StatusTodo.SELESAI)

    def test_gagal_ubah_status_todo_langsung_ke_diarsipkan(self):
        with self.assertRaises(DomainException) as context:
            self.service.ubah_status(
                todo=self.todo,
                status_baru=StatusTodo.DIARSIPKAN,
            )

        self.assertEqual(
            context.exception.kode,
            ErrorTodo.STATUS_TIDAK_VALID,
        )

    def test_gagal_ubah_status_jika_todo_sudah_diarsipkan(self):
        self.todo.status = StatusTodo.DIARSIPKAN
        self.todo.save()

        with self.assertRaises(DomainException) as context:
            self.service.ubah_status(
                todo=self.todo,
                status_baru=StatusTodo.SELESAI,
            )

            self.assertEqual(
                context.exception.kode,
                ErrorTodo.TODO_SUDAH_DIARSIPKAN,
            )

    def test_ambil_semua_todo_dengan_filter_status(self):
        Todo.objects.create(
            judul="Todo selesai",
            prioritas=PrioritasTodo.SEDANG,
            status=StatusTodo.SELESAI,
        )

        hasil = self.service.ambil_semua(status=StatusTodo.SELESAI)

        self.assertEqual(hasil.count(), 1)
        self.assertEqual(hasil.first().status, StatusTodo.SELESAI)


class TodoAPITest(APITestCase):

    def setUp(self):
        self.url_buat = "/api/todo/"

        self.todo = Todo.objects.create(
            judul="Test Todo",
            prioritas=PrioritasTodo.SEDANG,
        )

    def test_api_buat_todo(self):
        response = self.client.post(
            self.url_buat,
            data={
                "judul": "Belajar API",
                "prioritas": PrioritasTodo.SEDANG,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Todo.objects.count(), 2)

    def test_ubah_status_todo(self):
        response = self.client.post(
            f"/api/todo/{self.todo.id}/status/",
            data={
                "status": StatusTodo.SELESAI
            },
            format="json"
        )

        self.todo.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.todo.status, StatusTodo.SELESAI)

    def test_api_gagal_ubah_status_todo_langsung_diarsipkan(self):
        response = self.client.post(
            f"/api/todo/{self.todo.id}/status/",
            data={
                "status": StatusTodo.DIARSIPKAN
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"]["kode"], ErrorTodo.STATUS_TIDAK_VALID)

    def test_api_list_todo(self):
        response = self.client.get("/api/todo/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_api_filter_todo_by_status(self):
        response = self.client.get("/api/todo/?status=TODO")

        self.assertEqual(response.status_code, 200)

        for item in response.data:
            self.assertEqual(item["status"], StatusTodo.TODO)
