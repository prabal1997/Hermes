"""
USAGE:
This class is used as a 'node' in the graph library

BEHAVIOUR:
0.) Initially, '__data' is None, '__index' is -inf
1.) Only used as a data/index container
2.) Allows access to users via getter functions (NO setting permitted) 
"""

class node:

    #CONSTRUCTOR
    def __init__(self, data=None, index=float('-inf')):
        self.__data, self.__index = data, index;
        self._visited, self._parent, self._distance = False, None, float('inf');
        
    #GETTERS
    def data(self):
        return self.__data;
    
    def index(self):
        return self.__index;
        
    def _set_data(self, input_data):
        self.__data = input_data;
        return True;

    def _set_index(self, input_index):
        #make sure the input index is an integer, otherwise return a boolean indicating unsuccessful assignment
        if (isinstance(input_index, int)):
            self.__index = input_index;
            return True;
        else:
            print("ERROR: node cannot be assigned a non-integral index.");
            return False;
            
    #BUILT-INS
    def __str__(self):
        return "{"+str(self.__data)+" @ "+str(self.__index)+" pos}";
    def __repr__(self):
        return self.__str__();
#        return (self.__str__() + " @ " + str(id(self)));