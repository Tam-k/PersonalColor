from asyncio.log import logger
import logging
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from .forms import InquiryForm, ImgForm
from .models import Sample
from config.settings import *
import shutil
import os

logger = logging.getLogger(__name__)

class IndexView(generic.FormView):
    template_name = "index.html"
    form_class = ImgForm

    # postメソッドをオーバーライドする
    def post(self, request, *args, **kwargs):
        form = ImgForm(request.POST)

        # 前の画像データを消す
        shutil.rmtree(MEDIA_ROOT)
        os.mkdir(MEDIA_ROOT)

        # フォームから受け取った画像データを保存する
        sample = Sample()
        sample.img = request.FILES['img']

        #テストで追加予定
        #sample.save()

        #sample_imgをresult.htmlで表示できるか
        #削除予定↓
        sample_img = sample.img

        #画像判定モデルの使用
        from personal_color_finder import personal_color_finder
        img = request.FILES['img']
        base_value = personal_color_finder(img)

        #モデルで結果をDBから取り出し
        #ここに処理を書く


        #結果をresult.htmlに送ってHTML生成
        context={"img":sample_img}
        return render(request, 'result.html', context)
        # {
        #     'form': self.form_class , 
        #     #'result': result ,
        #     'sample_img': sample_img,
        #     }
        #)




class InquiryView(generic.FormView):
    template_name = "form.html"
    form_class = InquiryForm
    success_url = reverse_lazy('personal_color:form')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class IntroductionView(generic.TemplateView):
    template_name = "introduction.html"


class LoginView(generic.TemplateView):
    template_name = "login.html"
    

class LogoutView(generic.TemplateView):
    template_name = "signup.html"

class MembersView(generic.TemplateView):
    template_name = "members.html"

class ResultView(generic.TemplateView):
    template_name = "result.html"