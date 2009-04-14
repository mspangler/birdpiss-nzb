from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from nzb.models import Nzb

def _get_newsgroup(n):
    import xml.dom.minidom
    
    dom = xml.dom.minidom.parseString(n)
    node = dom.getElementsByTagName('group')[0]
    
    return node.childNodes[0].data

def upload_nzb(request):
    if not request.user.is_authenticated():
        return render_to_response('json/success.json',{'message':'fail', 'url': 'login'})
    
    if request.method == 'POST':
        title = request.POST['title']
        media = request.POST['media']
        fsize = request.POST['size']
        unit = request.POST['unit']
        # put the two above together to stick in one field
        size = "%s %s" % (fsize, unit)
        
        # get file contents to save with out saving file.
        # in theory....
        # i'm going to go ahead and guess that this is going
        # to be a memory pig with large files. might need to
        # rethink this...
        usenet_file = request.FILES['usenet_file']
        nzb_data = usenet_file.read()
        
        newsgroup = _get_newsgroup(nzb_data)
        
        # save it
        nzb = Nzb(title=title, newsgroup=newsgroup, media=media, size=size, xml_data=nzb_data)
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
    nzbs = Nzb.objects.filter(media=media)
    return render_to_response('json/media.json',{'nzbs':nzbs},mimetype="application/json")

def dummy_json(request, media):
    
    return render_to_response('json/test.json',{'media':media},mimetype="application/json")
