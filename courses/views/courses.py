from django.shortcuts import HttpResponse,render,redirect
from courses.models import Course,Video,UserCourse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator

@login_required(login_url='login')
def my_courses(request):
    user=request.user
    user_courses=UserCourse.objects.filter(user=user)
    context={
        'user_courses':user_courses
    }
    return render(request=request,template_name='courses/my_courses.html',context=context)
    



def coursePage(request,slug):

    course=Course.objects.get(slug=slug)
    serial_number=request.GET.get('lecture')
    videos=course.video_set.all().order_by("serial_number")
    next_lecture=None
    prev_lecture=None
    if serial_number is None:
        serial_number=1
    else: 
        next_lecture=int(serial_number)+1
        if len(videos)<next_lecture:
            next_lecture=None

        prev_lecture=int(serial_number)-1
        if len(videos)<0:
            prev_lecture=None

        


    video=Video.objects.get(serial_number=serial_number,course=course)

    if video.is_preview is False:
        if request.user.is_authenticated is False:
            return redirect("login")
        else:
            try:
                user_course=UserCourse.objects.get(user=request.user,course=course)

            except:
                return redirect('checkout',slug=course.slug)

    
    context={
        "course":course,
        "video":video,
        "videos" :videos,
        "next_lecture":next_lecture,
        "prev_lecture":prev_lecture
    }

    return render(request, "courses/course_page.html",context=context)
    