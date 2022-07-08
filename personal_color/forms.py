from cProfile import label
import os
from django import forms
from .models import Sample
from django.core.mail import EmailMessage
from django.db import models

class InquiryForm(forms.Form):
    CHOICE = {
    ('0', 'アプリについて'),
    ('1', '商品について'),
    ('2', 'その他について'),
}

    name = forms.CharField(label='お名前', max_length=30)
    email = forms.EmailField(label='メールアドレス')
    title = forms.ChoiceField(label='お問い合わせの種類', widget=forms.Select, choices= CHOICE, initial=0)
    message = forms.CharField(label='お問い合わせ内容', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class']='form-control'
        self.fields['name'].widget.attrs['placeholder']='山田 太郎'

        self.fields['email'].widget.attrs['class']='form-control'
        self.fields['email'].widget.attrs['placeholder']='xxx@email'

        self.fields['title'].widget.attrs['class']='form-control'

        self.fields['message'].widget.attrs['class']='form-control'
        self.fields['message'].widget.attrs['rows']='3'


    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせの種類{}'.format('title')
        message = '送信者名: {0}\nメールアドレス: {1}\nお問い合わせの種類{2}\nお問い合わせ内容:\n{3}'.format(name, email, title, message)
        from_email = os.environ.get('FROM_EMAIL')
        to_list = [
            os.environ.get('FROM_EMAIL')
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message,
        from_email=from_email, to=to_list, cc=cc_list)
        message.send()


class ImgForm(forms.ModelForm):
    # id = models.IntegerField()
    # color_id = models.IntegerField()
    # sex = models.IntegerField()
    # name = models.CharField(max_length=20)
    # explanaion = models.CharField(max_length=100)
    # price = models.IntegerField()
    # size = models.ImageField()
    # maker =  models.CharField(max_length=20)


    class Meta:
        model = Sample
        fields = ('img','id','color_id',
        'sex','name','explanaion','price',
        'size','maker')
        labels = {'id':'ID',
        'color_id':'color_id','sex':'性別',
        'name':'名前','explanaion':'商品説明',
        'price':'値段','size':'サイズ','maker':'メーカー'}
