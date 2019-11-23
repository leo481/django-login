from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import timezone
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist
from .forms import UploadFileForm

import datetime

# Create your views here.

def detail(request, id):
    return HttpResponse(id)

def index(request):
    return HttpResponse('index')

def current_date(request):
    now = datetime.datetime.now()
    timezone_now = timezone.now()
    html = '<html><body>It is now {}.<br><p>timezone:{}</body></html>'.format(now, timezone_now)
    return HttpResponse(html)

def not_found(request):
    raise Http404('not found!!!!!!!!')
    # raise ObjectDoesNotExist

def permission_denied_view(request):
    raise PermissionDenied

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(request.FILES.keys())
        if form.is_valid():
            with open('name.jpg', 'wb') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
            # raise Http404
            return HttpResponseRedirect('/news')
    else:
        form = UploadFileForm()
    return render(request, 'news/upload.html', {'form': form})

import csv
def csvout(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="django_csv.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response

from django.http import StreamingHttpResponse

class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def some_streaming_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    return response

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
def pdfgen(request):
    pdfmetrics.registerFont(TTFont('SimSun', 'SimSun.ttf'))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="djangopdf.pdf"'

    p = canvas.Canvas(response)
    p.setFont('SimSun', 12)

    p.drawString(100, 100, u"Hello World")
    p.drawString(110, 110, u"你好")

    p.showPage()
    p.save()
    return response

def sessiontest(request):
    if request.session.get('test', False):
        return HttpResponse('You have got a session')
    request.session['test'] = True
    return HttpResponse('First came')

def addmess(request):
    from django.contrib import messages
    storage = messages.get_messages(request)

    # if len(storage) == 0:
    #     messages.add_message(request, messages.INFO, '你好吗')
    #     messages.add_message(request, messages.SUCCESS, '我很好')
    storage.used = True
    return render(request, 'news/messagetest.html', {'messages': storage})

