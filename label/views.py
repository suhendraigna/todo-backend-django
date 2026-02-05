from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from label.serializers import LabelBuatSerializer
from label.services import LabelService
from common.exceptions import DomainException



class LabelBuatAPIView(APIView):

    def post(self, request):
        serializer = LabelBuatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = LabelService()

        try:
            label = service.buat_label(
                nama=serializer.validated_data["nama"]
            )
        except DomainException as e:
            return Reponse(
                {
                    "error": {
                        "kode": e.kode,
                        "pesan": e.pesan
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        return Response(
            {
                "id": str(label.id),
                "nama": label.nama
            },
            status=status.HTTP_201_CREATED,
        )
