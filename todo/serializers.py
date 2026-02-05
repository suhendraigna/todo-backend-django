from rest_framework import serializers
from todo.models import Todo, StatusTodo, PrioritasTodo
from label.models import Label


class TodoBuatSerializer(serializers.Serializer):
    judul = serializers.CharField(max_length=200)
    deskripsi = serializers.CharField(required=False, allow_blank=True)
    prioritas = serializers.ChoiceField(choices=PrioritasTodo.choices)
    tanggal_jatuh_tempo = serializers.DateField(required=False, allow_null=True)
    label_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
    )


class TodoUbahStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=StatusTodo.choices)


class TodoResponseSerializer(serializers.ModelSerializer):
    labels = serializers.StringRelatedField(many=True)

    class Meta:
        model = Todo
        fields = [
            "id",
            "judul",
            "deskripsi",
            "status",
            "prioritas",
            "tanggal_jatuh_tempo",
            "dibuat_pada",
            "diubah_pada",
            "labels",
        ]


class TodoUbahSerializer(serializers.Serializer):
    judul = serializers.CharField(max_length=200)
    deskripsi = serializers.CharField(required=False, allow_blank=True)
    prioritas = serializers.ChoiceField(choices=PrioritasTodo.choices)


class TodoTambahLabelSerializer(serializers.Serializer):
    label_id = serializers.UUIDField()
