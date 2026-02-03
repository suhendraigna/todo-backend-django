import uuid
from django.db import models



class Label(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    nama = models.CharField(
        max_length=100
    )
    warna = models.CharField(
        max_length=20,
        blank=True
    )
    dibuat_pada = models.DateTimeField(
        auto_now_add=True
    )
    diubah_pada = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.nama
