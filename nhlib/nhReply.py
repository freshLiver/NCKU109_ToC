from nhlib.nhEyes import *


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
    
    
    def get_reply_message ( self, current_state: NhCommand ) -> [str or None, str] :
        
        # append with current state
        self.add_message( "\n※ 目前位於 {0}, 可以使用 {1} 查看指令".format( current_state, NhCommand.HELP ) )
        
        # concatenate all message
        reply = ""
        for msg in self.__messages[:-1] :
            reply += """{0}\n""".format( msg )
        reply += """{0}""".format( self.__messages[-1] )
        
        return [self.__link, reply]