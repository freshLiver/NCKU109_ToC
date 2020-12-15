from nhlib.nhRequest import *
from nhlib.nhGallery import *


class NhBook :
    def __init__ ( self, title_info: list, id: int, pages: int, img_links: list ) :
        self.title_info = title_info
        self.id = id
        self.pages = pages
        self.images = img_links
    
    def get_book_info ( self ) -> str :
        info = """
        Title = {0},
        ID    = {1},
        Pages = {2},
        """.format( self.title_info, self.id, self.pages )
        
        return info
    
    
    def get_all ( self ) -> list :
        return self.images
    
    
    def get_page ( self, page: int ) -> list :
        return self.images[page]


# ************************************************
# ************** class test section **************
# ************************************************

if __name__ == '__main__' :
    pass