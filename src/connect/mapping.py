# from ranged_variable import RangedVariable
#
# class Mapping(object):
#     """"""
#     def __init__(self, source: RangedVariable, sink: RangedVariable):
#
#         if not isinstance(source, RangedVariable):
#             raise ValueError("source must be a ranged variable")
#
#         self.source = source
#
#         if not isinstance(sink, RangedVariable):
#             raise ValueError("sink must be a ranged variable")
#
#         self.sink = sink
#
#     def __str__(self):
#         str_rep = self.__class__.__name__ + ":\n"
#         str_rep += f"source = {self.source}\nsink   = {self.sink}"
#
#         return str_rep
