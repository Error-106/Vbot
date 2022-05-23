import sys
import re
import os
import time

text = sys.argv[1]
name = text.split('/')
length = len(name)
length_end = len(name[length-1])
houzhui = name[length-1][-3:]
newpath = text[:-length_end]
filename = text[-length_end:]

zhengze = re.compile(r'\[(.+?)\]', re.S)
judge = re.findall(zhengze, filename)

if(judge[0] == "NC-Raws"):
    name1 = text.split(' - ')
    EP = name1[1][:2]
    seanson1 = name[length-2]
    seanson = re.findall("\d+",seanson1)[0]
    os.rename(text,newpath + 'S' + seanson + 'E' + EP + '.'+ houzhui)
    nn = name[length-3]
    nn = nn.encode("ISO-8859-1").decode('utf-8')
elif(judge[0] == "NaN-Raws"):
    EP = judge[1]
    seanson1 = name[length-2]
    seanson = re.findall("\d+",seanson1)[0]
    os.rename(text,newpath + 'S' + seanson + 'E' + EP + '.'+ houzhui)
    nn = name[length-3]
    nn = nn.encode("ISO-8859-1").decode('utf-8')
elif(judge[0] == "ANi"):
    EP = judge[1]
    seanson1 = name[length-2]
    seanson = re.findall("\d+",seanson1)[0]
    os.rename(text,newpath + 'S' + seanson + 'E' + EP + '.'+ houzhui)
    nn = name[length-3]
    nn = nn.encode("ISO-8859-1").decode('utf-8')


time.sleep(5)
os.system('rclone copy --drive-chunk-size 64M /media/Emby_Temp/ googledrive:Emby/动漫/2022-4/ &') #这里只是例子，请根据自己的实际路径更改
time.sleep(90)
'''这里原本是自动刷新媒体库，因涉及到的敏感信息太多，故整段删除，如果想添加属于自己的自动扫库可以进行抓包，然后通过python post发送。不教了，开摆。'''

