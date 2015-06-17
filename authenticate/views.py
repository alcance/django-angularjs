from rest_framework import permissions, viewsets

from authenticate.models import Account
from authenticate.permissions import IsAccountOwner
from authenticate.serializers import AccountSerializer

# ModelViewSet offers a interface for: listing, create
# create, update and destroy objects of a given model
class AccountViewSet(viewsets.ModelViewSet):
    # Define the query set and the serializer that the
    # viewset will operate on.

    # Lookup accounts using username instead of the obj id
    lookup_field = 'username'
    # Get all objects from Model
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.AllowAny(), IsAccountOwner(),)


    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)

            return Response(serializer.validate_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        })




