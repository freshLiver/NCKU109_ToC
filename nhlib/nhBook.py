from nhlib.nhGallery import *
from nhlib.nhRequest import *


class NhBook :
    
    def __init__ ( self ) :
        self.__title = ""
        self.__gallery_link = ""
        self.__gallery_id = 0
        self.__total_pages = 0
        self.__favorites = 0
        self.__images = list( )
    
    
    def set_new_book ( self, link: str ) :
        # use url to get gallery info
        target = NhRequest.get_book_from_gallery( link )
        
        # get all properties of target gallery
        self.__title = target.__title
        self.__gallery_link = target.__gallery_link
        self.__gallery_id = target.__gallery_id
        self.__total_pages = target.__total_pages
        self.__favorites = target.__favorites
        self.__images = target.__images
    
    
    def get_total_pages ( self ) -> int :
        return self.__total_pages
    
    
    def get_link_of_page ( self, page: int ) -> str :
        return self.__images[page]
    
    
    def reset ( self ) :
        self.__title = ""
        self.__gallery_link = ""
        self.__gallery_id = 0
        self.__total_pages = 0
        self.__favorites = 0
        self.__images.clear( )
    
    
    # **********************************************************
    # ********************* private methods ********************
    # **********************************************************
    