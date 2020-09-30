############################
# ObjectDescriber.py
############################
# Description:
# * Describes passed objects.

import inspect 
import pandas

class ObjectDescriber:
    """
    * Give metadata about passed objects and classes.
    """
    __typeFuncs = {'Module' : lambda x : inspect.ismodule(x), 'Class' : lambda x : inspect.isclass(x), 
                   'Method' : lambda x : inspect.ismethod(x), 'Function' : lambda x : inspect.isfunction(x) }
    @classmethod
    def GetMembers(cls, objects):
        """
        * Return list detailing all members of object.
        """
        members = { 'Type' : [], 'Members' : [] }
        types = set([])
        if not hasattr(objects, '__iter__') or isinstance(objects, str):
            objects = [objects]
        for obj in objects:
            if type(obj) not in types:
                types.add(type(obj))
            else:
                continue
            membs = inspect.getmembers(obj)
            members['Type'].append(str(type(obj)))
            if not inspect.isclass(obj):
                members['Members'].append('')
            else:
                members['Members'].append('{%s}' % ','.join([mem[0] for mem in membs]))
        return members

    @classmethod
    def GetDocumentation(cls, objects):
        """
        * Return dictionary containing documentation
        strings for one or more objects.
        """
        docs = { 'Type' : [] ,'Documentation' : [] }
        types = set([])
        if hasattr(objects, '__iter__') and not isinstance(objects, str):
            objects = set(objects)
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
        if not hasattr(objects, '__iter__') or isinstance(objects, str):
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
        if not hasattr(objects, '__iter__') or isinstance(objects, str):
            objects = [objects]
        toTest = []
        for obj in objects:
            if type(obj) not in types:
                types.add(type(obj))
                toTest.append(obj)
        funcs = [getattr(cls, f) for f in dir(cls) if not f.startswith('_')]
        keyAttrs = { 'Type' : [str(tp) for tp in types] }
        for f in funcs:
            result = f(toTest)
            keyAttrs.update({key : result[key] for key in result if key != 'Type'})
        return DataFrame(keyAttrs).set_index('Type')
