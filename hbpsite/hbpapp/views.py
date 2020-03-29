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
    conf = ""
    proc_res = ""
    imp_res = ""
    #fields = ['placeholder']
    
    if request.method == 'POST':
        # check if Check_file button is clicked
        if 'check_btn' in request.POST:
            #form = ProcessFileForm(request.POST)
            #if form.is_valid():
            check_res = load_file(item.docfile.name)
            # get .xlsx tabs list only from returned result
            conf = check_res[0]
            check_res = check_res[2]
            
            form = ProcessFileForm(dynamic_field_names=(conf, check_res))
            
            # temporarily save file processing results data
            cache.set(pk, (conf, check_res, proc_res))
        
        # check if Process button is clicked
        elif 'proc_btn' in request.POST:
            # restore file processing results data from cache
            conf, check_res, proc_res = cache.get(pk)

            form = ProcessFileForm(dynamic_field_names=(conf, check_res))
            #form = ProcessFileForm(request.POST or None, dynamic_field_names=request.POST['xlsx_tabs'])
            #form = ProcessFileForm(request.POST or None)
            # msg=f"POST.xlsx_tabs={int(request.POST['xlsx_tabs'])}"
            # print(msg)
            print(request.POST)
            selection = int(request.POST['xlsx_tabs'])
            conf_sel = int(request.POST['conf'])
            conf_sel = dict(form.fields['conf'].choices)[conf_sel]
            # msg=f"conf_sel = {conf_sel}"
            #print(msg)
            #if form.is_valid():
            #selection = form.cleaned_data['xlsx_tabs']
            #selection = dict(form.fields['xlsx_tabs'].choices)[selection]
    
            proc_res = parse_data(item.docfile.name, tab_id=selection, conf_id=conf_sel)
    
            # temporarily save file processing results data
            cache.set(pk, (conf, check_res, proc_res))
                
        # check if 'Import data' button is clicked
        elif 'imprt_btn' in request.POST:
            # form = ProcessFileForm(request.POST)
            # if form.is_valid():
            
            # restore file processing results data from cache
            conf, check_res, proc_res = cache.get(pk)
            
            form = ProcessFileForm(dynamic_field_names=(conf, check_res))
            
            # update db with proc_res data
            imp_res = 'Import results placeholder'
            imp_res = proc_db_import(proc_res)
            
    else:
        form = ProcessFileForm(dynamic_field_names=('', '')) # An empty, unbound form
        # form = ProcessFileForm() # An empty, unbound form
        
    if "" == str(proc_res):
        nores = True
    else:
        nores = False
        # convert DF to html table
        proc_res = proc_res.to_html(index=False)
    
    return render(request, 'file_view.html', {'item': item, 'form': form, 'check_res': check_res, 'proc_res': proc_res, 'nores': nores, 'imp_res': imp_res})

    