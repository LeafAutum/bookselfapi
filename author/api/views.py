from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from author.models import Book, AuthorBio ,Review,Profile,ProfileStatus
from author.api.serializers import (BookSerializer ,AuthorBioSerializer,ReviewSerializer,
                                     ProfileSerializer,ProfileAvatarSerializer,ProfileStatusSerializer)

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import generics , mixins
from rest_framework import permissions
from author.api.permissions import (IsAdminUserOrReadOnly ,IsReviewAdminOrReadOnly,
                                    IsStatusAdminOrReadOnly,IsUserOrReadOnly)
from rest_framework.exceptions import ValidationError
from author.api.pagination import SmallsetPagination
from rest_framework.viewsets import ReadOnlyModelViewSet , ModelViewSet
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import  User

# from django.shortcuts import render , get_object_or_404
# from django.http import Http404


@api_view(['GET','POST'])
def book_list_create_api_view(request):
    if request.method == 'GET':
        book = Book.objects.filter(active = True)
        Serializer= BookSerializer(book,many=True)
        return Response(Serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def book_slug_create_api_view(request,*args,**kwargs):
   
        if request.method == 'GET':  
          slug=kwargs.get('slug')
          book = Book.objects.filter(title = slug )
          Serializer= BookSerializer(book,many=True)
          return Response(Serializer.data)


@api_view(['GET','PUT','DELETE'])    
def book_get_id_api_view(request,pk):

    try:
        book=Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({"error":{
                                    'code'      : 404,
                                    "message"   : "Object doesnt exists"
                                }},status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
      
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST) 

    elif  request.method == 'DELETE':
          serializer = BookSerializer(book)
          book.delete()
          return Response(serializer.data, status=status.HTTP_302_FOUND)


class Apilistview(APIView):

    def get(self,request):
        book = Book.objects.filter(active = True)
        Serializer= BookSerializer(book,many=True, context={'request': request} )
        return Response(Serializer.data)


    def post(self,request):      
        serializer = BookSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ApiDetailview(APIView):

    def get_object(self,pk) :
        book = get_object_or_404(Book,pk=pk)
        return book

    def get(self,request,pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book,context={'request': request}) # for hyperlinks
        return Response(serializer.data, status=status.HTTP_200_OK,)


    def put(self, request,pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
      
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST) 

    
    def delete(self,request,pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        book.delete()
        return Response(serializer.data, status=status.HTTP_302_FOUND)
     

class AuthorBiolistview(APIView):

    def get(self,request):
        authorbio = AuthorBio.objects.all()
        Serializer= AuthorBioSerializer(authorbio,many=True)
        return Response(Serializer.data)


    def post(self,request):      
        serializer = AuthorBioSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class Bookmixlistview(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView) :

    queryset=Book.objects.all()
    serializer_class =  BookSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class AuthorCreateListconcreteview(generics.ListCreateAPIView):
    queryset = AuthorBio.objects.all()
    serializer_class =  AuthorBioSerializer
    permission_classes= [IsAdminUserOrReadOnly]


class AuthorBioDetailconcerteview(generics.RetrieveUpdateDestroyAPIView):
    queryset=AuthorBio.objects.all()
    serializer_class =  AuthorBioSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class BookCreateListconcreteview(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by('-id')
    serializer_class = BookSerializer 
    #print(request.method)
    permission_classes = [permissions.IsAdminUser]
    pagination_class = SmallsetPagination

class BookCreateconcreteview(generics.CreateAPIView) :
      queryset= Book.objects.all()
      serializer_class =  BookSerializer
     

      def perform_create(self, serializer):
          book_pk= self.kwargs.get("book_pk")
          author= get_object_or_404(AuthorBio, pk = book_pk)
          print(book_pk,author)
          serializer.save(author=author)


class BookDetailconcerteview(generics.RetrieveUpdateDestroyAPIView):
    queryset=Book.objects.all()
    serializer_class =  BookSerializer         


class ReviewCreateconcreteview(generics.CreateAPIView) :
      queryset= Review.objects.all()
      serializer_class =  ReviewSerializer
      permission_classes = [permissions.IsAuthenticatedOrReadOnly]

      def perform_create(self, serializer):
          book_pk= self.kwargs.get("book_pk")
          book= get_object_or_404(Book, pk = book_pk)
          review_user = self.request.user
          review_queryset = Review.objects.filter(book=book,review_user=review_user)
          
          if review_queryset.exists():
              raise ValidationError("u have already review the book")

          print(book_pk,book)
          serializer.save(book=book,review_user=review_user)


class ReviewDetailconcerteview(generics.RetrieveUpdateDestroyAPIView):
      queryset= Review.objects.all()
      serializer_class =  ReviewSerializer 
      permission_classes = [IsAdminUserOrReadOnly]


class Profileslistview(generics.ListAPIView):
    queryset= Profile.objects.all()
    serializer_class =  ProfileSerializer 
    permission_classes = [IsAdminUserOrReadOnly]


class ProfilesViewSet(mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset= Profile.objects.all()
    serializer_class =  ProfileSerializer 
    permission_classes = [permissions.IsAuthenticated,IsUserOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["city"]


# class ProfilesViewSet(ReadOnlyModelViewSet):
#     queryset= Profile.objects.all()
#     serializer_class =  ProfileSerializer 
#     permission_classes = [permissions.IsAuthenticated,IsAdminUserOrReadOnly]
#     filter_backends = [SearchFilter]
#     search_fields = ["city"]
     

class ProfileStatusViewSet(ModelViewSet) :
    queryset= ProfileStatus.objects.all()
    serializer_class =  ProfileStatusSerializer
    permission_classes = [permissions.IsAuthenticated,IsStatusAdminOrReadOnly]


    def get_queryset(self):
        queryset= ProfileStatus.objects.all()
        #print(queryset)
        user_name= self.request.query_params.get("username",None)
        print(user_name)
        if user_name is not None:
            queryset = queryset.filter(user_profile__user__username=user_name)
        return queryset


    def perform_create(self, serializer):
        
        user_profile = self.request.user.profile
        serializer.save(user_profile = user_profile)
        print(serializer.data)


class ProfileAvatarView(generics.UpdateAPIView):   
   
    serializer_class =  ProfileAvatarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        Profile_object = self.request.user.profile
        return Profile_object

class ProfileStatuspartiViewSet(generics.UpdateAPIView,generics.ListAPIView) :
   
    
    serializer_class =  ProfileStatusSerializer
    permission_classes = [permissions.IsAuthenticated,IsStatusAdminOrReadOnly]   
 
    def get_queryset(self):
        Profile_object = self.request.user.profile
        query = ProfileStatus.objects.all()
        query= query.filter(user_profile__user__username = Profile_object)
        print(query,"query")
        return query
    
    def get_object(self):
        Profile_object = self.request.user.profile
        query = ProfileStatus.objects.all()
        #query = get_object_or_404(ProfileStatus,user_profile__user__username = Profile_object).first()
        query= query.filter(user_profile__user__username = Profile_object).first()
        print(query,"query",Profile_object)
        # if query is None:
        #      user_profile = self.request.user.profile
        #      serializer = ProfileStatusSerializer(data =self.request.data)
        #      serializer.is_valid()
        #      serializer.save()
        #      return Response(serializer.data)

        return query
    
    # def perform_update(self, serializer):
    #     instance = self.get_object
    #     if instance is None:
    #          user_profile = self.request.user.profile
    #          serializer.save(user_profile = user_profile)
    #          return Response(serializer.data)
    #     serializer.save()


