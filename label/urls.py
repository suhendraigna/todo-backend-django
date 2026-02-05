from django.urls import path
from label.views import LabelBuatAPIView

urlpatterns = [
    path("", LabelBuatAPIView.as_view(), name="label-buat"),
]
