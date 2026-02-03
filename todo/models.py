import uuid
from django.db import models



class StatusTodo(models.TextChoices):
    TODO = "TODO", "Todo"
    SELESAI = "SELESAI", "Selesai"
    DIARSIPKAN = "DIARSIPKAN", "Diarsipkan"


class PrioritasTodo(models.TextChoices):
    RENDAH = "RENDAH", "Rendah"
    SEDANG = "SEDANG", "Sedang"
    TINGGI = "TINGGI", "Tinggi"


class Todo(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    judul = models.CharField(
        max_length=200
    )
    deskripsi=models.TextField(
        blank=True
    )
    status=models.CharField(
        max_length=20,
        choices=StatusTodo.choices,
        default=StatusTodo.TODO,
    )
    prioritas=models.CharField(
        max_length=20,
        choices=PrioritasTodo.choices,
        default=PrioritasTodo.SEDANG
    )
    tanggal_jatuh_tempo=models.DateField(
        null=True,
        blank=True
    )
    dibuat_pada=models.DateTimeField(
        auto_now_add=True
    )
    diubah_pada=models.DateTimeField(
        auto_now=True
    )

    labels = models.ManyToManyField(
        "label.Label",
        related_name="todos",
        blank=True
    )


def __str__(self):
    return self.judul
