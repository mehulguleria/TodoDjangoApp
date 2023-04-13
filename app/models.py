from django.db import models
from account.models import User


class Todo(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=False)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

