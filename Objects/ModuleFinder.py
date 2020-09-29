############################
# ModuleFinder.py
############################
# Description:
# * Gets all modules used in a .py file.

import re
#from modulefinder import ModuleFinder

class ModuleFinder:
    __signatures = [re.compile('import (.+)\n'), re.compile('from (.+) import .+\n')]
    __removeAlias = re.compile('as .+')
    @classmethod
    def GetModules(cls, file):
        """
        * Import file and output all modules in file.
        """
        modules = set([])
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                for sig in ModuleFinder.__signatures:
                    match = sig.match(line)
                    if match:
                        module = match[1].split('.')[0]
                        # Remove alias:
                        module = ModuleFinder.__removeAlias.sub('', module)
                        modules.add(module)
                        break
        return modules

#class ModuleGetter:
#    __finder = ModuleFinder()
#    @classmethod
#    def GetModules(cls, file):
#        """
#        * Get all modules used in file.
#        """
#        ModuleGetter.__finder.run_script(file)
#        modules = set([])

#        return modules

