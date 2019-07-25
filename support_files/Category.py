class Category:

    def __init__(self, cat_name, reqs, loc, min_creds, curr_creds=0, satisfied=False):
        self.cat_name = cat_name
        self.reqs = reqs
        self.loc = loc
        self.min_creds = min_creds
        self.curr_creds = curr_creds
        self.satisfied = satisfied
