'''models used - user, project, lists, cards, comment_c/l/p'''
from django.db import models
from django.db.models.base import Model
from django.db.models.constraints import UniqueConstraint
from django.db.models.deletion import SET_NULL
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField 

# Create your models here.
class User(models.Model):
    '''
    user details
    username,name,
    admin-True/False,
    banned-True/False,
    details-position/branch/year
    '''

    username = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    details = models.CharField(max_length=200)
    banned = models.BooleanField(default=False)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

class Project(models.Model):
    '''
    Project details
    project name, start date, end/due date, creator, members,
    completed- True/False
    wiki-primary details abt the project 
    '''

    project_name = models.CharField(max_length=200,unique=True)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    wiki = RichTextField()
    is_completed = models.BooleanField(default=False)
    creator = models.ForeignKey(to=User, null=True, on_delete=SET_NULL)
    members_p = models.ManyToManyField(User, related_name='members_p')

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.project_name

class List(models.Model):
    '''
    Lists in a project
    list name, related project, start date, end/due date,
    completed-true/false
    tags-according to importance
    members- assigned to work on the list 
    '''

    list_name = models.CharField(max_length=200,unique=False)
    project_l = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    tags_l = TaggableManager()
    members_l = models.ManyToManyField(User, related_name='members_l')


    class Meta(object):
        ordering = ['due_date']
        '''unique list names in a particular project model'''
        UniqueConstraint(fields=['list_name','project_l'], name='unique_list')

    def __str__(self):
        return self.list_name

class Card(models.Model):
    '''
    Cards in a list of a particular project
    card name, list and project of that card, start date, end/due date,
    completed-true/false,
    members-assigned to work on the particular card,
    description-work to be done
    tags- accn to the importance/requirement
    '''

    card_name = models.CharField(max_length=200,unique=False)
    list_c = models.ForeignKey(to=List, on_delete=models.CASCADE)
    project_c = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    members_c = models.ManyToManyField(User)
    description = models.TextField()
    tags_c = TaggableManager()

    class Meta(object):
        ordering = ['due_date']
        '''unique card names in a particular list model'''
        UniqueConstraint(fields=['list_c','card_name'], name='unique_card')

    def __str__(self):
        return self.card_name

class Comment(models.Model):
    '''
    Comments for a particular card/list/project
    '''

    comment_content = models.TextField()
    sender = models.ForeignKey(to=User, null=True, on_delete=SET_NULL)
    time = models.DateTimeField()
    card = models.ForeignKey(to=Card, blank=True, on_delete=models.CASCADE)
    list = models.ForeignKey(to=List, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project,on_delete=models.CASCADE)

    class Meta(object):
        ordering = ['time']

    def __str__(self):
        return self.comment_content

