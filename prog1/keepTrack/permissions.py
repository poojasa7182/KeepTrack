'''Permissions for various views in the app'''
from rest_framework import permissions

class IsAdmin(permissions.Basepermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        return False

class  IsAdminOrTeamMember(permissions.Basepermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        if request.user in obj.members_p.all():
            return True
        return False

class  IsAdminOrTeamMember_l(permissions.Basepermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        if request.user in obj.project_l.members_p.all():
            return True
        if request.user in obj.members_l.all():
            return True
        return False

class  IsAdminOrTeamMember_c(permissions.Basepermission):
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

class IsAdminOrProjectAdmin(permissions.Basepermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        if request.user in obj.project_admins.all():
            return True