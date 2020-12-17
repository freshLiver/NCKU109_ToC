class NhReply :
    
    def __init__ ( self ) :
        self.__link = None
        self.__messages = list( )
    
    
    def add_message ( self, msg: str ) :
        self.__messages.append( msg )
    
    
    def add_reply_messages ( self, msgs: list ) :
        self.__messages += msgs
    
    
    def set_url ( self, url: str ) :
        self.__link = url
    
    
    def reset ( self ) -> None :
        self.__link = None
        self.__messages.clear( )
    
    
    def get_reply_message ( self ) -> [str or None, str] :
        reply = ""
        # concatenate all message
        for msg in self.__messages :
            reply += """{0}\n""".format( msg )
        
        return [self.__link, reply]