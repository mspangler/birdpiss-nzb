from django.shortcuts import render_to_response
from nzb.forms import NzbUpload
from nzb.models import Nzb

def upload_nzb(request):
    if request.method == 'POST':
        title = request.POST['title']
        newsgroup = request.POST['newsgroup']
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

        # save it
        nzb = Nzb(title=title, newsgroup=newsgroup, media=media, size=size, xml_data=nzb_data)
        nzb.save()

        # return some form of success message here or something
        return render_to_response('sucess.html')
    else:
        form = NzbUpload()

    return render_to_response('upload.html', {'form', form})
