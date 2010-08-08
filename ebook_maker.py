#!/usr/bin/env python
'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You have not received a copy of the GNU Lesser General Public License
    along with this program.  Please see <http://www.gnu.org/licenses/>.

'''

from mako.template import Template
from os import mkdir, remove, path
from shutil import copytree, copyfile,rmtree
from cStringIO import StringIO
from tempfile import mkstemp
from zipfile import ZipFile,  ZIP_DEFLATED
import time

class Epub(ZipFile):

    def writecontent(self, filename, content):
        ''' writestr(filename, content) seems to cause problems,
            content is ok, but the permission are wrong (atleast on OSX)
    
            so, what we do is:
                a) create a temp file
                b) write content to the temp file
                c) add temp file to zip
                d) remove the temp file

        '''

        handle,temp_filename = mkstemp()

        f = open(temp_filename,'w')
        f.write(content)
        f.close()

        # actaully add to the epub (zip file), override the archive name,
        # so we don't end up having the temp file as the name
        self.write(temp_filename, arcname=filename)

        # remove tempfile, we are done
        remove(temp_filename)

class Ebook(object):

    __slots__ = ['isbn', 'cover_art', 'title','primary_author',
                 'secondary_authors', 'language','publisher',
                 'date','renderer','chapters','template_folder',
                 'output_folder']

    def __init__(self):

        self.isbn              = '0123456789' 
        self.primary_author    = "Anonymous"
        self.secondary_authors = []
        self.template_folder   = path.join( path.split(__file__)[0],'template')
        self.language          = 'en'
        self.publisher         = "None"
        self.renderer          = 'text'
        self.date              = time.asctime()
        self.output_folder     = "./"

    def save(self, overrided_name=None):

        if not path.exists(self.output_folder):
            raise Exception, "Folder [%s] doesn't exisit"%self.output_folder

        # book file name
        epub_filename = path.join(self.output_folder,
                                     "%s - %s.epub" %(self.primary_author ,
                                                      self.title))

        # create the ebook
        epub_book = Epub(epub_filename,'w', ZIP_DEFLATED)

        # add cover art to the book
        if self.cover_art is not None:
            epub_book.write(self.cover_art, arcname='cover.jpg')

        # add varous meta files, that describe the book
        for filename in ['stylesheet.css', 'mimetype', 'titlepage.xhtml' ,'META-INF/container.xml']:
            src = path.join(self.template_folder, filename)
            epub_book.write(src, arcname=filename )

        # build the main content files
        book = {}
        for arg in self.__slots__:
            book[arg] = getattr(self,arg)

        for template in ['content.opf', 'toc.ncx']:
            template_file = path.join(self.template_folder,template)
            xml_content =  Template(filename=template_file,
                                    default_filters=['decode.utf8'],
                                    input_encoding='utf-8').render(**book)
            epub_book.writecontent(template, xml_content)

        # add the content of each chapter
        for i,chapter in enumerate(self.chapters):

            xml = None
            if self.renderer == 'text':
                filename = path.join(self.template_folder,'chapter_template_plain_text.xhtml')
                xml = Template(filename=filename,
                               default_filters=['decode.utf8'],
                               input_encoding='utf-8').render(title=chapter[0],
                                                              content=chapter[1])
            elif self.renderer == 'rtf':
                raise Exception,"don't have a template for rtf !"

            if xml is not None:
                epub_book.writecontent('chapter_%03d.xhtml'%i,xml)

if __name__ == '__main__':

    # TODO are command line options

    '''example ebook creation, with just a tiny bit of text'''

    book = Ebook()

    book.output_folder   = '../ebooks'

    book.isbn     = '0743421922'
    book.chapters =  [('Prologue','Some content ...'),
                      ('The Light of Ancient Mistakes', 'more content...\n<i>etc</i>'),
                      ('Winter Storm','Lots of text\nAnother <b>line</b>...\nthird line\nfourth line')]

    book.cover_art      = 'test/cover.jpg'
    book.primary_author = 'Banks, Iain M.'
    book.title          = 'Look to windward'

    book.save()

