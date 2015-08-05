import zipfile
import cPickle as pickle

from tools.myTools import *


def getDictFiles(dictName, sort = False, reverse = False):

    retFiles = []
    originalDocuentsNames = {}
    for i in os.listdir(dictName):
        #state = os.stat(os.path.join(dictName, i))
        path = os.path.join(dictName, i)
        #originalDocuentsNames[path] = state.st_ctime
        try:
            originalDocuentsNames[path] = int(i[:8])
        except:
            print 'transform to int occur an error!'
        retFiles.append(path)
    #sort = sorted(originalDocuentsNames.items(), key=lambda originalDocuentsNames:originalDocuentsNames[1], reverse=True)
    if not reverse:
        sort = sorted(originalDocuentsNames.items(), key=lambda originalDocuentsNames:originalDocuentsNames[1])
    else:
        sort = sorted(originalDocuentsNames.items(), key=lambda originalDocuentsNames:originalDocuentsNames[1], reverse=True)
    if not sort:
        return retFiles
    else:
        return [i[0] for i in sort]
class zipHandle:
    def __init__(self):
        print 'create a zipHandle!'

    def zip_dir(self, dirname,zipfilename):
        filelist = []
        if os.path.isfile(dirname):
            if dirname != zipfilename:
                filelist.append(dirname)
        else :
            for root, dirs, files in os.walk(dirname):
                for name in files:
                    file = os.path.join(root, name)
                    if file == zipfilename:
                        ext = zipfilename.split('.')[-1]
                        zipfilename = zipfilename[:-1 * (len(ext) + 1)] + '1.' + ext
                        print 'The dst dic has a file that has a name same as dst file! Now change the dst file name as ' + zipfilename
                        filelist.append(os.path.join(root, name))

        zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
        print len(filelist)
        for tar in filelist:
            print tar
            arcname = tar[len(dirname):]
            #print arcname
            zf.write(tar,arcname)
        zf.close()

    def unzip_file(self, zipfilename, unziptodir):
        if not os.path.exists(unziptodir):
            os.makedirs(unziptodir, 0777)
        zfobj = zipfile.ZipFile(zipfilename)
        for name in zfobj.namelist():
            name = name.replace('\\','/')

            if name.endswith('/'):
                os.mkdir(os.path.join(unziptodir, name))
            else:
                ext_filename = os.path.join(unziptodir, name)
                ext_dir= os.path.dirname(ext_filename)
                if not os.path.exists(ext_dir) : os.makedirs(ext_dir,0777)
                outfile = open(ext_filename, 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()

def dumpObjToFile(obj, filePath):
    try:
        savefile = open(filePath, "wb")
        pickle.dump(obj, savefile, True)
        savefile.close()
#         msg = u'The data has been saved successfully!\n'
#         Tools.printAndLog(msg)
    except Exception, e:
        msg = u'An error occered when use dumpObjToFile function, and the error is ' + str(e) + '\n'
        Tools.printAndLog(msg, isError = True)

def loadObjFromFile(filePath):
    try:
        readfile = open(filePath, "rb")
        ret = pickle.load(readfile)
        readfile.close()
        return ret
    except Exception, e:
        msg = 'An error occered when use loadObjFromFile function, and the error is ' + str(e) + '\n' + filePath
        Tools.printAndLog(msg, isError = True)
        return None

if __name__ == '__main__':
#     basePath = u'E:\\MySpace\\Crawel\\_36ke\\articles'
#     filter = 's00'
#     for i in os.listdir(basePath):
#         print i
#         if filter in i:
#             old = os.path.join(basePath, i)
#             new = os.path.join(basePath, i[1 :])
#             print 'old is: ' + old
#             print 'new is: ' + new
#             os.rename(old, new)
#     files = os.listdir(basePath)
#     for i in files:
#         for j in os.listdir(basePath):
#             if i != j and j[:6] == i[:6]:
#                 os.remove(os.path.join(basePath, j))
    pickle.dump({}, open('E:\\MySpace\\Crawel\\infoq\\downloadedPages.dat','w+'))