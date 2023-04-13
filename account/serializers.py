from rest_framework import serializers
from random import randint

from account.models import User

class RegisterSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(style={"input-type":"password"}, write_only=True)

    class Meta:

        model = User
        fields = ('email','name','password','password1')
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):

        p1 = self.validated_data['password']
        p2 = self.validated_data['password1']

        if p1!=p2:
            raise serializers.ValidationError("Password is not matching")
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError("Email already exists")
        
        user = User.objects.create_user(email = self.validated_data['email'],name = self.validated_data['name'])
        user.set_password(self.validated_data['password'])
        user.save()
        return user