class NhEyes :
    
    def __init__ ( self ) :
        self.__galleries = []
        self.__reading = None
        self.__states = []
    
    
    # ***************************************
    # ********** gallery conversion *********
    # ***************************************
    @staticmethod
    def gallery_to_reply_form ( gallery: list, index = None ) -> str :
        # reply with index only while needed
        reply = ""
        if index is not None :
            reply += "Gallery ID : {0}".format( index )
        
        # append basic gallery infos
        # TODO : convert gallery infos into reply form
        reply += """
        -- Title : {0}
        -- Lang  : {1}
        -- Link  : {2}
        -- Thumb : {3}
        ------------------------------
        """.format( gallery[0], gallery[1], gallery[2], gallery[3] )
        
        # return reply form of this gallery
        return reply
    
    
    @staticmethod
    def galleries_to_reply_form ( galleries: list ) -> (bool, str) :
        # no gallery found
        if galleries.__len__( ) == 0 :
            return (False, "")
        
        # not empty result, convert galleries info to reply form
        reply = ""
        
        # append each gallery info in galleries to reply
        for index, gallery in enumerate( galleries ) :
            reply += NhEyes.gallery_to_reply_form( gallery, index )
        
        # return all galleries' info as reply message
        return (True, reply)
    
    
    # ***************************************
    # ************ add  controls ************
    # ***************************************
    
    def add_galleries ( self, galleries: list ) :
        self.__galleries += galleries
    
    
    def push_state ( self, state: str ) :
        self.__states.append( state )
    
    
    # ***************************************
    # ************** get status *************
    # ***************************************
    
    def get_current_state ( self ) -> str :
        # return last state in states (stack::top)
        return self.__states[self.__states.__len__( )]
    
    
    def get_gallery_by_index ( self, index: int ) -> (bool, list) :
        # check if target gallery index out of range
        if 0 <= index < len( self.__galleries ) :
            return (True, self.__galleries[index])
        # if gallery index out of range, return false and empty list
        else :
            return (False, list( ))
    
    
    def get_reading_page_link ( self, page: int ) -> (bool, str) :
        # check if target page over current reading book's total pages
        if 0 < page <= len( self.__reading ) :
            # TODO : get target page's image link
            link = self.__reading.pages[page]
            return (True, link)
        # page out of range
        else :
            return (False, "Target Page Out Of Range")
    
    
    # ***************************************
    # ************* clear status ************
    # ***************************************
    
    def pop_state ( self ) :
        self.__states.pop( )
    
    
    def clear_state ( self ) :
        self.__states.clear( )
    
    
    def clear_galleries ( self ) :
        self.__galleries.clear( )
    
    
    def clear_reading ( self ) :
        self.__reading = None