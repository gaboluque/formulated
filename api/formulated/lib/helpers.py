from rest_framework.response import Response
from rest_framework import status

class Helpers:
    
    @staticmethod
    def api_response(data, status=status.HTTP_200_OK):
        return Response(data, status=status)
    
    @staticmethod
    def api_error(error, status=status.HTTP_400_BAD_REQUEST):
        return Response(error, status=status)