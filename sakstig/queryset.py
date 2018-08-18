from . import typeinfo

class QuerySet(list):
    def __repr__(self):
        return "%s\n" % ("\n".join(repr(item) for item in self))

    def execute(self, query, global_qs = None):
        from . import ast
        from . import ast_base_types
        if not isinstance(query, ast_base_types.Expr):
            if not isinstance(query, str):
                return QuerySet([query])
            query = ast.compile(query)
        if global_qs is None:
            global_qs = self
        return query(global_qs, None)

    def map(self, fn):
        def map():
            for item in self:
                try:
                    yield fn(item)
                except Exception as e:
                    pass
        return QuerySet(map())

    def flatten(self, children_only=False, no_dict=False):
        def flatten():
            for item in self:
                if typeinfo.is_dict(item):
                    if no_dict:
                        if not children_only:
                            yield item
                    else:
                        for value in item.values():
                            yield value
                elif typeinfo.is_list(item):
                    for value in item:
                        yield value
                elif not children_only:
                    yield item
        return QuerySet(flatten())

    def __add__(self, other):
        return type(self)(list.__add__(self, other))
