from rest_framework import serializers



class LabelBuatSerializer(serializers.Serializer):
    nama = serializers.CharField(max_length=100)
