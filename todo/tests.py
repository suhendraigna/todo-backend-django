from django.test import TestCase

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
