from django.urls import path
from todo.views import TodoBuatAPIView, TodoUbahStatusAPIView, TodoHapusAPIView


urlpatterns = [
    path("", TodoBuatAPIView.as_view(), name="todo-buat"),
    path("<uuid:todo_id>/status/", TodoUbahStatusAPIView.as_view(), name="todo-ubah-status"),
    path("<uuid:todo_id>/", TodoHapusAPIView.as_view(), name="todo-hapus"),
]
