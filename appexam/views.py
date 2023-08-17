from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers, models
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
import jwt

#creating a function for generate token 

def generatetoken(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=10),
        'iat': datetime.utcnow()
    }
    accessToken = jwt.encode(payload, 'secret', algorithm='HS256')
    return accessToken

class Blogusersignup(APIView):#cannot find error in sign up therefore cannot debug code..code written without testing,documentation also cannot be made.
    def post(self, request):
        serializer = serializers.BloguserSerializer(data=request.data)

        if serializer.is_valid():
            user_name = serializer.validated_data.get("username")

            if models.Bloguser.objects.filter(username=user_name).exists():
                return Response({'message': 'User already exists'})
            
            serializer.save(password = make_password(serializer.validated_data.get('password')))
            return Response({"message": "Bloguser signed up successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class Bloguserlogin(APIView):
    def post(self, request):
        serializer = serializers.BloguserSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data.get('username')
            pass_word = serializer.validated_data.get('password')

            try:
                bloguser = models.Bloguser.objects.get(username=user_name)
            except models.Bloguser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            if check_password(pass_word, bloguser.password):
                token = generatetoken(bloguser)
                response = Response()
                response.set_cookie('access_token', value=token, httponly=True)
                response.data = {
                    'message': 'Bloguser login successful',
                    'access_token': token
                }
                return response
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Createpost(APIView):
    def post(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = serializers.BlogpostSerializer(data=request.data)
        if serializer.is_valid():
            bloguser = models.Bloguser.objects.get(id=payload['user_id'])
            serializer.save(Blogcreator=bloguser)
            return Response({"message": "Post created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ReadPosts(APIView):
    def get(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        posts = models.Blogpost.objects.all()
        serializer = serializers.BlogpostSerializer(posts, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

class Updatepost(APIView):
    def put(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.DecodeError:
            return Response({'error': 'Token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        user = models.Bloguser.objects.get(id=payload['user_id'])
        post_id = request.query_params.get('post_id')

        try:
            post = models.Blogpost.objects.get(id=post_id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        if post.Blogcreator != user:
            return Response({"error": "You are not the owner of this post"}, status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.BlogpostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Post updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class DeletePost(APIView):
    def delete(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            return Response({'message': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        user = models.Bloguser.objects.get(id=payload['user_id'])
        post_id = request.query_params.get('post_id')

        try:
            post = models.Blogpost.objects.get(id=post_id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        if post.Blogcreator != user:
            return Response({"error": "You are not the owner of this post"}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)