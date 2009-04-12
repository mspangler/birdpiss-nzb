from django.shortcuts import render_to_response
from nzb.forms import NzbUpload
from nzb.models import Nzb

def upload_nzb(request):
    if request.method == 'POST':
        form = NzbUpload(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            newsgroup = form.cleaned_data['newsgroup']
            media = form.cleaned_data['media']
            fsize = form.cleaned_data['size']
            unit = form.cleaned_data['unit']
            # put the two above together to stick in one field
            size = "%s %s" % (fsize, unit)

            # get file contents to save with out saving file.
            # in theory....
            # i'm going to go ahead and guess that this is going
            # to be a memory pig with large files. might need to
            # rethink this...
            usenet_file = form.cleaned_data.['usenet_file']
            nzb_data = usenet_file.read()

            # save it
            nzb = Nzb(title=title, newsgroup=newsgroup, media=media, size=size, xml_data=nzb_data)
            nzb.save()

            # return some form of success message here or something
            return render_to_response('sucess.html')
    else:
        form = NzbUpload()

    return render_to_response('upload.html', {'form', form})
