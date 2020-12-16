class NhGallery :
    
    def __init__ ( self, title: str, link: str, cover: str, tags: list ) :
        self.title = title
        self.link = link
        self.cover = cover
        self.tags = tags
        self.lang = NhGallery.extract_lang_from_tags( tags )
    
    
    @staticmethod
    def extract_lang_from_tags ( tags: list ) -> str :
        if "29963" in tags :
            return "Chinese"
        if "12227" in tags :
            return "English"
        if "6346" in tags :
            return "Japanese"
        return "Unknown Language"
    
    
    def get_reply_form ( self, index = None ) -> str :
        reply = "" if index is None else "Gallery  : {0}".format( index )
        
        # convert gallery info into reply form
        reply += """
        -- Title : {0}
        -- Lang  : {1}
        -- Link  : {2}
        -- Cover : {3}
        ---------------------------------
        """.format( self.title, self.lang, self.link, self.cover )
        
        return reply