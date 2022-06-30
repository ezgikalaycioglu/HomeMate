import random
import string
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import uuid 

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



class Group(models.Model):
    class Meta:
        constraints=[models.UniqueConstraint(fields=['groupcode'],name='uniquegroupname')]
    groupcode=models.CharField(max_length=10, unique=True, null=True, blank=True)
    groupname=models.CharField('List Name', max_length=200)

    def save(self):
        if not self.groupcode:
            # Generate ID once, then check the db. If exists, keep trying.
            self.groupcode = id_generator()
            while Group.objects.filter(groupcode=self.groupcode).exists():
                self.groupcode = id_generator()
        super(Group, self).save()

    def __str__(self):
        return self.groupname

class GroupMember(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    groups=models.ManyToManyField(Group)

    def __str__(self):
        return self.user.username


class Task(models.Model):
    group= models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    completed= models.BooleanField(default=False, blank=True, null=True)
    quantity=models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['completed']

