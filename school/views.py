from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .models import Notification

# Create your views here.

def index(request):
    return JsonResponse({ 'message': 'API is running' })

def dashboard(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    return JsonResponse({ 'unread_notifications': unread_notification.count() })



def mark_notification_as_read(request):
    if request.method == 'POST':
        notification = Notification.objects.filter(user=request.user, is_read=False)
        notification.update(is_read=True)
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()

def clear_all_notification(request):
    if request.method == "POST":
        notification = Notification.objects.filter(user=request.user)
        notification.delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden