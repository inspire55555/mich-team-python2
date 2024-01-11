from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from cart.models import Cart
from main_app.models import Product
from .serializers import OrderSerializer

CustomUser = get_user_model()


class OrderListCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def get_session_id(self, request):
        # Function to get session ID for unauthenticated users
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        return session_key

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        delivery_method = request.data.get("delivery_method")
        country = request.data.get("country")
        street = request.data.get("street")
        city = request.data.get("city")
        state = request.data.get("state")
        zip_code = request.data.get("zip_code")
        product_data = request.data.get("product")

        session_id = request.session.session_key

        user = request.user if request.user.is_authenticated else None
        user_id = user.id if user and user.is_authenticated else None
        email = user.email if user and user.is_authenticated else request.data.get("email")
        first_name = user.first_name if user and user.is_authenticated else request.data.get("first_name")
        last_name = user.last_name if user and user.is_authenticated else request.data.get("last_name")

        response_data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "delivery_method": delivery_method,
            "country": country,
            "street": street,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            'user': user_id,
            'product': product_data
        }

        order_serializer = OrderSerializer(data=response_data)

        if order_serializer.is_valid():
            order = order_serializer.save(user=user)

            # Handle associating carts with the order
            if user and user.is_authenticated:
                user_carts = Cart.objects.filter(user=user, is_active=True)
                user_carts.update(order=order)

                for cart in user_carts:
                    cart.is_active = False
                    cart.save()
            else:
                session_carts = Cart.objects.filter(session_id=session_id, is_active=True)
                session_carts.update(order=order)

                for cart in session_carts:
                    cart.is_active = False
                    cart.save()

            # for cart in order.carts.all():
            #     product = cart.product
            #     quantity = cart.quantity
            #     product.quantity -= quantity
            #     product.save()

            return Response(order_serializer.data, status=status.HTTP_201_CREATED)

        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
