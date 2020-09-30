############################
# ObjectDescriber.py
############################
# Description:
# * Describes passed objects.

import inspect 
import pandas
import re

class ObjectDescriber:
    """
    * Give metadata about passed objects and classes.
    """
    __typeFuncs = {'Module' : lambda x : inspect.ismodule(x), 'Class' : lambda x : inspect.isclass(x), 
                   'Method' : lambda x : inspect.ismethod(x), 'Function' : lambda x : inspect.isfunction(x) }
    __containerTypes = (list, dict, set)
    __classPattern = re.compile("<class '(.+)'>")
    @classmethod
    def GetMembers(cls, objects):
        """
        * Return list detailing all members of object.
        """
        members = { 'Type' : [], 'Members' : [] }
        types = set([])
        if not isinstance(objects, ObjectDescriber.__containerTypes):
            objects = [objects]
        for obj in objects:
            if type(obj) not in types:
                types.add(type(obj))
            else:
                continue
            members['Type'].append(str(type(obj)))
            # Attempt to get members if supported:
            try:
                membs = inspect.getmembers(obj)
                if not inspect.isclass(obj):
                    members['Members'].append('')
                else:
                    members['Members'].append('{%s}' % ','.join([mem[0] for mem in membs]))
            except:
                members['Members'].append('')
            
        return members

    @classmethod
    def GetDocumentation(cls, objects):
        """
        * Return dictionary containing documentation
        strings for one or more objects.
        """
        docs = { 'Type' : [] ,'Documentation' : [] }
        types = set([])
        if not isinstance(objects, ObjectDescriber.__containerTypes):
            objects = [objects]
        for obj in objects:
            if not type(obj) in types:
                types.add(type(obj))
            else:
                continue
            docs['Type'].append(str(type(obj)))
            docs['Documentation'].append(inspect.getdoc(obj))
        return docs

    @classmethod
    def GetModuleInfo(cls, objects):
        """
        * Return dataframe with documentation
        strings for one or more objects.
        """
        mods = { 'Type' : [], 'Module' : [] }
        types = set([])
        if not isinstance(objects, ObjectDescriber.__containerTypes):
            objects = [objects]
        for obj in objects:
            if not type(obj) in types:
                types.add(type(obj))
            else:
                continue
            mods['Type'].append(str(type(obj)))
            mods['Module'].append(inspect.getmodule(obj))
        return mods

    @classmethod
    def GetKeyAttributes(cls, objects):
        """
        * Generate dataframe detailing all aspects
        of one or more objects.
        """
        types = set([])
        if not isinstance(objects, ObjectDescriber.__containerTypes):
            objects = [objects]
        toTest = []
        for obj in objects:
            if type(obj) not in types:
                types.add(type(obj))
                toTest.append(obj)
        funcs = [getattr(cls, f) for f in dir(cls) if not f.startswith('_') and not f == 'GetKeyAttributes']
        keyAttrs = { 'Type' : [] }
        for tp in types:
            match = ObjectDescriber.__classPattern.search(str(tp))
            keyAttrs['Type'].append(match[0])
        for f in funcs:
            result = f(toTest)
            keyAttrs.update({key : result[key] for key in result if key != 'Type'})
        return DataFrame(keyAttrs).set_index('Type')