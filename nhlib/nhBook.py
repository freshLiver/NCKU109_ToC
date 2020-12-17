from nhlib.nhGallery import *
from nhlib.nhRequest import *


class NhBook :
    
    def __init__ ( self ) :
        # @formatter:off
        self.__title        = ""
        self.__gallery_link = ""
        self.__gallery_id   = ""
        self.__total_pages  = 0
        self.__favorites    = 0
        self.__images       = list( )
        # @formatter:on
    
    
    def set_this_gallery ( self, link: str ) :
        # use url to get gallery info
        details: [str, str, str, int, int, list]
        details = NhRequest.get_detail_from_gallery( link )
        
        # @formatter:off
        # get all properties of target gallery
        self.__title        = details[0]
        self.__gallery_link = details[1]
        self.__gallery_id   = details[2]
        self.__total_pages  = details[3]
        self.__favorites    = details[4]
        self.__images       = details[5]
        # @formatter:on
    
    
    def get_total_pages ( self ) -> int :
        return self.__total_pages
    
    
    def get_link_of_page ( self, page: int ) -> str :
        return self.__images[page]
    
    
    def close_this_book ( self ) :
        # @formatter:off
        self.__title        = ""
        self.__gallery_link = ""
        self.__gallery_id   = ""
        self.__total_pages  = 0
        self.__favorites    = 0
        # @formatter:on
        self.__images.clear( )
    
    
    def book_info_to_reply ( self ) -> str :
        reply = ""
        # convert book info into reply form
        reply += """+ 標題：{0}\n""".format( self.__title )
        reply += """+ 編號：{0}\n""".format( self.__gallery_id )
        reply += """+ 連結：{0}\n""".format( self.__gallery_link )
        reply += """+ 頁數：{0}\n""".format( self.__total_pages )
        reply += """+ 愛心：{0}\n""".format( self.__favorites )
        
        return reply