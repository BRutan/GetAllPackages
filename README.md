** GetAllPackages **
----------------------------------
* Determine all the modules used in one or more .py files, located in one or more folders.

** Usage **
----------------------------------
GetAllPackages.py [-h] [--folders + [+ ...]] [--files +] [--recursive]
                         [--aggregate]
                         outfolder
positional arguments:
  outfolder            Output folder for report. Must exist.

optional arguments:
  -h, --help           show this help message and exit
  --folders + [+ ...]  One or more folder to recursively check all .py files.
  --files +            One or more .py files to check.
  --recursive          Put if want to recursively search sub folders in
                       folders.
  --aggregate          Include if just want all unique libraries listed, not
                       grouped by file where they occur.
