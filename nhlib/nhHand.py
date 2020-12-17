from nhlib.nhRequest import *


class NhHand :
    __last_link = ""
    __last_page = 1
    
    
    @classmethod
    def reset_link_and_page ( cls ) :
        cls.__last_link = ""
        cls.__last_page = 1
    
    
    @staticmethod
    def get_popular_result ( ) -> [NhRequest] :
        return NhRequest.get_popular_galleries( )
    
    
    @classmethod
    def get_newest_result ( cls, page: int ) -> [NhRequest] :
        # newest url form : HOME/?page=${page}
        newest_url = """{0}/?page={1}""".format( NhRequest.get_nh_home( ), page )
        
        # remember last command is newest and at this page
        cls.__remember_last_state( newest_url, page )
        
        # get_this_page_galleries
        galleries = NhRequest.get_galleries_from( newest_url )
        return galleries
    
    
    @classmethod
    def get_search_result ( cls, keywords: list, page: int ) -> [NhRequest] :
        # concatenate all keyword
        query = keywords[0]
        for kw in keywords[1 :] :
            query += ("+" + kw)
        # query should be url encoded
        query = NhRequest.urlencode( query )
        
        # finally query form : HOME/search/?q=${query}&page=${page}
        search_url = """{0}/search/?q={1}&page={2}""".format( NhRequest.get_nh_home( ), query, page )
        
        # remember last command is search and at this page
        cls.__remember_last_state( search_url, page )
        
        # get_this_page_galleries
        galleries = NhRequest.get_galleries_from( search_url )
        return galleries
    
    
    @classmethod
    def get_result_of_this_page ( cls, page: int ) -> [NhGallery] :
        
        # check target page (should not be negative)
        if page < 0 :
            return list( )
        
        # replace last state's url with new page
        target_page_url = cls.__last_link.split( "page=" )[0] + "page={0}".format( page )
        
        # remember target page and url
        cls.__remember_last_state( target_page_url, page )
        
        return NhRequest.get_galleries_from( target_page_url )
    
    
    @classmethod
    def get_next_page_result ( cls ) -> [NhRequest] :
        
        # get next page
        next_page = cls.__last_page + 1
        
        # replace last state's url with next page
        next_page_url = cls.__last_link.split( "page=" )[0] + "page={0}".format( next_page )
        
        # remember target page and url
        cls.__remember_last_state( next_page_url, next_page )
        
        return NhRequest.get_galleries_from( next_page_url )
    
    
    # **********************************************************
    # ********************* private methods ********************
    # **********************************************************
    
    @classmethod
    def __remember_last_state ( cls, url: str, page: int ) -> None :
        cls.__last_link = url
        cls.__last_page = page


if __name__ == '__main__' :
    new = NhHand.get_newest_result( 5 )
    search = NhHand.get_search_result( ["female", "isekai"], 6 )
    goto = NhHand.get_result_of_this_page( 20 )
    goto2 = NhHand.get_result_of_this_page( 2 )
    next = NhHand.get_next_page_result( )
    pass