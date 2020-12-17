from nhlib.nhEyes import *
from nhlib.nhHand import *
from nhlib.nhCommand import *
from nhlib.nhGallery import *
from nhlib.nhReply import *


class NhUser :
    __Hand = NhHand( )
    __Eyes = NhEyes( )
    __Reply = NhReply( )
    
    
    @classmethod
    def do_command ( cls, tokens: list ) -> NhReply :
        cls.__Reply.reset( )
        current_state = cls.__Eyes.get_current_state( )
        
        # #############################################################
        # ##################### back to home page #####################
        # #############################################################
        if tokens[0] == NhCommand.HOME :
            # reset status and page
            cls.__Eyes.clear_state( )
            cls.__Eyes.clear_galleries( )
            cls.__Eyes.clear_reading( )
            cls.__Hand.reset_link_and_page( )
            
            # reply available commands
            cls.__Reply.add_message( "$home done, now you can do $popular, $newest, $search, $home" )
        
        
        
        # ###############################################################
        # #################### get popular galleries ####################
        # ###############################################################
        elif tokens[0] == NhCommand.POPULAR :
            # only available while current state is home
            if current_state == NhCommand.HOME :
                # get popular galleries and convert to reply form
                populars = cls.__Hand.get_popular_result( )
                found, reply = NhEyes.galleries_to_reply_form( populars )
                
                # check if any galleries found
                if found == True :
                    # clear and add result galleries
                    cls.__Eyes.clear_galleries( )
                    cls.__Eyes.add_galleries( populars )
                    
                    # push into newest state
                    cls.__Eyes.push_state( NhCommand.POPULAR )
                    
                    cls.__Reply.add_message( reply )
                    cls.__Reply.add_message( "$popular done, now you can do $open, $home" )
                else :
                    cls.__Reply.add_message( "$newest failed, newest gallery not found" )
            else :
                cls.__Reply.add_message( "$popular failed, you should at $home" )
        
        
        
        # ##############################################################
        # #################### get newest galleries ####################
        # ##############################################################
        elif tokens[0] == NhCommand.NEWEST :
            # only available while current state is home
            if current_state == NhCommand.HOME :
                # get newest galleries and convert to reply form
                newest = cls.__Hand.get_newest_result( 0 )
                found, reply = NhEyes.galleries_to_reply_form( newest )
                
                # check if any galleries found
                if found == True :
                    # clear and add result galleries
                    cls.__Eyes.clear_galleries( )
                    cls.__Eyes.add_galleries( newest )
                    
                    # push into newest state
                    cls.__Eyes.push_state( NhCommand.NEWEST )
                    
                    cls.__Reply.add_message( reply )
                    cls.__Reply.add_message( "$newest done, now you can do $open, $next(maybe failed), $home" )
                
                else :
                    cls.__Reply.add_message( "$newest failed, newest gallery not found" )
            
            else :
                cls.__Reply.add_message( "$newest failed, you should at $home" )
        
        
        
        # ##############################################################
        # ###################### search galleries ######################
        # ##############################################################
        elif tokens[0] == NhCommand.SEARCH :
            # only available while current state is home
            if current_state == NhCommand.HOME :
                # use remain tokens as keywords to search
                keywords = tokens[1 :]
                
                # check if search without keywords
                if keywords != [] :
                    # get search galleries and convert to reply form
                    search_result = cls.__Hand.get_search_result( keywords, 1 )
                    found, reply = NhEyes.galleries_to_reply_form( search_result )
                    
                    # check if any galleries found
                    if found == True :
                        # clear and add result galleries
                        cls.__Eyes.clear_galleries( )
                        cls.__Eyes.add_galleries( search_result )
                        
                        # push into search state
                        cls.__Eyes.push_state( NhCommand.SEARCH )
                        
                        cls.__Reply.add_message( reply )
                        cls.__Reply.add_message( "$search done, now you can do $open, $next(maybe failed), $home" )
                    
                    else :
                        cls.__Reply.add_message( "$search failed, search result not found" )
                else :
                    cls.__Reply.add_message( "$search failed, you should not do search without keywords" )
            else :
                cls.__Reply.add_message( "$search failed, you should at $home" )
        
        
        
        # ##############################################################
        # ####################### goto next page #######################
        # ##############################################################
        elif tokens[0] == NhCommand.NEXT :
            # only available while search or newest
            if current_state in [NhCommand.SEARCH, NhCommand.NEWEST] :
                # get next page galleries and convert to replay form
                next_page_result = cls.__Hand.get_next_page_result( )
                found, reply = NhEyes.galleries_to_reply_form( next_page_result )
                
                # check if any galleries found
                if found == True :
                    # clear and add next page's galleries
                    cls.__Eyes.clear_galleries( )
                    cls.__Eyes.add_galleries( next_page_result )
                    
                    cls.__Reply.add_message( reply )
                    cls.__Reply.add_message( "$next done, now you can do $open, $next(maybe failed), $home" )
                else :
                    cls.__Reply.add_message( "$next failed, next page not found" )
            else :
                cls.__Reply.add_message( "$next failed, you should at $search or $newest" )
        
        
        
        # #############################################################
        # ######################## goto page N ########################
        # #############################################################
        elif tokens[0] == NhCommand.GOTO :
            # only available while search or newest
            if current_state in [NhCommand.SEARCH, NhCommand.NEWEST] :
                try :
                    # try to use tokens[1] as page, if not int -> ValueError
                    target_page = int( tokens[1] )
                    # get target page result
                    target_galleries = cls.__Hand.get_result_of_this_page( target_page )
                    found, reply = NhEyes.galleries_to_reply_form( target_galleries )
                    
                    # check if any galleries found
                    if found == True :
                        # clear and add target galleries
                        cls.__Eyes.clear_galleries( )
                        cls.__Eyes.add_galleries( target_galleries )
                        cls.__Reply.add_message( reply )
                        cls.__Reply.add_message( "$goto done, now you can do $open, $next(maybe failed), $home" )
                    
                    else :
                        cls.__Reply.add_message( "$goto failed, target page not found" )
                except ValueError :
                    cls.__Reply.add_message( "$goto failed, invalid page number" )
            else :
                cls.__Reply.add_message( "$goto failed, you should at $search or $newest" )
        
        
        
        # ##############################################################
        # ##################### open this gallery #####################
        # ##############################################################
        elif tokens[0] == NhCommand.OPEN :
            # only available while popular, search, newest
            if current_state in [NhCommand.POPULAR, NhCommand.SEARCH, NhCommand.NEWEST] :
                # use tokens[1] to select target gallery, if not int -> ValueError
                try :
                    gallery_index = int( tokens[1] )
                    gallery: NhGallery
                    found, gallery = cls.__Eyes.get_gallery_by_index( gallery_index )
                    
                    # check if this index out of range
                    if found == True :
                        # get opened gallery info and convert to reply form
                        reply = gallery.get_reply_form( None )
                        # open gallery and set it new book
                        cls.__Eyes.check_this_gallery( gallery_index )
                        cls.__Eyes.push_state( NhCommand.OPEN )
                        
                        cls.__Reply.add_message( reply )
                        cls.__Reply.add_message( "$open done, now you can do $watch, $close, $home" )
                    
                    # gallery index out of range
                    else :
                        cls.__Reply.add_message( "$open failed, gallery index out of range" )
                except ValueError :
                    cls.__Reply.add_message( "$open failed, invalid gallery index" )
            else :
                cls.__Reply.add_message( "$open failed, you should at $popular, $search, $newest" )
        
        
        
        # ###############################################################
        # ####################### watch this page #######################
        # ###############################################################
        elif tokens[0] == NhCommand.WATCH :
            # only available while open
            if current_state == NhCommand.OPEN :
                try :
                    # get token[1] as page number(start from 0), if not int -> ValueError
                    page = int( tokens[1] )
                    
                    # try to get target page from current reading book
                    found, url = cls.__Eyes.get_reading_page_link( page )
                    if found == True :
                        cls.__Reply.set_url( url )
                        cls.__Reply.add_message( "$watch done, now you can do $watch, $close, $home" )
                    
                    else :
                        cls.__Reply.add_message( "$watch failed, page number out of range" )
                except ValueError :
                    cls.__Reply.add_message( "$watch failed, invalid page parameter" )
            else :
                cls.__Reply.add_message( "$watch failed, you should at $open" )
        
        
        
        # ###############################################################
        # #################### close reading gallery ####################
        # ###############################################################
        elif tokens[0] == NhCommand.CLOSE :
            # only available while open
            if current_state == NhCommand.OPEN :
                # close and clear current reading
                cls.__Eyes.clear_reading( )
                # pop current state (go back to last state)
                cls.__Eyes.pop_state( )
                
                # check if new state is popular
                if cls.__Eyes.get_current_state( ) == NhCommand.POPULAR :
                    cls.__Reply.add_message( "$close done, now you can do $open, $home" )
                else :
                    cls.__Reply.add_message( "$close done, now you can do $open, $next(may be failed), $home" )
            else :
                cls.__Reply.add_message( "$close failed, you should at $open" )
        
        
        # ###############################################################
        # #################### NOT BELONGS ANY STATE ####################
        # ###############################################################
        else :
            raise Exception( "This Message is Not a Command !" )
        
        # return reply message to user
        return cls.__Reply.get_reply_message( )


if __name__ == '__main__' :
    msg = NhUser.do_command( ["$home"] )
    msg = NhUser.do_command( ["$popular"] )
    msg = NhUser.do_command( ["$home"] )
    msg = NhUser.do_command( ["$search", "ichiri", "isekai"] )
    msg = NhUser.do_command( ["$open", "0"] )
    msg = NhUser.do_command( ["$watch", "0"] )
    pass