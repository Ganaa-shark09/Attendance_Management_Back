from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404,redirect
from .models import *
from django.views.decorators.http import require_http_methods
# Create your views here.

@require_http_methods(["POST"])
def add_student(request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')

        # Retrieve parent data from the form
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        # save parent information
        parent = Parent.objects.create(
            father_name= father_name,
            father_occupation= father_occupation,
            father_mobile= father_mobile,
            father_email= father_email,
            mother_name= mother_name,
            mother_occupation= mother_occupation,
            mother_mobile= mother_mobile,
            mother_email= mother_email,
            present_address= present_address,
            permanent_address= permanent_address
        )

        # Save student information
        student = Student.objects.create(
            first_name= first_name,
            last_name= last_name,
            student_id= student_id,
            gender= gender,
            date_of_birth= date_of_birth,
            student_class= student_class,
            religion= religion,
            joining_date= joining_date,
            mobile_number = mobile_number,
            admission_number = admission_number,
            section = section,
            student_image = student_image,
            parent = parent
        )
        create_notification(request.user, f"Added Student: {student.first_name} {student.last_name}")
        return JsonResponse({'id': student.id, 'slug': student.slug})



@require_http_methods(["GET"])
def student_list(request):
    students = Student.objects.select_related('parent').all()
    data = []
    for s in students:
        data.append({
            'id': s.id,
            'slug': s.slug,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'student_id': s.student_id,
            'gender': s.gender,
            'student_class': s.student_class,
            'parent': {
                'father_name': s.parent.father_name if s.parent else None,
                'mother_name': s.parent.mother_name if s.parent else None,
            }
        })
    return JsonResponse({'results': data})


@require_http_methods(["POST"])
def edit_student(request,slug):
    student = get_object_or_404(Student, slug=slug)
    parent = student.parent if hasattr(student, 'parent') else None
    if True:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')  if request.FILES.get('student_image') else student.student_image

        # Retrieve parent data from the form
        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.father_email = request.POST.get('father_email')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.mother_email = request.POST.get('mother_email')
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')
        parent.save()

#  update student information

        student.first_name= first_name
        student.last_name= last_name
        student.student_id= student_id
        student.gender= gender
        student.date_of_birth= date_of_birth
        student.student_class= student_class
        student.religion= religion
        student.joining_date= joining_date
        student.mobile_number = mobile_number
        student.admission_number = admission_number
        student.section = section
        student.student_image = student_image
        student.save()
        create_notification(request.user, f"Updated Student: {student.first_name} {student.last_name}")
        return JsonResponse({'id': student.id, 'slug': student.slug})


@require_http_methods(["GET"])
def view_student(request, slug):
    student = get_object_or_404(Student, student_id = slug)
    data = {
        'id': student.id,
        'slug': student.slug,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'student_id': student.student_id,
        'gender': student.gender,
        'student_class': student.student_class,
    }
    return JsonResponse(data)


@require_http_methods(["POST"])
def delete_student(request,slug):
        student = get_object_or_404(Student, slug=slug)
        student_name = f"{student.first_name} {student.last_name}"
        student.delete()
        create_notification(request.user, f"Deleted student: {student_name}")
    return JsonResponse({'status': 'deleted'})