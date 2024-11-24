from django.urls import path
from .views import (MemoListView,MemoDetailView,MemoCreateModelFormView,
                    MemoUpdateModelFormView,MemoDeleteModelFormView,
                    )

urlpatterns =[
    path("memolist/",MemoListView.as_view(),name="memo-list"),
    path("memodetail/<slug:slug>/",MemoDetailView.as_view(),name="memo-detail"),
    path("memocreate/",MemoCreateModelFormView.as_view(),name="memo-create"),
    path("memoupdate/<slug:slug>/",MemoUpdateModelFormView.as_view(),name="memo-update"),
    path("memodelete/<slug:slug>/",MemoDeleteModelFormView.as_view(),name="memo-delete"),
]