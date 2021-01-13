from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# # Create your models here.

class AuthorBio(models.Model):
    firstName = models.CharField(max_length=10)
    lastName = models.CharField(max_length=10)      
    Bio = models.CharField(max_length= 20) 
    Rating = models.PositiveIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])

    def __str__(self):
        return f"{self.firstName} {self.lastName}"



class Book(models.Model):
    author=models.ForeignKey(AuthorBio,on_delete = models.CASCADE, related_name= 'authorbio')
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    body =models.TextField()
    publication_date=models.DateTimeField()
    active=models.BooleanField(default=True)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author} {self.title}"

 
class Review(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE, related_name='review')
    review_user = models.ForeignKey(User,on_delete=models.CASCADE)
    review = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Reviews'

class Profile(models.Model):
    user= models.OneToOneField(User , on_delete= models.CASCADE)
    city = models.CharField(max_length=20,blank=True)
    avatar = models.ImageField(null = True , blank = True)
    
    def __str__(self):
        return  str(self.user.username)

class ProfileStatus(models.Model):
    user_profile = models.ForeignKey(Profile,on_delete= models.DO_NOTHING,blank= False )
    about = models.CharField(max_length=20 , blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    class Meta:
        verbose_name_plural = 'Statuses'
    
    def __str__(self):
          return str(self.about)+str(self.user_profile.user.username)


