class NhBook :
    
    def __init__ ( self ) :
        self.__title = ""
        self.__total_pages = 0
        self.__pages = list( )
    
    
    def set_new_book ( self, gallery ) :
        # TODO
        pass
    
    
    def get_total_pages ( self ) -> int :
        return self.__total_pages
    
    
    def get_link_of_page ( self, page: int ) -> str :
        return self.__pages[page]
    
    
    def reset ( self ) :
        self.__title = ""
        self.__total_pages = 0
        self.__pages = list( )