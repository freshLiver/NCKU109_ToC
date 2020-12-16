from requests import get
from bs4 import BeautifulSoup
import typing

from nhlib.nhBook import *
from nhlib.nhGallery import *


class NhRequest :
    # CONSTANTS for HTTP requests
    __HOME = "https://nhentai.net"
    
    __HEADERS = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/75.0.3770.142 '
                       'Safari/537.36'
    }
    
    # ILLEGAL symbols for os file/dir
    __ILLEGAL_SYMBOLS = {
        '/' : '／'
        , '\\' : '＼'
        , '|' : '｜'
        , '<' : '＜'
        , '>' : '＞'
        , '?' : '？'
        , ':' : '：'
        , '"' : '＂'
        , '*' : '＊'
    }
    
    
    @classmethod
    def get_popular_galleries ( cls ) -> [NhGallery] :
        # get home page soup
        soup = cls.__get2soup( cls.__HOME )
        
        # get popular books info from home page
        popular_container_class = "container index-container index-popular"
        popular_raw = soup.find( "div", class_ = popular_container_class ).find_all( "div", class_ = "gallery" )
        
        # parse raw populars into book info
        populars = []
        for popular in popular_raw :
            # get info
            title = popular.a.find( "div", class_ = "caption" ).text
            link = cls.__HOME + popular.a.get( "href" )
            cover = popular.a.img.get( "data-src" )
            tags = str( popular.get( "data-tags" ) ).split( " " )
            
            # add to gallery list
            populars.append( NhGallery( title, link, cover, tags ) )
        
        return populars
    
    
    @classmethod
    def get_raw_galleries_from ( cls, nh_url: str ) -> [NhGallery] :
        pass
    
    
    @classmethod
    def get_detail_from_gallery ( cls, gallery_link: str ) -> [str, str, str, int, int, list] :
        
        # needed details @formatter:off
        title       = ""
        gallery_id  = ""
        pages       = 0
        favorites   = 0
        images      = list( )
        # @formatter:on
        
        # visit and get target gallery raw html
        soup = cls.__get2soup( gallery_link )
        info_raw = soup.find( "div", id = "info" )
        
        # get title and convert to legal title
        title = cls.__legalize_string( info_raw.find( "h2", class_ = "title" ) )
        
        # get gallery id, num of favorite of this gallery
        gallery_id = info_raw.find( "h3", id = "gallery_id" ).text
        favorites = info_raw.find( "div", class_ = "buttons" ).a.span.span.text[1 :-1]
        
        # get total pages of this gallery
        tags = info_raw.find( "section", id = "tags" ).find_all( "div" )
        for tag in tags :
            if "Pages" in tag.contents[0] :
                pages = tag.span.text
                break
        
        # get all image links base on thumbs
        thumbs_raw = soup.find( "div", class_ = "thumbs" ).find_all( "div" )
        for thumb in thumbs_raw :
            thumb_link = thumb.a.img.get( "data-src" )
            images.append( thumb_link.replace( "t.", "." ).replace( "//.", "//i." ) )
        
        # return gallery details
        return [title, gallery_link, gallery_id, pages, favorites, images]
    
    
    # **********************************************************
    # ********************* private methods ********************
    # **********************************************************
    
    @classmethod
    def __get2soup ( cls, url: str ) -> BeautifulSoup :
        raw = get( url, headers = cls.__HEADERS ).text
        soup = BeautifulSoup( raw, "html.parser" )
        return soup
    
    
    @classmethod
    def __legalize_string ( cls, title: str ) -> str :
        new_title = title
        
        # if any illegal symbol in title, replace it
        for symbol in cls.__ILLEGAL_SYMBOLS :
            if symbol in new_title :
                new_title.replace( symbol, cls.__ILLEGAL_SYMBOLS[symbol] )
        
        return new_title


if __name__ == '__main__' :
    # detail = NhRequest.get_detail_from_gallery( "https://nhentai.net/g/339808/" )
    pass