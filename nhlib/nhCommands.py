class NhCommands :
    # @formatter:off
    HOME    = "$home"
    POPULAR = "$popu"
    SEARCH  = "$sear"
    NEWEST  = "$newe"
    GOTO    = "$goto"
    NEXT    = "$next"
    CHECK   = "$chec"
    WATCH   = "$watc"
    BACK    = "$back"
    ILLEGAL   = "NOT COMMAND"
    # @formatter:on
    
    @staticmethod
    def get_command_type ( text: str ) -> NhCommands.NhCommands :
        # check if this text has command prefix '$'
        if text[0] != '$' :
            return NhCommands.ILLEGAL
        else :
            # if text is command, check type (base on )
            cmd = text[0 :4]
            if cmd == NhCommands.HOME :
                return NhCommands.HOME
            
            if cmd == NhCommands.POPULAR :
                return NhCommands.POPULAR
            
            if cmd == NhCommands.SEARCH :
                return NhCommands.SEARCH
            
            if cmd == NhCommands.NEWEST :
                return NhCommands.NEWEST
            
            if cmd == NhCommands.GOTO :
                return NhCommands.GOTO
            
            if cmd == NhCommands.NEXT :
                return NhCommands.NEXT
            
            if cmd == NhCommands.CHECK :
                return NhCommands.CHECK

            if cmd == NhCommands.WATCH:
                return NhCommands.WATCH

            if cmd == NhCommands.BACK :
                return NhCommands.BACK

        return NhCommands.ILLEGAL