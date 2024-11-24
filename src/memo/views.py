from typing import Any
from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,FormView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import MemoModel
from .form import MemoModelForm,MemoFormClass
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from utils.access_restrictions import OwnerOnly

from .filters import MemoModelFilter

from accounts.models import Profile
        






class MemoListView(ListView):
    template_name = "memo/memo-list.html"
    model = MemoModel
    

    # def get_queryset(self):
    #     qs = MemoModel.objects.all()    
    #     if self.request.user.is_authenticated:
    #         qs = qs.filter(Q(public=True)|Q(user=self.request.user))
    #     else:
    #         qs = qs.order_by("-timestamp")

    #     return qs


    def get_queryset(self):
        q = self.request.GET.get("search")
        qs = MemoModel.objects.search(query=q)
        if self.request.user.is_authenticated:
            qs = qs.filter(Q(public=True)|Q(user=self.request.user))
        else:
            qs = qs.filter(public=True)
        return qs
    

        
    
 
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args,**kwargs)
        ctx["filter"] = MemoModelFilter(self.request.GET,queryset=self.get_queryset())
        profile_id = self.request.GET.get("profile")
        q = Profile.objects.filter(id=profile_id)
        if q.exists():
            ctx["profile"] = q.first()
        return ctx


class MemoDetailView(DetailView):
    template_name = "memo/memo-detail.html"
    model = MemoModel
    
    def get_object(self):
        return super().get_object()
    
class MemoCreateModelFormView(LoginRequiredMixin,CreateView):
    template_name = "memo/memo-form.html"
    form_class = MemoModelForm
    success_url = reverse_lazy("memo-list")

    def get_form_kwargs(self,*args,**kwargs):
        kwags = super().get_form_kwargs(*args,**kwargs)
        kwags["user"]=self.request.user
        return kwags



class MemoUpdateModelFormView(OwnerOnly,UpdateView):
    template_name = "memo/memo-form.html"
    model = MemoModel
    form_class = MemoModelForm
    success_url = reverse_lazy("memo-list")


class MemoDeleteModelFormView(OwnerOnly,DeleteView):
    template_name = "memo/memo-delete.html"
    model = MemoModel
    success_url = reverse_lazy("memo-list")

#以下未使用

class MemoCreateFormView(FormView):
    template_name = "memo/memo-form.html"
    form_class = MemoFormClass
    success_url = reverse_lazy("memo-list")

    def form_valid(self,form):
        data = form.cleaned_data
        obj = MemoModel(**data)
        obj.save()
        return super().form_valid(form)



def memoListView(request):
    template_name = "memo/memo-list.html"
    ctx = {}
    qs = MemoModel.objects.all()
    ctx["object_list"] = qs
    return render(request,template_name,ctx)

def memoDetailView(request,pk):
    template_name = "memo/memo-detail.html"
    ctx= {}
    # q = MemoModel.objects.get(pk = pk)
    q = get_object_or_404(MemoModel,pk = pk)
    ctx["object"] = q
    return render(request,template_name,ctx)

def memoCreateView(request):
    template_name = "memo/memo-form.html"
   #formを渡す作業
    form = MemoFormClass(request.POST or None)
    ctx = {}
    ctx["form"] = form
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj = MemoModel(title = title,content = content)
        obj.save()
        return redirect("memo-list")
    return render(request,template_name,ctx)

def memoUpdateView(request,pk):
    template_name = "memo/memo-form.html"
    # obj = MemoModel.objects.get(pk=pk)
    obj = get_object_or_404(MemoModel,pk=pk)
    initial_values = {"title":obj.title,"content":obj.content}
    form = MemoFormClass(request.POST or initial_values)
    ctx = {"form":form}
    ctx["object"] = obj
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj.title = title
        obj.content = content
        obj.save()
        if request.POST:
            return redirect("memo-list")
    return render(request,template_name,ctx)

def memoDeleteView(request,pk):
    template_name="memo/memo-delete.html"
    obj = get_object_or_404(MemoModel,pk=pk)
    ctx = {"object":obj}
    if request.POST:
        obj.delete()
        return redirect("memo-list")
    return render(request,template_name,ctx)