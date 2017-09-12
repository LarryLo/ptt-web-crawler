class PttArticle:

    def __init__(self, *args): 
        self.board = args[0]
        self.article_id = args[1]
        self.author = args[2]
        self.title = args[3]
        self.content = args[4]
        self.site_name = args[5]
        self.created_datetime = args[6]
        self.ip = args[7]
        self.article_url = args[8]
        self.like = args[9]
        self.dislike = args[10]
        self.arrow = args[11]

    def __str__(self):
        return "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11}".format(
                self.board, 
                self.article_id, 
                self.author,
                self.title, 
                self.content, 
                self.site_name,
                self.created_datetime,
                self.ip,
                self.article_url,
                self.like,
                self.dislike,
                self.arrow)
