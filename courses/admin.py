from django.contrib import admin
from django.utils.html import format_html
# Register your models here.
from courses.models import Course, Tag, Learning, Prerequisite, Video, UserCourse, Payment,CouponCode

# created 3 class so that we have tag,learning ,prerequisite in bottom of course form.


class TagAdmin(admin.TabularInline):
    model = Tag


class LearningAdmin(admin.TabularInline):
    model = Learning


class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite


class VideoAdmin(admin.TabularInline):
    model = Video


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ['order_id', 'get_user', 'get_course', 'status']
    list_filter = ['status', 'course']

    def get_user(Self, payment):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{payment.user.id}'>{payment.user}</a>")

    def get_course(Self, payment):
        return format_html(f"<a target='_blank' href='/admin/courses/course/{payment.course.id}'>{payment.course}</a>")
    get_course.short_description = "Course"
    get_user.short_description = "User"
class UserCourseModelAdmin(admin.ModelAdmin):
    model = UserCourse
    list_display = ['click','get_user','get_course']
    list_filter = ['course']

    def get_user(Self, usercourse):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{usercourse.user.id}'>{usercourse.user}</a>")

    def get_course(Self, usercourse):
        return format_html(f"<a target='_blank' href='/admin/courses/course/{usercourse.course.id}'>{usercourse.course}</a>")
    def click(Self, usercourse):
        return "Click to Open"

    get_course.short_description = "Course"
    get_user.short_description = "User"


class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin, LearningAdmin, PrerequisiteAdmin, VideoAdmin]
    list_display = ["name", "get_price", "get_discount", "active"]

    list_filter = ("discount", "active")

    def get_discount(self, course):
        return f'{course.discount} %'

    def get_price(self, course):
        return f'₹ {course.price}'

    get_discount.short_description = "Discount"
    get_price.short_description = "Price"


admin.site.register(Course, CourseAdmin)
admin.site.register(Video)
admin.site.register(UserCourse,UserCourseModelAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(CouponCode)