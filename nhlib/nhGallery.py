class NhGallery :
    
    def __init__ ( self, title: str, link: str, cover: str, tags: list ) :
        self.title = title
        self.link = link
        self.cover = cover
        self.tags = tags
        self.lang = NhGallery.__extract_lang_from_tags( tags )
    
    
    @staticmethod
    def __extract_lang_from_tags ( tags: list ) -> str :
        if "29963" in tags :
            return "Chinese"
        if "12227" in tags :
            return "English"
        if "6346" in tags :
            return "Japanese"
        return "Unknown Language"
    
    
    def get_reply_form ( self, index = None ) -> str :
        
        # if given index, show index in reply message
        reply = "" if index is None else "Gallery  : {0}\n".format( index )
        
        # convert gallery info into reply form
        reply += """-- Title : {0}\n""".format( self.title )
        reply += """-- Lang  : {0}\n""".format( self.lang )
        reply += """-- Link  : {0}\n""".format( self.link )
        reply += """-- Cover : {0}\n""".format( self.cover )
        reply += "---------------------------------\n\n"
        
        return reply