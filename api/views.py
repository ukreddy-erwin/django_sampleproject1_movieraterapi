from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from .models import Rating,Movie
from .serializers import MovieSerializer,RatingSerializer
from django.contrib.auth.models import User

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    ## http://url:port/api/movies
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    autentication_classes = (TokenAuthentication,) ## will extract user from token

    ## http://url:port/api/movies/1/rate_movie/ POST
    ## detail True means one specific movie, False means all movies
    @action(detail=True, methods=['POST'])
    def rate_movie(self,request,pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user ##AnonymousUser as no token used ## will be fixed once we set authentication class for the view
            #user = User.objects.get(id=1)
            #print(pk,stars,user.username)

            print('movie title', movie.title)

            try:
                rating = Rating.objects.get(user=user.id,movie=movie.id)
                rating.stars = stars 
                rating.save()
                serializer = RatingSerializer(rating,many=False)
                response = {'message': 'Rating updated','result':serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user,movie=movie,stars=stars)
                serializer = RatingSerializer(rating,many=False)
                response = {'message': 'Rating created','result':serializer.data}
                return Response(response, status=status.HTTP_200_OK)

            
        else:
            response = {'message': 'You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
    ## http://url:port/api/ratings
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    autentication_classes = (TokenAuthentication,)