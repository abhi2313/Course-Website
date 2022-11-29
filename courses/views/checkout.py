from django.shortcuts import HttpResponse, render, redirect
from courses.models import Course, Video
from coursewebsite.settings import KEY_ID, KEY_SECRET
from time import time
from courses.models import Payment, UserCourse, CouponCode
import razorpay
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


@login_required(login_url='/login')
def checkOut(request, slug):

    course = Course.objects.get(slug=slug)

    user = request.user

    action = request.GET.get('action')
    couponcode = request.GET.get('couponcode')
    coupon_code_message = None
    coupon = None
    order = None
    payment = None
    error = None
    amount = None
    try:
        # if user already taken the course so restrict user for making this payment.
        user_course = UserCourse.objects.get(user=user, course=course)
        error = "You are already enrolled in this course"
    except:
        pass
    if error is None:
        price = course.price
        discount = course.discount
        amount = int((price-(price * discount*.01))*100)
    
    if couponcode:
        try:
            coupon = CouponCode.objects.get(course=course, code=couponcode)
            amount=course.price-(course.price*coupon.discount*.01)
            amount=int(amount)*100
        except:
            coupon_code_message = "invalid coupon code"
    print("amount: ",amount)


    # if amount is zero dont created the payment.only save enrollment object.
    if amount == 0:
        # enroll direct
        userCourse = UserCourse(
            user=user, course=course)
        userCourse.save()
        return redirect("my-courses")
    

    if action == 'create_payment':
        currency = "INR"
        notes = {
            "Email": user.email,
            "Name": f'{user.first_name} {user.last_name}',
        }
        receipt = f"course_website -{int(time())}"
        order = client.order.create({'receipt': receipt,
                                    'notes': notes,
                                     'amount': amount,
                                     'currency': currency
                                     })

        payment = Payment()
        payment.user = user
        payment.course = course
        payment.order_id = order.get('id')
        payment.save()

    context = {
        "course": course,
        "order": order,
        "payment": payment,
        "user": user,
        "error": error,
        "coupon": coupon,
        "coupon_code_message": coupon_code_message
    }

    return render(request, "courses/check_out.html", context=context)


@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = request.POST
        context = {}
        try:
            client.utility.verify_payment_signature(data)

            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            userCourse = UserCourse(user=payment.user, course=payment.course)
            userCourse.save()

            payment.user_course = userCourse
            payment.save()
            return redirect("my-courses")
        except:
            return HttpResponse("invalid payment detail")
