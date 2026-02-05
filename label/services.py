from label.models import Label
from common.exceptions import DomainException



class LabelService:

    def buat_label(self, *, nama: str):
        if not nama:
            raise DomainException("LABEL_KOSONG", "Nama label wajib diisi")

        return Label.objects.create(nama=nama)
