import docx
import os
import datetime

article_list = []
for file in filter(lambda x : x[-5:] == '.docx', os.listdir('.')):
    stat = os.stat(file)
    utime = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    txt = '\n--------------------------------------------------------\n' + file[:-5] + '\n' + utime + '\n\n'
    doc = docx.Document(file)
    for para in doc.paragraphs:
        txt += para.text
    txt += '\n\n'
    article_list.append((stat.st_mtime, txt))

article_list.sort(reverse=True)
print (''.join([x[1] for x in article_list]))
