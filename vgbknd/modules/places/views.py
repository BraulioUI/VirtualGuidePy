from .services import PlaceService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import CategoryTpSerializer, NearbyPlaceSerializer, TouristicPlaceCategorySerializer, TouristicPlaceSerializer, PictureTouristicPlaceSerializer
from .models import *
from modules.reviews.models import Review
from modules.reviews.serializers import ReviewTpSerializer
import jwt

# Create your views here.

class CreateTouristicPlace(APIView):
    def post(self, request):
        serializer = TouristicPlaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AddTpCategory(APIView):
    def post(self, request):
        serializer = TouristicPlaceCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class TouristicPlaceListView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        touristicPlaces = TouristicPlace.objects.all()
        serializer = TouristicPlaceSerializer(touristicPlaces, many=True)
        return Response(serializer.data)

class TouristicPlaceById(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        touristicPlace = TouristicPlace.objects.filter(touristicplace_id=pk).first()
        
        tppictures = PictureTouristicPlace.objects.filter(touristic_place=pk)
        picturesSerializer = PictureTouristicPlaceSerializer(tppictures, many=True)

        categorystp =  TouristicPlaceCategory.objects.filter(touristic_place=pk)
        categorystpSerializer = CategoryTpSerializer(categorystp, many=True)

        
        reviews = Review.objects.filter(touristic_place=pk)



       
        reviewsSerializer = ReviewTpSerializer(reviews, many=True)
        
        response = Response()

        simExp = TouristicPlace.objects.filter(type_place=touristicPlace.type_place).exclude(touristicplace_id=pk)

        simExpSer = NearbyPlaceSerializer(simExp, many=True)

        response.data = {
            'pictures': picturesSerializer.data,
            'name': touristicPlace.name,
            'long_info': touristicPlace.long_info,
            'categories': categorystpSerializer.data,
            'latitude': touristicPlace.latitude,
            'longitude': touristicPlace.longitude,
            'avg_ranking': touristicPlace.avg_ranking,
            'number_comments': touristicPlace.number_comments,
            'reviews': reviewsSerializer.data,
            'similarExperiences': simExpSer.data,
            'isFavourite': touristicPlace.isFavourite
        }
        return response


class CreatePictureTouristicPlace(APIView):
   def post(self, request):
        serializer = PictureTouristicPlaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PictureTouristicPlaceListView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        pictureTouristicPlaces = PictureTouristicPlace.objects.filter(touristic_place=pk)
        serializer = PictureTouristicPlaceSerializer(pictureTouristicPlaces, many=True)
        return Response(serializer.data)

class NearbyPlaces(APIView):
    def post(self, request):
        touristicPlaces = TouristicPlace.objects.filter(type_place=1)
        
        lat = request.data['latitude']
        lon = request.data['longitude']

        placeService = PlaceService(lat, lon) 
        
        tplist = placeService.tpnearbylist(touristicPlaces)
        
        serializer = NearbyPlaceSerializer(tplist, many=True)
        
        return Response(serializer.data)