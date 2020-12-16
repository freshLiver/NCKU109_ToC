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
        popular_items = soup.find( "div", class_ = popular_container_class ).find_all( "div", class_ = "gallery" )
        
        # parse raw populars into book info
        populars = []
        for gallery_item in popular_items :
            # get info from this gallery item
            info: [str, str, str, list]
            info = cls.__get_info_from_gallery_item( gallery_item )
            
            # add to gallery list
            populars.append( NhGallery( info[0], info[1], info[2], info[3] ) )
        
        return populars
    
    
    @classmethod
    def get_galleries_from ( cls, nh_url: str ) -> [NhGallery] :
        
        # get soup of this nh_page
        soup = cls.__get2soup( nh_url )
        gallery_container = soup.find( "div", class_ = "container index-container" )
        
        # get all gallery items from soup
        galleries = list( )
        gallery_items = gallery_container.find_all( "div", class_ = "gallery" )
        
        # get gallery info from every gallery in gallery container
        for gallery_item in gallery_items :
            # get info from this gallery item
            info: [str, str, str, list]
            info = cls.__get_info_from_gallery_item( gallery_item )
            
            # add to gallery list
            galleries.append( NhGallery( info[0], info[1], info[2], info[3] ) )
        
        return galleries
    
    
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
    
    
    @classmethod
    def __get_info_from_gallery_item ( cls, gallery_item: BeautifulSoup ) -> [str, str, str, list] :
        
        # get info from this gallery item
        title = gallery_item.a.find( "div", class_ = "caption" ).text
        link = cls.__HOME + gallery_item.a.get( "href" )
        cover = gallery_item.a.img.get( "data-src" )
        tags = gallery_item.get( "data-tags" ).split( " " )
        
        return [title, link, cover, tags]


if __name__ == '__main__' :
    detail = NhRequest.get_detail_from_gallery( "https://nhentai.net/g/339808/" )
    populars = NhRequest.get_popular_galleries()
    result = NhRequest.get_galleries_from( "https://nhentai.net/search/?q=kedama" )
    pass