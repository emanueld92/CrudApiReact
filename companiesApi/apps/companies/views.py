from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status, views
from rest_framework.response import Response
from .models import Companies
from .serializers import CompaniesSerializer
# Create your views here.
import json


class CompaniesSet(views.APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0, *args, **kwargs):

        if (id > 0):

            queryset = Companies.objects.filter(id=id).values()
            serializer = CompaniesSerializer(queryset, many=True)
            if (len(queryset) > 0):
              
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'status': "Company not Found"}, status=status.HTTP_404_NOT_FOUND)
        else:

            queryset = Companies.objects.all()

            serializer = CompaniesSerializer(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

    # Create new company

    def post(self, request, *args, **kwargs):

        companies = Companies.objects.filter(name=request.data['name'])
        if companies:
            return Response({'status': "error, company already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            companies = Companies.objects.create(
                name=request.data['name'], website=request.data['website'], fundations=request.data['fundations'])
            companies.save()
        return Response({'status': "successfully registered"}, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        update = json.loads(request.body)
        companies = Companies.objects.filter(id=id).values()


        if companies:
            company = Companies.objects.get(id=id)
      
            company.name = update['name']
            company.website = update['website']
            company.fundations = update['fundations']
            company.save()
        else:
            return Response({'status': "error, company no exists"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'status':"update"},status=status.HTTP_200_OK)
    
    def delete(self,request,id, *args, **kwargs):
        company=Companies.objects.filter(id=id)
        if company:
            company.delete()
            return Response({'status':"company delete"},status=status.HTTP_200_OK)
        else:
            return Response({'status': "error, company no exists"}, status=status.HTTP_404_NOT_FOUND)
