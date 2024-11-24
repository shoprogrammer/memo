from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import MemoModel

class MemoModelForm(forms.ModelForm):
    date = forms.DateField(
        label="作成日",
        widget=DatePickerInput(format='%Y-%m-%d')

    )
    class Meta:
        model = MemoModel
        exclude = ["user"]
        # fields = "__all__"

    def __init__(self,user=None,*args,**kwargs):
        
        for key,field in self.base_fields.items():
            if key != "public":
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs["class"] = "form-check-input"



        self.user = user
        super().__init__(*args,**kwargs)





    def save(self,commit=True):
        memo_obj = super().save(commit=False)
        if self.user:
            memo_obj.user = self.user
        if commit:
            memo_obj.save()
        return memo_obj







class MemoFormClass(forms.Form):
    title = forms.CharField(label = "タイトル",widget=forms.TextInput(attrs={'placeholder':'タイトル...'}))
    content = forms.CharField(label = "内容",widget=forms.Textarea(attrs={'placeholder':'内容...'}))
    
    def __init__(self,*args,**kwargs):
        
        for field in self.base_fields.values():
            field.widget.attrs.update({"class":"form-control"})


        super().__init__(*args,**kwargs)