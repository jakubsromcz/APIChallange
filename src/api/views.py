from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Country
from .serializers import CountrySerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CountryListCreateAPIView(APIView):

    # method GET for all countries with query paramaters
    def get(self, request, format=None):
        country_code = request.query_params.get('country-code', None)
        limit = request.query_params.get('limit', 50) # default limit is 50
        offset = request.query_params.get('offset', 0)
        
        # filter countryCode if exist in query or render all countries
        if country_code:
            countries = Country.objects.filter(countryCode=country_code)
        else:
            countries = Country.objects.all()
        
        # Pagination settings
        paginator = Paginator(countries, limit)
        try:
            countries_page = paginator.page(int(offset) // int(limit) + 1)
        except PageNotAnInteger:
            countries_page = paginator.page(1)
        except EmptyPage:
            countries_page = paginator.page(paginator.num_pages)

        serializer = CountrySerializer(countries_page, many=True)

        response_data = {
            "links": {      # links for pagination
                "next": countries_page.has_next() and f"/countries/?limit={limit}&offset={int(offset) + int(limit)}" or "",
                "previous": countries_page.has_previous() and f"/countries/?limit={limit}&offset={int(offset) - int(limit)}" or ""
            },
            "pagination": {     # pagination info
                "count": paginator.count,
                "offset": int(offset),
                "limit": int(limit)
            },
            "results": serializer.data
        }

        return Response(response_data)

    # Create country
    def post(self, request, format=None):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            country = serializer.save()
            country.groupId = country.id # id and groupId is same value
            country.save()
            response_data = CountrySerializer(country).data
            response_data["description"] = "Succesfully created a country"
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountryRetrieveUpdateAPIView(APIView):

    # GET country from id in url
    def get(self, request, pk, format=None):
        try:
            country = Country.objects.get(pk=pk)
        except Country.DoesNotExist:
            return Response({
                "error": "Country not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CountrySerializer(country)
        response_data = serializer.data
        response_data["description"] = "Succesful retrieval information of certain country"
        return Response(response_data)

    # update country if get ID in url
    def put(self, request, pk, format=None):
        try:
            country = Country.objects.get(pk=pk) 
        except Country.DoesNotExist:
            return Response({
                "error": "Country not found"
            }, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name')
        country_code = request.data.get('countryCode')
        
        # Check if name or countryCode already exist in database (except current saving country)
        if Country.objects.filter(name=name).exclude(pk=pk).exists() or Country.objects.filter(countryCode=country_code).exclude(pk=pk).exists():
            return Response({
                "error": "Country with this name or countryCode already exists."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            response_data["description"] = "Succesfully updated the country"
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
