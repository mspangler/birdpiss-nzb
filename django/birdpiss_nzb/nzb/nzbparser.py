import xml.dom.minidom

class NzbParser:
    
    def __init__(self, n):
        self.n = n
        self.dom = xml.dom.minidom.parseString(self.n)
    
    def get_first_newsgroup(self):
        # gets the first newsgroup listed
        # not good but close enough for me
        node = self.dom.getElementsByTagName('group')[0]
        
        return node.childNodes[0].data
    
    def get_size(self):
        # returns the size in bytes
        segments = self.dom.getElementsByTagName('segment')
        
        bytes = [int(node.attributes['bytes'].value) for node in segments]
        
        return sum(bytes)
    
    def get_size_formatted(self):
        # returns a string formated size
        b = self.get_size()
        
        kbs = b >> 10
        mbs = kbs >> 10
        gbs = mbs >> 10
        if kbs < 1000:
            size = "%d %s" % (kbs, "KB")
        elif mbs < 1000:
            size = "%d %s" % (mbs, "MB")
        else:
            size = "%d %s" % (gbs, "GB")
        
        return size
    
    def get_oldest_age(self):
        # get the age of oldest file in nzb
        # return python datetime object
        import datetime

        files = self.dom.getElementsByTagName('file')
        
        ages = [node.attributes['date'].value for node in files]
        dta = datetime.datetime.utcfromtimestamp(float(max(ages)))
        
        return dta