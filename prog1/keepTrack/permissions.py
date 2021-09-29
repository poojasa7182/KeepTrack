'''Permissions for various views in the app'''
from .models import Users
from rest_framework import permissions

'''safe methods - get/options/head'''

'''if admin or if safe methods'''
class IsAdmin(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        return False

'''accessible only by admins'''
class IsAdminP(permissions.BasePermission):
    def has_permission(self, request, view):
        for p in Users.objects.all().iterator():
            if p.is_admin and p == request.user:
                return True
        return False

'''check if the user is enabled or not'''
class IsEnabeled(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(request.user)
        if(request.user.is_authenticated):
            for p in Users.objects.all().iterator():
                if p.banned and p == request.user:
                    return False
            return True
        return False
'''if the user is an admin or part of the team'''
class  IsAdminOrTeamMember(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        if request.user in obj.members_p.all():
            return True
        return False

'''if the user is part of the team or the list or is an admin'''
class  IsAdminOrTeamMember_l(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method == 'GET' or request.user.is_admin:
            return True
        if request.user in obj.project_l.members_p.all():
            return True
        if request.user in obj.members_l.all():
            return True
        return False

'''if the user is part of the team or the list or the card or is an admin'''
class  IsAdminOrTeamMember_c(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        if request.user in obj.project_c.members_p.all():
            return True
        if request.user in obj.list_c.members_l.all():
            return True
        if request.user in obj.members_c.all():
            return True
        return False

'''if the user id an admin or project admin'''
class IsAdminOrProjectAdmin(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        if request.user in obj.project_admins.all():
            return True
        return False

'''if the user has written that comment'''
class CommentEdit(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.user == obj.sender :
            return True
        return False

'''when the action is not allowed'''
class NobodyCan(permissions.BasePermission):
     def has_permission(self, request, view):
        for p in Users.objects.all().iterator():
            if p.is_admin and p == request.user:
                return False
        return False

'''comments can be deleted by the sender himself or the member of the team or list or card'''
'''comments for cards'''
class CommentCDelete(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        if request.user in obj.cards.list_c.members_l.all():
            return True
        if request.user in obj.cards.project_c.members_p.all():
            return True
        if request.user in obj.cards.members_c.all():
            return True
        return request.user == obj.sender

'''comments can be deleted by the sender himself or the member of the team '''
'''comments for a project'''
class CommentPDelete(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        if request.user in obj.project.members_p.all():
            return True
        return request.user == obj.sender
        
