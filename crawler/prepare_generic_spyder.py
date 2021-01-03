import sys
import os
from os import path

if (path.exists("urls2")):
    #copy file to volume
    copy_urls = "copy urls additional\\{0}\\urls".format(sys.argv[1])    #windows backslash + copy
    copy_rules = "copy rules additional\\{0}\\rules".format(sys.argv[1])

    #copy_rules = "cp urls /{0}/urls".format(sys.argv[1])   #docker slashes + cp
    #copy_rules = "cp rules /{0}/rules".format(sys.argv[1])   #docker slashes + cp

    os.system("mkdir additional\\{0}".format(sys.argv[1]))
    os.system(copy_urls)
    os.system(copy_rules)

    #open copied files
    urls = open('additional/{0}/urls'.format(sys.argv[1]), 'r')
    rules = open('additional/{0}/rules'.format(sys.argv[1]), 'r')
    read = urls.readlines()
    url_list = []

    for url in read:
        url_list.append(url.strip())

    print(url_list)

    #os.system("scrapy crawl generic")
elif (path.exists("\\additional\\{0}".format(sys.argv[1]))):
    #If the folder for new crawler was previously created under /custom, then call generic crawler with existing data
    os.system("scrapy crawl generic -a name={0}".format(sys.argv[1]))
    print("dum")