from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializers import ItemSerializer
from .models import Item


class KeyValueViewSet(viewsets.ViewSet):
    peers = ["http://127.0.0.1:8001", "http://127.0.0.1:8002"] 

    def list(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        key = pk
        responses = []

        for peer in self.peers:
            try:
                response = requests.get(f"{peer}/store/{key}/")
                if response.status_code == 200:
                    responses.append(response.json()['name'])
                else:
                    print(f"No 200 OK response from {peer}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to connect to {peer}: {e}")

        if len(responses) >= 2:  # Quorum condition
            most_common_value = max(set(responses), key=responses.count)
            return Response({"key": key, "value": most_common_value})
        
        return Response({"error": "Failed quorum read"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        responses = []
        
        for peer in self.peers:
            try:
                response = requests.put(f"{peer}/store/", data=request.data, timeout=2)
                if response.status_code == 201:
                    responses.append(response)
            except requests.exceptions.RequestException as e:
                print(f"Failed to write to {peer}: {e}")

        if len(responses) >= 2: #Quorum condition
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"error": "Failed quorum write"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
