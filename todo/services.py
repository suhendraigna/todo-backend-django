from todo.models import Todo
from todo.error_codes import ErrorTodo
from common.exceptionx import DomainException



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

        if not self._transisi_status_valid(todo.STATUS, status_baru):
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
        return status_baru in transisi_valid_get(status_lama, [])

