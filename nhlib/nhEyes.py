class NhEyes :
    
    def __init__ ( self ) :
        self.galleries = []
        self.reading = None
        self.states = []
        self.page = 1
    
    
    # ***************************************
    # ************ add  controls ************
    # ***************************************
    
    def add_galleries ( self, galleries: list ) :
        self.galleries += galleries
    
    
    def push_state ( self, state: str ) :
        self.states.append( state )
    
    
    # ***************************************
    # ************** get status *************
    # ***************************************
    
    def get_current_state ( self ) -> str :
        # return last state in states (stack::top)
        return self.states[self.states.__len__( )]
    
    
    def get_reading_max_pages ( self ) -> int :
        return len( self.reading )
    
    
    # ***************************************
    # ************* clear status ************
    # ***************************************
    
    def reset_page ( self ) :
        self.page = 1
    
    
    def pop_state ( self ) :
        self.states.pop( )
    
    
    def clear_state ( self ) :
        self.states.clear( )
    
    
    def clear_galleries ( self ) :
        self.galleries.clear( )
    
    
    def clear_reading ( self ) :
        self.reading = None