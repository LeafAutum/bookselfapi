from rest_framework import permissions



class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    # admin can change anything in any way can change user alone ,can change review alone
    def has_permission(self,request,view):
        Is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or Is_admin


class IsReviewAdminOrReadOnly(permissions.BasePermission):    

    #admin only  and admin entered reviews only

    def has_object_permission(self, request, view, obj):
      if  request.method in permissions.SAFE_METHODS:
          return True

      return obj.review_user == request.user  

class IsUserOrReadOnly(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):
      if  request.method in permissions.SAFE_METHODS:
          return True

      return obj.user == request.user    
       


class IsStatusAdminOrReadOnly(permissions.BasePermission):    

    #admin only  and admin entered reviews only
    # def has_permission(self, request, view):
    #     return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
      Is_admin = bool(request.user and request.user.is_staff)
      
      if  request.method in permissions.SAFE_METHODS or Is_admin:
          #print(obj.user_profile == request.user,obj.user_profile,request.user,"print",request.method,Is_admin)
          return True

      #print(obj.user_profile == request.user,obj.user_profile,request.user)
      return str(obj.user_profile)== str(request.user)  


