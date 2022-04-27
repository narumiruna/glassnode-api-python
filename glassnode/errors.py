class Forbidden(Exception):
    pass


class ResolutionForbidden(Forbidden):
    """this resolution is forbidden for endpoint"""
    pass
