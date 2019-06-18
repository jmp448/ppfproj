from ReqTypes import BasicCourseReq, MultiCourseReq


class Category:

    def __init__(self, cat_name, reqs, loc, min_creds, curr_creds=0, satisfied=False):
        self.cat_name = cat_name
        self.reqs = reqs
        self.loc = loc
        self.min_creds = min_creds
        self.curr_creds = curr_creds
        self.satisfied = satisfied

    def update_total(self):
        for r in self.reqs:
            if isinstance(r, BasicCourseReq):
                if r.course is not None:
                    self.curr_creds += int(r.course.creds)
            elif isinstance(r, MultiCourseReq):
                for c in r.courses:
                    self.curr_creds += int(c.creds)
        if self.curr_creds >= self.min_creds:
            self.satisfied = True
        return self.curr_creds
