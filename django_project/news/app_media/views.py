from _csv import reader
from decimal import Decimal

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView

from app_media.forms import FileUploadForm, DocumentForm, MultiFileUpload

from app_media.models import Goods, File


class FileUploadView(FormView):
    template_name = 'media/upload_file.html'
    form_class = FileUploadForm

    def post(self, request, *args, **kwargs):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # file = form.cleaned_data.get('file').read()
            file = request.FILES.get('file').read()
            file_str = file.decode('utf-8').split('\n')
            print(file_str)
            csv_reader = reader(file_str, delimiter=',', quotechar='"')
            for row in csv_reader:
                good = Goods.objects.filter(vendor_code=row[0]).first()
                if good:
                    good.quantity = Decimal(row[1])
                    good.price = Decimal(row[2])
                    good.save()
                else:
                    Goods.objects.create(
                        vendor_code=row[0],
                        quantity=Decimal(row[1]),
                        price=Decimal(row[2])
                    )
        return redirect('table-goods')


class TableView(View):
    def get(self, request):
        goods = Goods.objects.all()
        return render(request, 'media/table.html', context={
            'goods': goods
        })


class DocumentUploadView(FormView):
    template_name = 'media/upload_file.html'
    form_class = DocumentForm

    def post(self, request, *args, **kwargs):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')


class MultipleFilesUploadView(FormView):
    template_name = 'media/upload_file.html'
    form_class = MultiFileUpload

    def post(self, request, *args, **kwargs):
        form = MultiFileUpload(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for file in files:
                instance = File(file=file)
                instance.save()

            return redirect('/')
