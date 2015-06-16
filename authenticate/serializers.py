from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers

from authenticate.models import Account


class AccountSerializer(serializers.ModelSerializer):
    # Don't update password unless a new one is provided.
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    # Define metadata for serializer to operate
    class Meta:
        # Model to serialize
        model = Account

        # Attributes of the Account model should be serialized
        # Some fields should not be available on client for security
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'tagline', 'password',
                  'confirm_password',)

        # Self-updating models are read-only
        read_only_fields = ('created_at', 'updated_at',)

        # Turn JSON into Python object (Deserialization)
        def create(self, validate_data):
            return Account.objects.create(**validate_data)

        def update(self, instance, validate_data):
            # Let user update username and tagline attributes
            # If keys are present in the array dictionary will use new value
            # Otherwise, current value of the instance will be used
            instance.username = validate_data.get('username', instance.username)
            instance.tagline = validate_data.get('tagline', instance.tagline)

            instance.save()

            # Before updating user's password confirm both values are provided
            password = validate_data.get('password', None)
            confirm_password = validate_data.get('confirm_password', None)

            # Both values are equivelant
            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            # Session auth hash update.
            # If you dont do this user will not be auth on next request and
            # will be asked to login again
            updated_session_auth_hash(self.context.get('request'), instance)

            return instance




