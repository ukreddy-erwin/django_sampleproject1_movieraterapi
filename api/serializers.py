from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Movie, Rating

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id','username','password')
        extra_kwargs = {'password':{'write_olny': True, 'required': True}}  ## password is sipped in get request of api
    ## overridden default method
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie 
        fields = ('id','title','description','no_of_ratings')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating 
        fields = ('id','stars','user','movie')