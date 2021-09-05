'''Permissions for various views in the app'''
from rest_framework import permissions

'''safe methods - get/options/head'''
class IsAdmin(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        return False

class  IsAdminOrTeamMember(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        if request.user in obj.members_p.all():
            return True
        return False

class  IsAdminOrTeamMember_l(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        if request.user in obj.project_l.members_p.all():
            return True
        if request.user in obj.members_l.all():
            return True
        return False

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

class IsAdminOrProjectAdmin(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        if request.user in obj.project_admins.all():
            return True
        return False

class CommentEdit(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.user == obj.sender :
            return True
        return False

class NobodyCan(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        return False

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

class CommentPDelete(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        if request.user in obj.project.members_p.all():
            return True
        return request.user == obj.sender
        
