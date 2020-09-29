############################
# GetAllPackages.py
############################
# Description:
# * CLI used to aggregate all packages used 
# in collection of .py files.

from argparse import ArgumentParser
from Objects.ModuleFinder import _ModuleFinder, ModuleGetter
import os

def Main():
    outfolder, folders, files, aggregate, recursive, skipstd = GetArgs()
    outfolder, files, folders = CheckArgs(outfolder, folders, files)
    fileModules = CheckAllFiles(files, aggregate)
    folderModules = CheckAllFolders(folders, aggregate, recursive)
    outfile = GenerateReport(outfolder, fileModules, folderModules, aggregate)
    PrintEnd(outfile)

def GetArgs():
    parser = ArgumentParser(description='Get all packages used in .py files in folder or specifed.')
    parser.add_argument('outfolder', type = str, help = 'Output folder for report. Must exist.')
    parser.add_argument('--folders', metavar='+', type=str, nargs='+', help='One or more folder to recursively check all .py files.')
    parser.add_argument('--files', metavar='+', type=str, help='One or more .py files to check.')
    parser.add_argument('--recursive', action='store_true', help='Put if want to recursively search sub folders in folders.')
    parser.add_argument('--aggregate', action='store_true', help='Include if just want all unique libraries listed, not grouped by file where they occur.')
    parser.add_argument('--skipstandardlib', action='store_true', help="Include if don't want to include standard modules in output.")
    result = parser.parse_args()
    
    return result.outfolder, result.folders, result.files, result.aggregate, result.recursive, result.skipstandardlib

def CheckArgs(outfolder, folders, files):
    """
    * Ensure all folders and files exist and outfolder is valid.
    """
    errs = []
    if outfolder and not os.path.exists(outfolder):
        errs.append('(outfolder) %s folder does not exist.' % outfolder)
    if files:
        if isinstance(files, str):
            files = [files]
        missing = [f for f in files if not os.path.isfile(f)]
        invalid = [f for f in files if not f.endswith('.py')]
        if missing:
            errs.append('(files) The following files are missing: %s' % '\n'.join(missing))
        if invalid:
            errs.append('(files) The following files are not .py: %s' % '\n'.join(invalid))
    else:
        files = []
    if folders:
        if isinstance(folders, str):
            folders = [folders]
        missing = [f for f in folders if not os.path.isdir(f)]
        if missing:
            errs.append('(folders) The following folders are missing: %s' % '\n'.join(missing))
    else:
        folders = []
    if errs:
        raise ValueError('The following command line args occurred: %s' % '\n'.join(errs))
    
    return outfolder, files, folders

def CheckAllFiles(files, aggregate):
    """
    * Aggregate all imported packages in files.
    """
    fileModules = {} if not aggregate else set([])
    for file in files:
        modules = ModuleFinder.GetModules(file)
        if not aggregate:
            fileModules[file] = modules
        else:
            fileModules.update(modules)
    return fileModules

def CheckAllFolders(folders, aggregate, recursive):
    """
    * Aggregate all packages listed in all files in 
    all passed folders.
    """
    folderModules = {} if not aggregate else set([])
    for folder in folders:
        paths = ['%s\\%s' % (folder, f) for f in os.listdir(folder)]
        files = [f for f in paths if os.path.isfile(f) and f.endswith('.py')]
        fileModules = CheckAllFiles(files, aggregate)
        if not aggregate:
            for key in fileModules:
                if len(fileModules[key]) > 0:
                    folderModules[key] = fileModules[key]
        elif aggregate:
            folderModules.update(fileModules)
        if recursive:
            subFolders = [f for f in paths if os.path.isdir(f)]
            folderResults = CheckAllFolders(subFolders, aggregate, recursive)
            if not aggregate:
                for key in folderResults:
                    if len(folderResults[key]) > 0:
                        folderModules[key] = folderResults[key] 
            elif aggregate:
                folderModules.update(folderResults)

    return folderModules

def GenerateReport(outfolder, fileModules, folderModules, aggregate):
    """
    * Generate report of all required modules based upon aggregation
    method.
    """
    outfile = '%sAllPackages.txt' % outfolder
    if aggregate:
        results = set()
        results.update(fileModules)
        results.update(folderModules)
        results = sorted(results, key = str.lower)
        with open(outfile, 'w') as f:
            f.write('Module:\n')
            f.writelines([rs + '\n' for rs in results])
    else:
        results = {}
        for key in fileModules:
            results[key] = fileModules[key]
        for key in folderModules:
            results[key] = folderModules[key]
        with open(outfile, 'w') as f:
            f.write('Path:, Modules:\n')
            for key in results:
                f.write('%s, %s\n' % (key, ','.join(sorted(results[key], key = str.lower))))
    return outfile

def PrintEnd(outfile):
    """
    * Express end of program.
    """
    print("Results located at %s." % outfile)

if __name__ == '__main__':
    Main()
