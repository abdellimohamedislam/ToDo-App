from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustomLoginView(LoginView):
    template_name="todo/login.html"
    fields = '__all__'
    redirect_authenticated_user=True

    def get_success_url( self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name= 'todo/register.html'
    form_class= UserCreationForm
    redirect_authenticated_user=True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super().form_valid(form)
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args,**kwargs)
    






class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    fields={'title','description','complete'}
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super().form_valid(form)
        
    

    


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'Tasks'

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["Tasks"] = context["Tasks"].filter(user=self.request.user)
        context["count"] = context["Tasks"].filter(complete=False).count()
        search_input= self.request.GET.get('search-area') or ''
        if search_input :
            context['Tasks'] = context['Tasks'].filter(title__icontains=search_input)

        context['search_input']=search_input
        return context

from django.views import View
from django.db import transaction
from .forms import PositionForm


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))

class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'Task'
    



class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    fields={'title','description','complete'}
    success_url = reverse_lazy('tasks')



class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    context_object_name = 'task'


