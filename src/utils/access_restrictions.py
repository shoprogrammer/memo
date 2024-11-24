from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

#自分のメモの時だけアクセスできる
class OwnerOnly(UserPassesTestMixin):
    #アクセス制限を行う関数
    def test_func(self):
        memo_instance = self.get_object()
        return memo_instance.user == self.request.user
    
    #Falseの時、リダイレクト先を指定
    def handle_no_permission(self):
        messages.error(self.request,"ご自身のメモでのみ編集・削除可能です")
        return redirect("memo-detail",pk=self.kwargs["pk"])
    
#自分のプロフィールだけ見れるようにする
class OwnProfileOnly(UserPassesTestMixin):
    def test_func(self):
        profile_obj = self.get_object()
        try:
            return profile_obj == self.request.user.profile
        except:
            return False
        