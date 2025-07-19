from .views import TaskListView,CustomLoginView,RegisterPage,TaskDetailView,TaskReorder,TaskCreateView,TaskUpdateView,TaskDeleteView
from django.urls import path
from django.contrib.auth.views import LogoutView

urlpatterns = [
  path('login/',CustomLoginView.as_view(),name='login'),
  path('logout/',LogoutView.as_view(next_page="login"),name='logout'),
  path('register/',RegisterPage.as_view(),name='register'),
  path('',TaskListView.as_view(),name='tasks'),
  path('task-create/',TaskCreateView.as_view(),name='task-create'),
  path('task/<int:pk>/',TaskDetailView.as_view(),name='task-detail')  ,
  path('task-delete/<int:pk>/',TaskDeleteView.as_view(),name='task-delete')  ,
  path('task-edit/<int:pk>/',TaskUpdateView.as_view(),name='task-update')  ,
  path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),

]