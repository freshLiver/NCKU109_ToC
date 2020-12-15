class NhCommand :
    COMMANDS = ["$home", "$popular", "$search", "$newest",
                "$goto", "$next", "$open", "$watch", "$close"]
    
    # @formatter:off
    HOME    = "$home"
    POPULAR = "$popular"
    SEARCH  = "$search"
    NEWEST  = "$newest"
    GOTO    = "$goto"
    NEXT    = "$next"
    OPEN    = "$open"
    WATCH   = "$watch"
    CLOSE   = "$close"
    # @formatter:on
    
    @staticmethod
    def is_command ( msg: str ) -> [bool, list] :
        # tokenize message
        tokens = msg.split( " " )
        
        # if first token is command, return true
        if tokens[0] in NhCommand.COMMANDS :
            return [True, tokens]
        else :
            return [False, tokens]