__author__ = 'tamal.2k14@gmail.com (Tamal Sen)'
# Get PyDrive module from repository
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import ApiRequestError

def GetHumanReadable(size,precision=2): # Byte size to human readable size
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f %s"%(precision,size,suffixes[suffixIndex])

def details(Metadata): # function to print selected attributes from metadata
    def printvalues(ValueName, ValueMeta):
        fetchedData = Metadata[ValueMeta]
        if ValueMeta == 'fileSize':
            fetchedData = GetHumanReadable(int(fetchedData))
        else:
            fetchedData
        print '%s : %s' % (ValueName, fetchedData)

    print '-----Details-----'
    printvalues('ID', 'id')
    printvalues('Title', 'title')
    printvalues('Owner', 'ownerNames')
    printvalues('Size','fileSize')
    printvalues('Sharing Link', 'alternateLink')
    printvalues('Download Link', 'webContentLink') # This will provide the download link

def IdExtractor(Link): # Eliminating unnecessary sub-strings to get ID from a share link
    try:
        if 'file/d' in Link:
            Link = Link.split("file/d/", 1)[1]
        elif 'open?id=' in Link:
            Link = Link.split("/open?id=", 1)[1]
        if '/view' in Link:
            Link = Link.split('/view')
            ID = Link[0]
        elif '/preview' in Link:
            Link = Link.split('/preview')
            ID = Link[0]
        else:
            ID = Link
        return ID
    except:
        print 'No ID found on given URL'

gauth = GoogleAuth() # initiate Google Auth because you need to allow this app
gauth.LoadCredentialsFile("mycreds.txt") # Create a file named 'mycreds.txt' of root directory of this program
if gauth.credentials is None: # allow access to app to use Google Drive API
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.LocalWebserverAuth()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth) # get instance from Google Drive
URL = 'https://docs.google.com/file/d/0B0rP928erB3KekVvWmRCTEZPNWM/preview?pli=1' # Let's say, this is a sample link

try:
    print 'Given Link: ' + URL
    file1 = drive.CreateFile({'id': IdExtractor(URL)}) # create a file class with ID extracted from URL
    file1.FetchMetadata(fetch_all=True) # fetch metadata for this file

    details(file1.metadata) # calling details() function to print the attributes
except ApiRequestError as Exception:
    print 'File Not Found'

'''
for x in file1.metadata: #Print all available metadata
        print str(x) +' : '+str(file1.metadata[x])
        
Meta = file1.GetPermissions() #Read Permission

#Automatically set permission for own file for direct download link
permission = file1.InsertPermission({ 
                        'type': 'anyone',
                        'value': 'anyone',
                        'role': 'reader'})

'''
