from rest_framework import serializers
from . import models

class BloguserSerializer(serializers.Serializer):
    class Meta:
        model=models.Bloguser
        fields=('id','username','password')
        read_only_fields=('id',)


class BlogpostSerializer(serializers.Serializer):
    class Meta:
        model=models.Blogpost
        fields=('id','title','content','created_at','Bloguser')
        read_only_fields=('id',)

