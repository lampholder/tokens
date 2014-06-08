import cherrypy
import gspread

class ListMethods(object):

    @staticmethod
    def is_empty(lst):
        for item in lst:
            if item.strip():
                return False
        return True

    @staticmethod
    def nonempty_length(self):
        for x in range(len(self) -1, -1, -1):
            if self[x] is not "":
                return x +1
        return 0

    @staticmethod
    def strip(self):
        max_length = reduce(lambda x, y: x if x > y else y, map(lambda x: ListMethods.nonempty_length(x), self))
        return [x[:max_length] for x in self]

    @staticmethod
    def split(lst, condition=None):
        if condition is None:
            condition = ListMethods.is_empty

        list_of_lists = [[]]
        for row in lst:
            if condition(row):
                list_of_lists.append([])
            else:
                list_of_lists[-1].append(row)
        return list_of_lists

class TokensMethods(object):

    @staticmethod
    def parse(string):
        if string[0] is '>':
            values = string[1:].split(',')
            return {'whcode': values[0], 'tags': values[1:]}
        else:
            return string

class Root(object):
    @cherrypy.expose
    def index(self): 
        return 'Hello, world.'

class Buckets(object):

    def __init__(self, password):
        self.password = password;

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        gc = gspread.login('lampholder@gmail.com', self.password)
        spreadsheet = gc.open_by_key('14Yb7BQ5PtczaX9z7b2YIig_xFZgI7Ox8kPA_PNRhXB4')

        worksheet = [x for x in spreadsheet.worksheet('Individuals').get_all_values() if x[0] == 'thomasl']
        if len(worksheet) == 0:
            return None
        else:
            group_name = worksheet[0][1]
        
        spreadsheet_data = [ListMethods.strip(y) for y in ListMethods.split(spreadsheet.worksheet(group_name).get_all_values())]
        return [[[TokensMethods.parse(z) for z in y] for y in x] for x in spreadsheet_data]
