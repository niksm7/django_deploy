from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=5000000,default="")
    views = models.IntegerField(default=0)
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to="blog/images",default="")

    def __str__(self):
        return self.title

class BlogComment(models.Model):
    sno = models.AutoField(primary_key = True)
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Blogpost,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13]+"... "+"by "+self.user.username