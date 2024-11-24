from django.db import models
from django.contrib.auth import get_user_model
from utils.random_string import *
User = get_user_model()

#検索機能
from django.db.models import Q
from django.utils import timezone

def slug_maker():
    repeat = True
    while repeat:
        new_slug = random_string_generator()
        counter = MemoModel.objects.filter(slug=new_slug).count()
        if counter==0:
            repeat=False
    return new_slug







class MemoModelQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        # qs = qs.filter(public=True) #公開済みの日報のみでQuerySetを作成しています
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)|
                Q(content__icontains=query)            
            )
            qs = qs.filter(or_lookup).distinct()
        return qs.order_by("-date") #新しい順に並び替えてます

class MemoModelManager(models.Manager):
    def get_queryset(self):
        return MemoModelQuerySet(self.model,using=self._db)
    
    def search(self,query=None):
        return self.get_queryset().search(query=query)
        







class MemoModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length =100,verbose_name="タイトル")
    content = models.TextField(max_length=1000,verbose_name="内容")
    public = models.BooleanField(default=False,verbose_name="公開する")
    date = models.DateField(default=timezone.now)
    slug = models.SlugField(max_length=20,default=slug_maker,unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "メモ"
        verbose_name_plural = "メモ一覧"


    objects = MemoModelManager()

    def __str__(self):
       
        return self.title

    def get_profile_page_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy("memo-list") + f"?profile={self.user.profile.id}"