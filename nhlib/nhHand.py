class NhHand :
    
    def __init__ ( self ) :
        self.__current_link = ""
        self.__current_page = 1
    
    
    def reset_link_and_page ( self ) :
        self.__current_link = ""
        self.__current_page = 1
    
    
    @staticmethod
    def get_popular_result ( ) -> list :
        # TODO
        pass
    
    
    @staticmethod
    def get_newest_result ( page: int ) -> list :
        # TODO
        pass
    
    
    @staticmethod
    def get_search_result ( keywords: list, page: int ) -> list :
        # TODO
        pass
    
    
    @staticmethod
    def get_result_of_page ( page: int ) -> list :
        # TODO
        pass
    
    
    @staticmethod
    def get_next_page_result ( ) -> list :
        # TODO
        pass