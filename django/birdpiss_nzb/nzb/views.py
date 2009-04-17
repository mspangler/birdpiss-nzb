from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from nzbparser import NzbParser
from nzb.models import Nzb


def _get_current_site_url():
    current_site = Site.objects.get_current()
    return current_site.domain

def upload_nzb(request):
    
    if not request.user.is_authenticated():
        return render_to_response('json/success.json',{'message':'fail', 'url': "%s%s" % (_get_current_site_url(), reverse('login')) }, mimetype="application/json")
    
    if request.method == 'POST':
        title = request.POST['title']
        media = request.POST['media']
        user = request.user
        
        # get file contents to save with out saving file.
        # in theory....
        # i'm going to go ahead and guess that this is going
        # to be a memory pig with large files. might need to
        # rethink this...
        usenet_file = request.FILES['usenet_file']
        nzb_data = usenet_file.read()
        
        nzbparser = NzbParser(nzb_data)
        newsgroup = nzbparser.get_first_newsgroup()
        size = nzbparser.get_size_formatted()
        
        # save it
        nzb = Nzb(title=title, newsgroup=newsgroup, media=media, size=size, xml_data=nzb_data, user=user)
        try:
            nzb.save()
            return render_to_response('json/success.json',{'message':'success'})
        except:
            # something failed on the save, return teh_fail
            return render_to_response('json/success.json',{'message':'fail', 'url': 'error' })
        

@login_required
def index(request):
    return render_to_response('index.html',{}, context_instance=RequestContext(request))

def get_json(request, media):
    if not request.user.is_authenticated():
        return render_to_response('json/success.json',{'message':'fail', 'url': "%s%s" % (_get_current_site_url(), reverse('login')) }, mimetype="application/json")
    nzbs = Nzb.objects.filter(media=media)
    return render_to_response('json/media.json',{'message':'success', 'nzbs':nzbs}, mimetype="application/json")

@login_required
def download(request, ids):
    import memzip
    import StringIO
    from django.http import HttpResponse
    
    # parse url to get list of ids
    idlist = ids.split('/')
    
    # get nzbs for id list
    nzbs = Nzb.objects.filter(pk__in=idlist)
    
    # create in memory zip
    imz = memzip.InMemoryZip()
    
    # append each nzb to in memory zip
    for nzb in nzbs:
        fname = "%s.nzb" % nzb.title
        content = nzb.xml_data
        imz.append(fname.encode('utf-8'), content.encode('utf-8'))
    
    # create string object and add zip to it
    tzip = StringIO.StringIO()
    tzip = imz.read()
    
    # create response object of type x-zip-compressed
    response = HttpResponse(tzip, mimetype='application/x-zip-compressed')
    response['Content-Disposition'] = 'attachment; filename=birdpiss.nzb.zip'
    
    return response


def dummy_json(request, media):
    
    return render_to_response('json/test.json',{'media':media}, mimetype="application/json")
