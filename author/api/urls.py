from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (book_list_create_api_view,
                   book_slug_create_api_view,
                   book_get_id_api_view,
                   ApiDetailview,
                   Apilistview,
                   AuthorBiolistview,
                   Bookmixlistview,
                   BookCreateconcreteview,
                   AuthorCreateListconcreteview,
                   AuthorBioDetailconcerteview,
                   BookCreateListconcreteview,
                   BookDetailconcerteview,
                   ReviewCreateconcreteview,
                   ReviewDetailconcerteview,
                   Profileslistview,
                   ProfilesViewSet,
                   ProfileStatusViewSet,
                   ProfileAvatarView,
                   ProfileStatuspartiViewSet,
                  
                   )

router = DefaultRouter()
router.register(r'profiles', ProfilesViewSet)
router.register(r'status', ProfileStatusViewSet, basename = "status")
profileviewsetlist = ProfilesViewSet.as_view({'get':'list'})
profileviewsetdetail = ProfilesViewSet.as_view({'get':'retrieve'})

urlpatterns = [
    path('book/', book_list_create_api_view, name='booklist'),
    path('book/<str:slug>/', book_slug_create_api_view, name='bookslug'),
    path('book/<int:pk>/',book_get_id_api_view,name='bookpk'),
    path('apiview/<int:pk>/',ApiDetailview.as_view(),name='apidetail'),
    path('apiview/',Apilistview.as_view(), name='apilist'),
    path('bioapiview/',AuthorBiolistview.as_view(), name='bioapilist'),
    path('bokmixlist/',Bookmixlistview.as_view(), name='book_mix_apilist'),
    path('authorcreatelistcon/',AuthorCreateListconcreteview.as_view(), name='AuthorCreateListconcrete'),
    path('authordetailcon/<int:pk>/',AuthorBioDetailconcerteview.as_view(), name='AuthorBioDetailconcerte'),
    path('bookcreatlistecon/',BookCreateListconcreteview.as_view(), name='BookCreateListconcreteview'),
    path('bokcreatecon/<int:book_pk>/',BookCreateconcreteview.as_view(), name='BookCreateconcrete'),
    path('bokdetailcon/<int:pk>/',BookDetailconcerteview.as_view(), name='BookDeatilconcrete'),
    path('reviewcreatecon/<int:book_pk>/',ReviewCreateconcreteview.as_view(), name='ReviewCreateconcrete'),
    path('reviewdetailcon/<int:pk>/',ReviewDetailconcerteview.as_view(), name='ReviewDetailconcerte'),
    path('Profileslist/',Profileslistview.as_view(), name='Profileslist'),
    path('profileviewsetlist/',profileviewsetlist, name='profileviewsetlist'),
    path('profileviewsetdetail/<int:pk>/',profileviewsetdetail, name='profileviewsetdetail'),
    path("routers/", include(router.urls)),
    path('ProfileAvatarView/',ProfileAvatarView.as_view(), name='ProfileAvatarView'),

    path('ProfileStatuspartiViewSet/',ProfileStatuspartiViewSet.as_view(), name='ProfileStatuspartiViewSet'),
]