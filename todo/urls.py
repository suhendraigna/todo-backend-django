from django.urls import path, include
from todo.views import TodoBuatAPIView, TodoUbahStatusAPIView, TodoDetailAPIView


urlpatterns = [
    path("", TodoBuatAPIView.as_view(), name="todo-buat"),
    path("<uuid:todo_id>/status/", TodoUbahStatusAPIView.as_view(), name="todo-ubah-status"),
    path("<uuid:todo_id>/", TodoDetailAPIView.as_view(), name="todo-detail"),
]
