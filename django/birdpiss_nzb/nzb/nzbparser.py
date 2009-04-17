import xml.dom.minidom

class NzbParser:
    
    def __init__(self, n):
        self.n = n
    
    def get_dom(self):
        # returns the dom object
        return xml.dom.minidom.parseString(self.n)
    
    def get_first_newsgroup(self):

        dom = self.get_dom()
        node = dom.getElementsByTagName('group')[0]

        return node.childNodes[0].data
    
    def get_size(self):
        # returns the size in bytes
        dom = self.get_dom()
        segments = dom.getElementsByTagName('segment')

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