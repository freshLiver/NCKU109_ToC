from nhlib.nhRequest import *
from nhlib.nhGlobal import *


class NhGallery :
    def __init__ ( self, title, link, thumb, tags: list ) :
        self.title = NhGallery.legalize_title( title )
        self.link = link
        self.tags = tags
        self.thumb = thumb
        self.lang = NhGallery.get_lang_from_tags( tags )
    
    
    def gallery_info ( self ) -> list :
        pass
    
    
    """
    ************************
    static methods
    ************************
    """
    
    
    @staticmethod
    def legalize_title ( title: str ) -> str :
        new_title = title
        
        # if any illegal symbol in title, replace it
        for symbol in NhGlobal.illegals :
            if symbol in new_title :
                new_title.replace( symbol, NhGlobal.illegals[symbol] )
        
        return new_title
    
    
    @staticmethod
    def get_lang_from_tags ( tags ) -> str or None :
        if "29963" in tags :
            return "Chinese"
        if "12227" in tags :
            return "English"
        if "6346" in tags :
            return "Japanese"
        return None
    
    
    @staticmethod
    def get_gallery_info_by_url ( url: str ) -> list :
        
        # get raw soup of this gallery
        html = NhRequest.get2soup( url )
        
        #
        
        pass