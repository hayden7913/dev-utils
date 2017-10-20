import os
import re
import sys


# put your find and replace logic here
# the script feeds each line of each file into this function so do your find and replace on a line by line basis
def replaceFunction(line, lineNumber, filePath):  
    match = re.search(r'(?<==> { return).*?(?=;)', line)
    
    if match:
        matchText = match.group(0);
        print 'Changed line %s @ %s' % (lineNumber, filePath)
    else:
        return line    
    # you must return your replacement string here
    return re.sub(r'=> { return .*?; }', '=>%s' % matchText, line) 


##################################################################################        
def getFileNameFromPath(path):
  pathArray = path.split('/')
  return pathArray[len(pathArray) - 1]
  
def processFilesInDir(path, callback): 
    for dirItem in os.listdir(path): #iterate through files and folders in given directory
        dirItemPath = os.path.join(path, dirItem)
        if os.path.isdir(dirItemPath):
            processFilesInDir(dirItemPath, callback)
        else: 
            callback(dirItemPath)
            
def rewriteFile(lineEditorFunction): 
    def rewriteFileWrapper(filePath):
        # Read in the file
        with open(filePath, 'r') as file:
            filedata = file.readlines()
          
        # create a new file based on provided replace function  
        new_filedata = [];
        for index, line in enumerate(filedata):
            new_filedata.append(lineEditorFunction(line, index + 1, getFileNameFromPath(filePath)))    
            
        # Overwrite the file with updated text array
        with open(filePath, 'w') as file:
            for line in new_filedata:
                file.write(line)
            file.close
            
    return rewriteFileWrapper

def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]   
    else:
        print('please provide a path to a file or directory')
        return    
        # path='/home/hayden/Dropbox/tf/PomTracker-Capstone/client/src/containers/Timer.js'
    hasProjectBeenSaved = raw_input('Have you commited to git (y/n)');
    
    findReplaceAndRewriteFile = rewriteFile(replaceFunction);
    
    # if the path does not end in a word preceded by a period, assume that the path leads to a directory rather than a file
    doesPathLeadToDirectory = not bool(re.search(r'\.(?=\w+$)', path))


    if (hasProjectBeenSaved == 'y') & doesPathLeadToDirectory:
        processFilesInDir(path, findReplaceAndRewriteFile) 
        print('***search complete***') 
    elif hasProjectBeenSaved == 'y':
        rewriteFile(path)
        print('***search complete***') 
    else:    
        print('***good bye***')

main()
