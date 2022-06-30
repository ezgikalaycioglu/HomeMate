from django.urls import path, include

from . import views
from .views import TaskDelete, TaskCreate, TaskUpdate, GroupList, GroupDetail, GroupCreate, JoinGroup, CompleteTask, UnCompleteTask, LeaveList


urlpatterns=[
    # path('',TaskList.as_view(), name='tasks'),
    path('task-create/<int:pk>',TaskCreate.as_view(), name='task-create'),
    path('task-complete/<int:pk>/<int:pkgroup>',CompleteTask, name='task-complete'),
    path('task-uncomplete/<int:pk>/<int:pkgroup>',UnCompleteTask, name='task-uncomplete'),
    path('task-update/<int:pk>/<int:pk_group>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/<int:pk_group>', TaskDelete.as_view(), name='task-delete'),
    path('',GroupList.as_view(), name='group-list'),
    path('group-detail/<int:pk>',GroupDetail, name='group-detail'),
    path('leave-list/<int:pk_group>',LeaveList.as_view(), name='leave-list'),
    path('group-create',GroupCreate.as_view(), name='group-create'),
    path('join-group',JoinGroup.as_view(), name='join-group'),
    # path('overview-api',views.apiOverview, name="api-overview"),
    # path('task-list-api/',views.tasklist, name="task-list-api"),
    # path('task-detail-api/<str:pk>/',views.taskdetail, name="task-detail-api"),
    # path('task-create-api/',views.taskcreate, name="task-create-api"),
    # path('task-update-api/<str:pk>/',views.taskupdate, name="task-update-api"),
    # path('task-delete-api/<str:pk>/',views.taskdelete, name="task-delete-api"),
    
]


