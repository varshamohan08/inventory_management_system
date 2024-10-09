from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Item
from global_functions import generate_exception
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .serializers import itemSerializer
from django.http import Http404
from redis import StrictRedis
from django.conf import settings
import json

redis_instance = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)

class ItemAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id=None):
        try:
            with transaction.atomic():
                # import pdb;pdb.set_trace()
                if item_id:
                    cache_key = f"item_{item_id}"
                    cached_item = redis_instance.get(cache_key)

                    if cached_item:
                        item_data = json.loads(cached_item)
                        return Response({'success': True, 'details': item_data}, status=status.HTTP_200_OK)
                    
                    try:
                        item_instance = get_object_or_404(Item, id=item_id)
                    except Http404:
                        return Response({'success': False, 'details': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
                    
                    serializer = itemSerializer(item_instance)
                    redis_instance.set(cache_key, json.dumps(serializer.data), ex=900)

                    return Response({'success': True, 'details': serializer.data}, status=status.HTTP_200_OK)
                
                else:
                    cached_item = redis_instance.get("item_list")

                    if cached_item:
                        item_data = json.loads(cached_item)
                        return Response({'success': True, 'details': item_data}, status=status.HTTP_200_OK)

                    items = Item.objects.filter(bln_active=True).order_by('-id')
                    serializer = itemSerializer(items, many=True)
                    redis_instance.set("item_list", json.dumps(serializer.data), ex=900)

                    return Response({'success': True, 'details': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            generate_exception(e)
            return Response({'success': False, 'details':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    def post(self, request):
        # import pdb;pdb.set_trace()
        try:
            with transaction.atomic():
                serializer = itemSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()

                    redis_instance.delete("item_list")

                    return Response({'success': True, 'details':serializer.data}, status=status.HTTP_200_OK)
                generate_exception(serializer.errors)
                return Response({'success': False, 'details':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            generate_exception(e)
            return Response({'success': False, 'details':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, item_id=None):
        try:
            with transaction.atomic():
                try:
                    item_instance = get_object_or_404(Item, id=item_id)
                except Http404:
                    return Response({'success': False, 'details': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
                serializer = itemSerializer(item_instance, data=request.data, context={'request': request}, partial=True)
                if serializer.is_valid():
                    serializer.save()

                    cache_key = f"item_{item_id}"
                    redis_instance.delete(cache_key)
                    redis_instance.delete("item_list")

                    return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)
                generate_exception(serializer.errors)
                return Response({"success":False, 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            context = generate_exception(e)
            return Response({'success': False, 'details':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id=None):
        try:
            with transaction.atomic():
                item_instance = Item.objects.get(id=item_id)
                if item_instance.bln_active:
                    Item.objects.filter(id=item_id).update(bln_active = False)

                    cache_key = f"item_{item_id}"
                    redis_instance.delete(cache_key)
                    redis_instance.delete("item_list")

                    return Response({"success":True, 'details': "Deleted Successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({'success': False, 'details': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            generate_exception(e)
            return Response({'success': False, 'details':str(e)}, status=status.HTTP_400_BAD_REQUEST)

