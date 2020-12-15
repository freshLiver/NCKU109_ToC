class NhBook :
    def __init__ ( self ) :
        self.title_info = None
        self.gallery_id = None
        self.pages = None
        self.images = None
    
    
    def set_book ( self, title_info: list, gallery_id: int, pages: int, img_links: list ) :
        self.title_info = title_info
        self.gallery_id = gallery_id
        self.pages = pages
        self.images = img_links
    
    
    def get_book_info ( self ) -> str :
        info = """
        Author  = {0}
        Title   = {1}
        Info    - {2}
        ID      = {3}
        Pages   = {4}
        """.format( self.title_info[0], self.title_info[1], self.title_info[2]
                    , self.gallery_id, self.pages )
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