from asyncio import tasks
from pickle import GET
from tokenize import group
from typing import List
from django.shortcuts import redirect, render
from django.views import View
#from django.http import HttpResponse, JsonResponse

#from rest_framework.decorators import api_view
#from rest_framework.response import Response

#from .serializers import TaskSerializer
from .models import Group, Task, GroupMember



from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# class TaskList(LoginRequiredMixin, ListView):
#     model=Task
#     context_object_name='tasks'
#     template_name='task-list.html'
        
def GroupDetail(Request,pk): #lists the tasks and groupmembers 
    groupmembers=GroupMember.objects.filter(groups__id=pk)
    groupid=pk
    groupname=Group.objects.get(pk=groupid).groupname
    groupcode=Group.objects.get(pk=groupid).groupcode
    return render(Request,'api/group-detail.html', {'groupmembers':groupmembers,'groupid':groupid, 'groupname':groupname, 'groupcode':groupcode} )

def CompleteTask(Request,pk,pkgroup):
    if(Request.GET.get('mybtn')):
        taskgroupid=Group.objects.get(pk=pkgroup).id
        task=Task.objects.filter(group=taskgroupid).get(pk=pk)
        task.completed=True
        task.save(update_fields=["completed"])
        return redirect("task-create", pkgroup)

def UnCompleteTask(Request,pk,pkgroup):
    if(Request.GET.get('mybtnuc')):
        taskgroupid=Group.objects.get(pk=pkgroup).id
        task=Task.objects.filter(group=taskgroupid).get(pk=pk)
        task.completed=False
        task.save(update_fields=["completed"])
        return redirect("task-create", pkgroup)

class GroupList(LoginRequiredMixin, ListView): #lists the groups of the customer 
    model=Group
    context_object_name='groups'
    template_name='api/group-list.html' 
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['groups']=context['groups'].filter(groupmember=self.request.user.groupmember)
        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    model=Task
    fields=['title', 'quantity']
    
    def get_success_url(self, **kwargs):
        return reverse("task-create", kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['tasks']=Task.objects.filter(group__id=self.kwargs.get('pk'))
        context['groupid']=self.kwargs.get('pk')
        context['groupname']=Group.objects.get(id=self.kwargs.get('pk')).groupname
        search_input=self.request.GET.get('search_area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__startswith=search_input)
        
        context['search_input']=search_input
        return context

    def form_valid(self,form):
        form.instance.group=Group.objects.get(pk=self.kwargs.get('pk'))
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model=Task
    fields=['title', 'completed', 'quantity']

    def get_success_url(self, **kwargs):
        return reverse("task-create", kwargs={'pk': self.kwargs.get('pk_group')})
    
    def form_valid(self,form):
        form.instance.group=Group.objects.get(pk=self.kwargs.get('pk_group'))
        return super(TaskUpdate, self).form_valid(form)

class TaskDelete(LoginRequiredMixin, DeleteView):
    model=Task
    fields=['title', 'completed']

    def get_success_url(self, **kwargs):
        return reverse("task-create", kwargs={'pk': self.kwargs.get('pk_group')})

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['groupid']=self.kwargs.get('pk_group')
        return context
    
class GroupCreate(LoginRequiredMixin, CreateView):
    model=Group
    fields=['groupname']

    def get_success_url(self, **kwargs):
        return reverse("group-list")

    def form_valid(self, form):
        self.object=form.save()
        self.request.user.groupmember.groups.add(self.object)
        return super(GroupCreate, self).form_valid(form)

class JoinGroup(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'api/joingroup.html', {'message':"Please enter list code"})

    def post(self, request, *args, **kwargs):
        if 'submit' in request.POST:
            gc=request.POST['groupCode']
            if Group.objects.filter(groupcode=gc).exists():
                try:
                    self.request.user.groupmember.groups.add(Group.objects.get(groupcode=gc))
                    return redirect("group-list")
                except:
                    return render(request, 'api/joingroup.html', {'message':"You already added this list"})
            else:
                return render(request, 'api/joingroup.html', {'message':"Please enter a valid list code"})
        return render(request, 'api/joingroup.html', {'message':"Please enter list code"})

class LeaveList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'api/leavelist.html', {'message':"Are you sure you want to leave this list?", 'groupid':self.kwargs.get('pk_group')})
    def post(self, request, *args, **kwargs):
        if 'submit' in request.POST:
            group_id=self.kwargs.get('pk_group')
            try:
                self.request.user.groupmember.groups.remove(Group.objects.get(pk=group_id))
                return redirect("group-list")
            except:
                Group.objects.get(pk=group_id).delete()
                return redirect("group-list")   
        return render(request, 'api/leavelist.html', {'message':"Are you sure you want to leave this list?", 'groupid':self.kwargs.get('pk_group')})






###############FOR REST API--to use later#########
# @api_view(['GET'])
# def apiOverview(request):
#     api_urls={
#         'List':'/task-list/',
#         'Detail View': '/task-detail/<str:pk>/',
#         'Create':'/task-create/',
#         'Update': '/task-update/<str:pk>/',
#         'Delete': '/task-delete/<str:pk>/',
#     }
#     return Response(api_urls)

# @api_view(['GET'])
# def tasklist(request):
#     tasks=Task.objects.all()
#     serializer=TaskSerializer(tasks, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def taskdetail(request,pk):
#     tasks=Task.objects(id=pk)
#     serializer=TaskSerializer(tasks, many=False)
#     return Response(serializer.data)

# @api_view(['POST'])
# def taskcreate(request):
#     serializer=TaskSerializer(data=request.data)

#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)


# @api_view(['POST'])
# def taskupdate(request,pk):
#     task=Task.objects.get(id=pk)
#     serializer=TaskSerializer(instance=task, data=request.data)

#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# @api_view(['DELETE'])
# def taskdelete(request,pk):
#     task=Task.objects.get(id=pk)
#     task.delete()
#     return HttpResponse("deleted")