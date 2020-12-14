from nhlib.nhRequest import *


class NhGallery :
    
    def __init__ ( self, title: str, link: str, cover: str, tags: list ) :
        self.title = NhGallery.legalize_string( title )
        self.link = link
        self.tags = tags
        self.cover = cover
        self.lang = NhGallery.get_lang_from_tags( tags )
    
    
    def gallery_info ( self ) -> list :
        return [self.title, self.link, self.tags, self.lang, self.cover]
    
    
    # ************************************************
    # **************** static methods ****************
    # ************************************************
    
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
        html_raw = NhRequest.get2soup( url )
        info_raw = html_raw.find( "div", id = "info" )
        
        # get author, title, other infos from jp title
        title_raw = info_raw.find( "h2", class_ = "title" )
        author = title_raw.find( "span", class_ = "before" ).text
        title = title_raw.find( "span", class_ = "pretty" ).text
        parody_translate_info = title_raw.find( "span", class_ = "after" ).text
        
        # find pages from tags
        pages = -1
        tags = info_raw.find( "section", id = "tags" ).find_all( "div" )
        
        for tag in tags :
            if "Pages" in tag.contents[0] :
                pages = tag.span.text
                break
        
        # get num of favorite from button
        favorites = info_raw.find( "div", class_ = "buttons" ).a.span.span.text[1 :-1]
        
        # get image links from thumb images' link
        images = []
        thumbs_raw = html_raw.find( "div", class_ = "thumbs" ).find_all( "div" )
        
        for thumb in thumbs_raw :
            thumb_link = thumb.a.img.get( "data-src" )
            images.append( thumb_link.replace( "t.", "." ).replace( "//.", "//i." ) )
        
        return [[author, title, parody_translate_info], pages, favorites, images]


# ************************************************
# ************** class test section **************
# ************************************************

if __name__ == '__main__' :
    res = NhGallery.get_gallery_info_by_url( "https://nhentai.net/g/339502/" )
    pass