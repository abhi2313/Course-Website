from django.db import models
from courses.models import Course,UserCourse
from django.contrib.auth.models import User

class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    order_id=models.CharField(max_length=50,null=False)
    payment_id=models.CharField(max_length=50,null=True)
    user_course=models.ForeignKey(UserCourse,null=True,blank=True,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    status=models.BooleanField(default=False)
    
    data=models.DateField(auto_now_add=True)