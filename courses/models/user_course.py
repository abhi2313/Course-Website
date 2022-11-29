from django.db import models
from courses.models import Course
from django.contrib.auth.models import User


# create this object only when payment is complted
class UserCourse(models.Model):
    def __str__(self):
        return f'{self.user.username} -- {self.course.name}'
    user=models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)
    data=models.DateField(auto_now_add=True)