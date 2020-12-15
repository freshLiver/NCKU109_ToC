from nhlib.nhEyes import *
from nhlib.nhHand import *
from nhlib.nhCommand import *


class NhUser :
    __Hand = NhHand( )
    __Eyes = NhEyes( )
    
    
    @staticmethod
    def do_command ( tokens: list ) -> str :
        reply = ""
        
        current_state = NhUser.__Eyes.get_current_state( )
        # #############################################################
        # ##################### back to home page #####################
        # #############################################################
        if tokens[0] == "$home" :
            # reset status and page
            NhUser.__Eyes.clear_state( )
            NhUser.__Eyes.clear_galleries( )
            NhUser.__Eyes.clear_reading( )
            NhUser.__Hand.reset_link_and_page( )
            # push current state
            NhUser.__Eyes.push_state( tokens[0] )
            # reply available commands
            reply = "$home done, now you can do $popular, $newest, $search, $home"
        
        
        # ###############################################################
        # #################### get popular galleries ####################
        # ###############################################################
        elif tokens[0] == "$popular" :
            # only available while current state is home
            if current_state == NhCommand.HOME :
                # get popular galleries and convert to reply form
                populars = NhUser.__Hand.get_popular_result( )
                found, reply = NhEyes.galleries_to_reply_form( populars )
                
                # check if any galleries found
                if found == True :
                    # clear and add result galleries
                    NhUser.__Eyes.clear_galleries( )
                    NhUser.__Eyes.add_galleries( populars )
                    
                    # push into newest state
                    NhUser.__Eyes.push_state( NhCommand.POPULAR )
                    
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
                # get newest galleries and convert to reply form
                newest = NhUser.__Hand.get_newest_result( 0 )
                found, reply = NhEyes.galleries_to_reply_form( newest )
                
                # check if any galleries found
                if found == True :
                    # clear and add result galleries
                    NhUser.__Eyes.clear_galleries( )
                    NhUser.__Eyes.add_galleries( newest )
                    
                    # push into newest state
                    NhUser.__Eyes.push_state( NhCommand.NEWEST )
                    
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
                # use remain tokens as keywords to search
                keywords = tokens[1 :]
                # get search galleries and convert to reply form
                search_result = NhUser.__Hand.get_search_result( keywords, 0 )
                found, reply = NhEyes.galleries_to_reply_form( search_result )
                
                # check if any galleries found
                if found == True :
                    # clear and add result galleries
                    NhUser.__Eyes.clear_galleries( )
                    NhUser.__Eyes.add_galleries( search_result )
                    
                    # push into search state
                    NhUser.__Eyes.push_state( NhCommand.SEARCH )
                    
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
                # get next page galleries and convert to replay form
                next_page_result = NhUser.__Hand.get_next_page_result( )
                found, reply = NhEyes.galleries_to_reply_form( next_page_result )
                
                # check if any galleries found
                if found == True :
                    # clear and add next page's galleries
                    NhUser.__Eyes.clear_galleries( )
                    NhUser.__Eyes.add_galleries( next_page_result )
                    
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
                try :
                    # try to use tokens[1] as page, if not int -> ValueError
                    target_page = int( tokens[1] )
                    # get target page result
                    target_galleries = NhUser.__Hand.get_result_of_page( target_page )
                    found, reply = NhEyes.galleries_to_reply_form( target_galleries )
                    
                    # check if any galleries found
                    if found == True :
                        # clear and add target galleries
                        NhUser.__Eyes.clear_galleries( )
                        NhUser.__Eyes.add_galleries( target_galleries )
                        
                        reply += "$goto done, now you can do $open, $next(maybe failed), $home"
                    else :
                        reply = "$goto failed, target page not found"
                
                except ValueError :
                    reply = "$goto failed, invalid page number"
            else :
                reply = "$goto failed, you should at $search or $newest"
        
        # ##############################################################
        # ##################### open this gallery #####################
        # ##############################################################
        elif tokens[0] == "open" :
            # only available while popular, search, newest
            if current_state in [NhCommand.POPULAR, NhCommand.SEARCH, NhCommand.NEWEST] :
                # use tokens[1] to select target gallery, if not int -> ValueError
                try :
                    gallery_index = int( tokens[1] )
                    found, gallery = NhUser.__Eyes.get_gallery_by_index( gallery_index )
                    
                    # check if this index out of range
                    if found == True :
                        # get opened gallery info and convert to reply form
                        reply = NhEyes.gallery_to_reply_form( gallery, None )
                        NhUser.__Eyes.push_state( NhCommand.OPEN )
                        reply += "$open done, now you can do $watch, $close, $home"
                    
                    # gallery index out of range
                    else :
                        reply = "$open failed, gallery index out of range"
                except ValueError :
                    reply = "$open failed, invalid gallery index"
            else :
                reply = "$open failed, you should at $popular, $search, $newest"
        
        # ###############################################################
        # ####################### watch this page #######################
        # ###############################################################
        elif tokens[0] == "$watch" :
            # only available while open
            if current_state == NhCommand.OPEN :
                try :
                    # get token[1] as page number, if not int -> ValueError
                    page = int( tokens[1] )
                    
                    # try to get target page from current reading book
                    found, url = NhUser.__Eyes.get_reading_page_link( page )
                    if found == True :
                        # TODO : get page image and convert to image message
                        reply += "$watch done, now you can do $watch, $close, $home"
                    else :
                        reply = "$watch failed, page number out of range"
                
                # may be illegal page form
                except ValueError :
                    reply = "$watch failed, invalid page parameter"
            
            else :
                reply = "$watch failed, you should at $open"
        
        # ###############################################################
        # #################### close reading gallery ####################
        # ###############################################################
        elif tokens[0] == "$close" :
            # only available while open
            if current_state == NhCommand.OPEN :
                # close and clear current reading
                NhUser.__Eyes.clear_reading( )
                # pop current state (go back to last state)
                NhUser.__Eyes.pop_state( )
                
                # check if new state is popular
                if NhUser.__Eyes.get_current_state( ) == NhCommand.POPULAR :
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