class PttComment:

    def __init__(self, *args): 
        self.user_id = args[0]
        self.push = args[1]
        self.content = args[2]
        self.datetime = args[3]

    def __str__(self):
        return "{0} {1} {2} {3}".format(
                self.user_id, 
                self.push, 
                self.content,
                self.datetime) 
