from rest_framework import serializers
from author.models  import Book, AuthorBio, Review,Profile,ProfileStatus

from datetime import datetime,timezone
from django.utils.timesince import timesince



class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only =True)
    avatar =  serializers.ImageField (read_only = True)

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileAvatarSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Profile
        fields = ("avatar",)

       

class ProfileStatusSerializer(serializers.ModelSerializer):

    user_profile = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProfileStatus
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
     
     class Meta:
        model = Review
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):

    time_since_publication = serializers.SerializerMethodField()
    #book = serializers.StringRelatedField()
    reviews=ReviewSerializer(many=True , read_only=True)
    
    class Meta:
        model = Book
        fields = "__all__"
        #fields=("title","book")
        #exclude = ("id",'book',)

    def get_time_since_publication(self, object) :   
        publication_date = object.publication_date
        now = datetime.now(timezone.utc)
        delta= timesince(publication_date, now)
    
        return delta


        
class AuthorBioSerializer(serializers.ModelSerializer):
     
     #authorbio= serializers.HyperlinkedRelatedField(many= True, read_only =True, view_name ="apilist")
     authorbio = BookSerializer(many= True , read_only=True)
     #books = serializers.StringRelatedField()
     class Meta:
        model = AuthorBio
        fields = "__all__"


# class BookSerializer(serializers.Serializer):
#     id =serializers.IntegerField(read_only=True)

#     book=serializers.CharField()
#     title=serializers.CharField()
#     description=serializers.CharField()
#     body =serializers.CharField()
#     publication_date=serializers.DateTimeField()
#     active=serializers.BooleanField() 
#     created_at=serializers.DateTimeField(read_only=True)
#     updated_at=serializers.DateTimeField(read_only=True)

#     def create(self,validated_data):
#         print(validated_data)
#         return Book.objects.create(**validated_data)

#     def update(self,instance,validated_data):
#         instance.book            =   validated_data.get("book",instance.book)    
#         instance.title             =   validated_data.get("title",instance.title)
#         instance.description       =   validated_data.get('description',instance.description)
#         instance.body              =   validated_data.get("body",instance.body)
#         instance.publication_date  =   validated_data.get('publication_date',instance.publication_date)
#         instance.active            =   validated_data.get("active",instance.active)
#         instance.created_at        =   validated_data.get("created_at",instance.created_at)
#         instance.updated_at        =   validated_data.get('updated_at',instance.updated_at)
        
#         instance.save()
#         return instance

#     def validate(self,data):
#         if data["title"]==data["description"]:
#             raise serializers.ValidationError("should be diff")
#         return data

#     def validate_title(self,value):
#         if len(value)< 15:
#             raise serializers.ValidationError("length less")
