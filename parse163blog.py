#!/usr/local/bin/python

import xml.sax
import os
from html.parser import HTMLParser
import datetime

blogList = []
class Blog163Handler (xml.sax.ContentHandler):
    def __init__(self):
        self.title = ''    
        self.time = ''    
        self.content = ''
        self.buf = ''

    def characters(self, content):
        textWithFormat = content.strip()
        text = []
        class ContentHtmlParser (HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag == 'br':
                    text.extend('\n')
            def handle_data(self, data):
                text.extend(data);
        try: 
           ContentHtmlParser().feed(textWithFormat)
           self.buf = ''.join(text);
        except Exception:
           print('error striping html tag of article: ' + self.title)
           self.buf = textWithFormat
            
    def startElement(self, tag, attrs):
        pass

    def endElement(self, tag):
        if tag == 'title':
            self.title = self.buf
        elif tag == 'publishTime':
            self.time = self.buf
        elif tag == 'content':
            self.content = self.buf
            if self.title != '':
                name = self.title + '.txt'
                with open(name, 'w') as f:
                   f.write(self.content)
                os.utime(name, (int(self.time[:-3]), int(self.time[:-3]))) 
                date = datetime.datetime.fromtimestamp(int(self.time[:-3])).strftime('%Y-%m-%d %H:%M:%S')
                blogList.append(self.title + '\n' + date + '\n\n' + self.content)

            self.title = ''
            self.time = ''
            self.content = ''


if __name__ == '__main__':
    parser = xml.sax.make_parser()
    parser.setContentHandler(Blog163Handler())
    parser.parse('163blog.xml')
    merged = '\n\n--------------------------------------------------------------\n'.join(blogList)
    with open('163_blog_merged.txt', 'w') as f:
        f.write(merged)
