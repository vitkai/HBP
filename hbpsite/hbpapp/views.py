from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.cache import cache

from .models import Transactions, CCY, Category, Document

# own function to handle an uploaded file
from .xlsx_parser import load_file, parse_data
from .db_updates import proc_db_import
from .forms import UploadFileForm, ProcessFileForm


class TransactionsListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Transactions
    paginate_by = 10


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_trans = Transactions.objects.all().count()
    num_ccys = CCY.objects.all().count()
    num_categories = Category.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_trans': num_trans, 'num_ccys': num_ccys,
                 'num_categories': num_categories, 'num_visits': num_visits},
    )


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            # parse(newdoc.docfile.name)
            return HttpResponseRedirect(reverse('upload_file'))
    else:
        form = UploadFileForm() # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    return render(request, 'upload.html', {'documents': documents, 'form': form})
    

def file_view(request, pk):
    item = Document.objects.get(pk=pk)

    check_res = ""
    proc_res = ""
    imp_res = ""
    
    if request.method == 'POST':
        # check if Check_file button is clicked
        if 'check_btn' in request.POST:
            form = ProcessFileForm(request.POST)
            if form.is_valid():
                check_res = load_file(item.docfile.name)
                # get .xlsx tabs list only from returned result
                check_res = check_res[2]
                
                # temporarily save file processing results data
                cache.set(pk, (check_res, proc_res))
        
        # check if Process button is clicked
        elif 'proc_btn' in request.POST:
            form = ProcessFileForm(request.POST)
            if form.is_valid():
                check_res, proc_res = cache.get(pk)
                proc_res = parse_data(item.docfile.name)
                
                # temporarily save file processing results data
                cache.set(pk, (check_res, proc_res))
                
        # check if 'Import data' button is clicked
        elif 'imprt_btn' in request.POST:
            form = ProcessFileForm(request.POST)
            if form.is_valid():
                # restore file processing results data from cache
                check_res, proc_res = cache.get(pk)
                
                # update db with proc_res data
                imp_res = 'Import results placeholder'
                imp_res = proc_db_import(proc_res)
            
    else:
        form = ProcessFileForm() # An empty, unbound form
        
    if "" == str(proc_res):
        nores = True
    else:
        nores = False
        # convert DF to html table
        proc_res = proc_res.to_html(index=False)
    
    return render(request, 'file_view.html', {'item': item, 'form': form, 'check_res': check_res, 'proc_res': proc_res, 'nores': nores, 'imp_res': imp_res})
    # return render(request, 'file_view.html', {'item': item})