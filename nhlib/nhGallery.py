from nhlib.nhRequest import *
from nhlib.nhGlobal import *
from bs4 import element


class NhGallery :
    def __init__ ( self, title, link, thumb, tags: list ) :
        self.title = NhGallery.legalize_string( title )
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
    def legalize_string ( title: str ) -> str :
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
        info_raw = NhRequest.get2soup( url ).find( "div", id = "info" )
        
        # get japanese title
        title_raw = info_raw.find( "h2", class_ = "title" )
        
        # get author, title, other infos
        author = title_raw.find( "span", class_ = "before" ).text
        title = title_raw.find( "span", class_ = "pretty" ).text
        others = title_raw.find( "span", class_ = "after" ).text
        
        # find pages from tags
        pages = -1
        tags = info_raw.find( "section", id = "tags" ).find_all( "div" )
        
        for tag in tags :
            tag_text = tag.contents[0]
            if "Pages" in tag_text :
                pages = tag.span.text
        
        # find favorites from button
        favorites = info_raw.find( "div", class_ = "buttons" ).a.span.span.text[1 :-1]
        pass
        
        return [author, title, others, pages, favorites]


if __name__ == '__main__' :
    res = NhGallery.get_gallery_info_by_url( "https://nhentai.net/g/339502/" )
    pass