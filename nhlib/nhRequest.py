from bs4 import BeautifulSoup as BSoup
from bs4 import element
from requests import get

from nhlib.nhGallery import *
from nhlib.nhGlobal import *


class NhRequest :
    
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
        
        populars = []
        
        # parse raw populars into book info
        popular: element.Tag
        for popular in popular_galleries :
            
            title = popular.a.find( "div", class_ = "caption" ).text
            link = NhGlobal.home + popular.a.get( "href" )
            thumb = popular.a.img.get( "data-src" )
            
            # get lang from data tag
            tags = str( popular.get( "data-tags" ) ).split( " " )
            
            populars.append( NhGallery( title, link, thumb, tags ) )
        
        return populars
    
if __name__ == '__main__':
    pass