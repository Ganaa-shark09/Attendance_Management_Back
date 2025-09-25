from django.http import HttpResponse, HttpResponseForbidden
from .models import Notification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

# Create your views here.

@api_view(["GET"]) 
@permission_classes([AllowAny])
def index(request):
    return Response({ 'message': 'API is running' })

@api_view(["GET"]) 
@permission_classes([IsAuthenticated])
def dashboard(request):
    unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    return Response({ 'unread_notifications': unread_notification.count() })



@api_view(["POST"]) 
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request):
    notification = Notification.objects.filter(user=request.user, is_read=False)
    notification.update(is_read=True)
    return Response({'status': 'success'})

@api_view(["POST"]) 
@permission_classes([IsAuthenticated])
def clear_all_notification(request):
    notification = Notification.objects.filter(user=request.user)
    notification.delete()
    return Response({'status': 'success'})