from nhlib.nhRequest import *


class NhHand :
    
    def __init__ ( self ) :
        self.__current_link = ""
        self.__current_page = 1
    
    
    def reset_link_and_page ( self ) :
        self.__current_link = ""
        self.__current_page = 1
    
    
    @staticmethod
    def get_popular_result ( ) -> [NhRequest] :
        return NhRequest.get_popular_galleries( )
    
    
    @classmethod
    def get_newest_result ( cls, page: int ) -> [NhRequest] :
        # newest url form : HOME/?page=${page}
        newest_url = """{0}/?page={1}""".format( NhRequest.get_nh_home( ), page )
        
        # get_this_page_galleries
        galleries = NhRequest.get_galleries_from( newest_url )
        return galleries
    
    
    @staticmethod
    def get_search_result ( keywords: list, page: int ) -> [NhRequest] :
        # concatenate all keyword
        query = keywords[0]
        for kw in keywords[1 :] :
            query += ("+" + kw)
        # query should be url encoded
        query = NhRequest.urlencode( query )
        
        # finally query form : HOME/search/?q=${query}&page=${page}
        search_url = """{0}/search/?q={1}&page={2}""".format( NhRequest.get_nh_home( ), query, page )
        
        # get_this_page_galleries
        galleries = NhRequest.get_galleries_from( search_url )
        return galleries
    
    
    @staticmethod
    def get_result_of_page ( page: int ) -> [NhRequest] :
        # TODO
        pass
    
    
    @staticmethod
    def get_next_page_result ( ) -> [NhRequest] :
        # TODO
        pass


if __name__ == '__main__' :
    # keywords = ["artist:ichiri", "isekai"]
    # page = 2
    # res = NhHand.get_search_result( keywords, page )
    res = NhHand.get_newest_result( 5 )
    pass