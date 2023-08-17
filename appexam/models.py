from django.db import models

# Create your models here.
class Bloguser(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=250,null=False)
    password=models.CharField(max_length=250,null=False)

class Blogpost(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=250,null=False)
    content=models.CharField(max_length=250,null=False)
    created_at=models.BigIntegerField(null=False)
    Blogcreator=models.ForeignKey(Bloguser,on_delete=models.CASCADE,null=True)
