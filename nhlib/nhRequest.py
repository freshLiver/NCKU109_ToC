from bs4 import BeautifulSoup as BSoup
from requests import get

from nhlib.nhGallery import *
from nhlib.nhGlobal import *


class NhRequest :
    
    def __init__ ( self ) :
        pass
    
    
    @staticmethod
    def get2soup ( url: str ) -> BSoup :
        raw = get( url, headers = NhGlobal.headers ).text
        soup = BSoup( raw, "html.parser" )
        return soup
    
    
    @staticmethod
    def get_populars ( ) -> list :
        # crawl home page
        soup = NhRequest.get2soup( NhGlobal.home )
        
        # get popular books info from home page
        popular_galleries = soup.find( "div", class_ = "container index-container index-popular"
                                       ).find_all( "div", class_ = "gallery" )
        
        # parse raw populars into book info
        populars = []
        for popular in popular_galleries :
            # get infomations
            title = popular.a.find( "div", class_ = "caption" ).text
            link = NhGlobal.home + popular.a.get( "href" )
            cover = popular.a.img.get( "data-src" )
            tags = str( popular.get( "data-tags" ) ).split( " " )
            
            # add to gallery list
            populars.append( NhGallery( title, link, cover, tags ) )
        
        # return result (popular galleries from home page)
        return populars


# ************************************************
# ************** class test section **************
# ************************************************

if __name__ == '__main__' :
    res = NhRequest.get_populars( )
    pass