from nhlib.nhEyes import *
from nhlib.nhHand import *
from nhlib.nhCommand import *


class NhUser :
    Hand = NhHand( )
    Eyes = NhEyes( )
    
    
    @staticmethod
    def is_command ( msg: str ) -> [bool, list] :
        # tokenize message
        tokens = msg.split( " " )
        
        # if first token is command, return true
        if tokens[0] in NhCommand.COMMANDS :
            return [True, tokens]
        else :
            return [False, tokens]
    
    
    @staticmethod
    def galleries_to_reply_form ( galleries: list ) -> (bool, str) :
        # no gallery found
        if galleries.__len__( ) == 0 :
            return (False, "")
        else :
            # TODO convert galleries info to reply form
            return (True, "")
    
    
    @staticmethod
    def do_command ( tokens: list ) -> str :
        reply = ""
        
        current_state = NhUser.Eyes.get_current_state( )
        # #############################################################
        # ##################### back to home page #####################
        # #############################################################
        if tokens[0] == "$home" :
            # reset status and page
            NhUser.Eyes.clear_state( )
            NhUser.Eyes.clear_galleries( )
            NhUser.Eyes.clear_reading( )
            NhUser.Eyes.reset_page( )
            # push current state
            NhUser.Eyes.push_state( tokens[0] )
            # reply available commands
            reply = "$home done, now you can do $popular, $newest, $search, $home"
        
        
        # ###############################################################
        # #################### get popular galleries ####################
        # ###############################################################
        elif tokens[0] == "$popular" :
            # only available while current state is home
            if current_state == NhCommand.HOME :
                # TODO : get popular galleries and convert to reply form
                populars = []
                found, reply = NhUser.galleries_to_reply_form( populars )
                
                # check if any galleries found
                if found == True :
                    # clear and add result galleries
                    NhUser.Eyes.clear_galleries( )
                    NhUser.Eyes.add_galleries( populars )
                    
                    # push into newest state
                    NhUser.Eyes.push_state( NhCommand.POPULAR )
                    
                    reply += "$popular done, now you can do $open, $home"
                else :
                    reply = "$newest failed, newest gallery not found"
            else :
                reply = "$popular failed, you should at $home"
        
        # ##############################################################
        # #################### get newest galleries ####################
        # ##############################################################
        elif tokens[0] == "$newest" :
            # only available while current state is home
            if current_state == NhCommand.HOME :
                # TODO : get newest galleries and convert to reply form
                newest = []
                found, reply = NhUser.galleries_to_reply_form( newest )
                
                # check if any galleries found
                if found == True :
                    # clear and add result galleries
                    NhUser.Eyes.clear_galleries( )
                    NhUser.Eyes.add_galleries( newest )
                    
                    # push into newest state
                    NhUser.Eyes.push_state( NhCommand.NEWEST )
                    
                    reply += "$newest done, now you can do $open, $next(maybe failed), $home"
                else :
                    reply = "$newest failed, newest gallery not found"
            
            else :
                reply = "$newest failed, you should at $home"
        
        # ##############################################################
        # ###################### search galleries ######################
        # ##############################################################
        elif tokens[0] == "$search" :
            # only available while current state is home
            if current_state == NhCommand.HOME :
                # TODO : get search galleries and convert to reply form
                search_result = []
                found, reply = NhUser.galleries_to_reply_form( search_result )
                
                # check if any galleries found
                if found == True :
                    # clear and add result galleries
                    NhUser.Eyes.clear_galleries( )
                    NhUser.Eyes.add_galleries( search_result )
                    
                    # push into search state
                    NhUser.Eyes.push_state( NhCommand.SEARCH )
                    
                    reply += "$search done, now you can do $open, $next(maybe failed), $home"
                else :
                    reply = "$search failed, search result not found"
            else :
                reply = "$search failed, you should at $home"
        
        # ##############################################################
        # ####################### goto next page #######################
        # ##############################################################
        elif tokens[0] == "$next" :
            # only available while search or newest
            if current_state in [NhCommand.SEARCH, NhCommand.NEWEST] :
                # TODO : get next page galleries and convert to replay form
                next_page_result = []
                found, reply = NhUser.galleries_to_reply_form( next_page_result )
                
                # check if any galleries found
                if found == True :
                    # clear and add next page's galleries
                    NhUser.Eyes.clear_galleries( )
                    NhUser.Eyes.add_galleries( next_page_result )
                    
                    reply += "$next done, now you can do $open, $next(maybe failed), $home"
                else :
                    reply = "$next failed, next page not found"
            else :
                reply = "$next failed, you should at $search or $newest"
        
        # #############################################################
        # ######################## goto page N ########################
        # #############################################################
        elif tokens[0] == "$goto" :
            # only available while search or newest
            if current_state in [NhCommand.SEARCH, NhCommand.NEWEST] :
                # TODO get target page result
                target_galleries = []
                found, reply = NhUser.galleries_to_reply_form( target_galleries )
                
                # check if any galleries found
                if found == True :
                    # clear and add target galleries
                    NhUser.Eyes.clear_galleries( )
                    NhUser.Eyes.add_galleries( target_galleries )
                    
                    reply += "$goto done, now you can do $open, $next(maybe failed), $home"
                else :
                    reply = "$goto failed, target page not found"
            else :
                reply = "$goto failed, you should at $search or $newest"
        
        # ##############################################################
        # ##################### open this gallery #####################
        # ##############################################################
        elif tokens[0] == "open" :
            # only available while popular, search, newest
            if current_state in [NhCommand.POPULAR, NhCommand.SEARCH, NhCommand.NEWEST] :
                # TODO get opened gallery info and convert to reply form
                
                NhUser.Eyes.push_state( NhCommand.OPEN )
                reply = "$open done, now you can do $watch, $close, $home"
            else :
                reply = "$open failed, you should at $popular, $search, $newest"
        
        # ###############################################################
        # ####################### watch this page #######################
        # ###############################################################
        elif tokens[0] == "$watch" :
            # only available while open
            if current_state == NhCommand.OPEN :
                try :
                    # get token[1] as page number
                    page = int( tokens[1] )
                    
                    # check if this page out of gallery pages
                    if 0 < page <= NhUser.Eyes.get_reading_max_pages( ) :
                        # TODO : get page image and convert to image message
                        reply += "$watch done, now you can do $watch, $close, $home"
                    
                    else :
                        reply = "$watch failed, page number out of range"
                
                # may be illegal page form
                except ValueError :
                    reply = "$watch failed, illegal page parameter"
            
            else :
                reply = "$watch failed, you should at $open"
        
        # ###############################################################
        # #################### close reading gallery ####################
        # ###############################################################
        elif tokens[0] == "$close" :
            # only available while open
            if current_state == NhCommand.OPEN :
                # close and clear current reading
                NhUser.Eyes.clear_reading( )
                # pop current state (go back to last state)
                NhUser.Eyes.pop_state( )
                
                # check if new state is popular
                if NhUser.Eyes.get_current_state( ) == NhCommand.POPULAR :
                    reply = "$close done, now you can do $open, $home"
                else :
                    reply = "$close done, now you can do $open, $next(may be failed), $home"
            else :
                reply = "$close failed, you should at $open"
        
        
        # ###############################################################
        # #################### NOT BELONGS ANY STATE ####################
        # ###############################################################
        else :
            raise Exception( "This Message is Not a Command !" )
        
        # return reply message to user
        return reply