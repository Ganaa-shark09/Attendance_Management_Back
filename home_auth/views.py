from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import CustomUser, PasswordResetRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer
from rest_framework.response import Response


@csrf_exempt
@require_http_methods(["POST"])
def signup_view(request):
    data = request.POST or {}
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password:
        return JsonResponse({'detail': 'email and password required'}, status=400)

    if CustomUser.objects.filter(email=email).exists():
        return JsonResponse({'detail': 'email already registered'}, status=400)

    user = CustomUser.objects.create_user(
        username=email,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
    )

    if role == 'student':
        user.is_student = True
    elif role == 'teacher':
        user.is_teacher = True
    elif role == 'admin':
        user.is_admin = True
    user.save()

    return JsonResponse({'id': user.id, 'email': user.email})


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    data = request.POST or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return JsonResponse({'detail': 'email and password required'}, status=400)
    user = authenticate(request, username=email, password=password)
    if user is None:
        return JsonResponse({'detail': 'invalid credentials'}, status=401)
    login(request, user)
    return JsonResponse({'id': user.id, 'email': user.email, 'roles': {
        'is_admin': user.is_admin,
        'is_teacher': user.is_teacher,
        'is_student': user.is_student,
    }})


@csrf_exempt
@require_http_methods(["POST"])
def forgot_password_view(request):
    data = request.POST or {}
    email = data.get('email')
    if not email:
        return JsonResponse({'detail': 'email required'}, status=400)
    user = CustomUser.objects.filter(email=email).first()
    if not user:
        return JsonResponse({'detail': 'email not found'}, status=404)
    reset_request = PasswordResetRequest.objects.create(user=user, email=email)
    reset_request.send_reset_email()
    return JsonResponse({'detail': 'reset link sent'})


@csrf_exempt
@require_http_methods(["POST"])
def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(token=token).first()
    if not reset_request or not reset_request.is_valid():
        return JsonResponse({'detail': 'invalid or expired token'}, status=400)
    data = request.POST or {}
    new_password = data.get('new_password')
    if not new_password:
        return JsonResponse({'detail': 'new_password required'}, status=400)
    reset_request.user.set_password(new_password)
    reset_request.user.save()
    return JsonResponse({'detail': 'password reset successful'})


@api_view(["POST"]) 
def logout_view(request):
    logout(request)
    return Response({'detail': 'logged out'})


@api_view(["GET"]) 
@permission_classes([IsAuthenticated])
def me_view(request):
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data)
