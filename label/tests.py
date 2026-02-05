from django.test import TestCase

from label.services import LabelService



class LabelServiceTest(TestCase):

    def setUp(self):
        self.service = LabelService()

    def test_buat_label_berhasil(self):
        label = self.service.buat_label(nama="urgent")

        self.assertEqual(label.nama, "urgent")

    def test_gagal_buat_label_karena_nama_kosong(self):
        with self.assertRaises(Exception):
            self.service.buat_label(nama="")
