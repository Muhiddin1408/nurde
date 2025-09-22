from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.model.card import Card, CardInfo
from payment.serializers import CardInfoSerializer
from payment.utils.add_card import add_card


class AddCardView(CreateAPIView):
    serializer_class = CardInfoSerializer
    model = Card
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        merchant_id ='6830068ddfc9ac0473674de8'
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        self.perform_create(serializer)
        card_number = serializer.data['card_number']
        expiry_date = serializer.data['expire']
        card_id = serializer.data['id']
        response = add_card(card_number, expiry_date, card_id, merchant_id)
        card_data = response["result"]["card"]
        card = Card.objects.get(pk=card_id)
        # Create CardInfo instance
        card_info = CardInfo.objects.create(
            parent=card,
            token=card_data["token"],
            card_number=card_data["number"],
            card_expire=card_data["expire"],
            recurrent=card_data["recurrent"],
            verify=card_data["verify"],
            type=card_data["type"]
        )
        print(card_info)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
