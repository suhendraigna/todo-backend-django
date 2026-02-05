from todo.models import Todo, StatusTodo
from todo.error_codes import ErrorTodo
from common.exceptions import DomainException
from label.models import Label



class TodoService:

    def buat_todo(
        self,
        *,
        judul,
        deskripsi="",
        prioritas,
        tanggal_jatuh_tempo=None,
        labels=None
    ):
        todo = Todo.objects.create(
            judul=judul,
            deskripsi=deskripsi,
            prioritas=prioritas,
            tanggal_jatuh_tempo=tanggal_jatuh_tempo,
        )

        if labels:
            todo.labels.set(labels)
            return todo

    def ubah_status(self, *, todo:Todo, status_baru: str):
        if todo.status == StatusTodo.DIARSIPKAN:
            raise DomainException(
                ErrorTodo.TODO_SUDAH_DIARSIPKAN,
                "Todo yang sudah diarsipkan tidak boleh diubah.",
            )

        if not self._transisi_status_valid(todo.status, status_baru):
            raise DomainException(
                ErrorTodo.STATUS_TIDAK_VALID,
                f"Transisi status dari {todo.status} ke {status_baru} tidak valid"
            )
        
        todo.status = status_baru
        todo.save(update_fields=["status", "diubah_pada"])
        return todo

    def _transisi_status_valid(self, status_lama, status_baru):
        transisi_valid = {
            StatusTodo.TODO: [StatusTodo.SELESAI],
            StatusTodo.SELESAI: [StatusTodo.DIARSIPKAN],        
        }
        return status_baru in transisi_valid.get(status_lama, [])

    
    def ambil_semua(self, *, status=None):
        queryset = Todo.objects.all().order_by("-dibuat_pada")

        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def hapus_todo(self, *, todo: Todo):
        if todo.status != StatusTodo.DIARSIPKAN:
            todo.status = StatusTodo.DIARSIPKAN
            todo.save(update_fields=["status", "diubah_pada"])
            return {"diarsipkan": True}

        todo.delete()
        return {"dihapus": True}

    def ubah_todo(
        self,
        *,
        todo: Todo,
        judul,
        deskripsi="",
        prioritas
    ):
        if todo.status == StatusTodo.DIARSIPKAN:
            raise DomainException(
                ErrorTodo.TODO_SUDAH_DIARSIPKAN,
                "Todo yang sudah diarsipkan tidak dapat diubah.",
            )

        todo.judul = judul
        todo.deskripsi = deskripsi
        todo.prioritas = prioritas

        todo.save(update_fields=["judul", "deskripsi", "prioritas", "diubah_pada"])
        return todo

    def tambah_label(self, *, todo: Todo, label_id):
        try:
            label = Label.objects.get(id=label_id)
        except Label.DoesNotExist:
            raise DomainException("LABEL_TIDAK_DITEMUKAN", "Label tidak ditemukan.")
        if todo.labels.filter(id=label_id).exists():
            raise DomainException("LABEL_SUDAH_ADA", "Label sudah terpasang di todo ini.")

        todo.labels.add(label)
        return todo
