#!/usr/bin/env python

from mako.template import Template
from os import mkdir, remove, path
from shutil import copytree, copyfile,rmtree
from cStringIO import StringIO
from tempfile import mkstemp

from zipfile import ZipFile,  ZIP_DEFLATED

#from PIL import Image

def prop(func):
    '''see http://code.activestate.com/recipes/576742/ '''
    ops = func() or {}
    name=ops.get('prefix','_')+func.__name__ # property name
    fget=ops.get('fget',lambda self:getattr(self, name))
    fset=ops.get('fset',lambda self,value:setattr(self,name,value))
    fdel=ops.get('fdel',lambda self:delattr(self,name))
    return property ( fget, fset, fdel, ops.get('doc','') )
    

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

    def __init__(self,
                 isbn               = '0123456789',
                 cover_art          = None,
                 title              = "The Book Title",
                 primary_author     = 'Blogs, Joe',
                 secondary_authors  = [],
                 language           = "en",
                 publisher          = "some publisher",
                 date               = '2010',
                 renderer           = 'text',
                 chapters           =  [('Prologue','Some content ...'),
                                        ('Chapter 1: Soup', 'first line\nsecond line\n')],
                 template_folder    = './template',
                 output_folder      = './'):

        ''' Creates a new ebook based upon a dictionary,
            e.g. 
            ebook =  {'isbn'              : '0743421922' ,
                      'cover_art'         : 'test/cover.jpg',  # location of the cover art file
                      'title'             : 'The hand of Oberon',
                      'primary_author'    : 'Banks, Iain M.',
                      'secondary_authors' : [],
                      'language':'en',
                      'publisher':'New York : Avon Books',
                      'date':2002', #  YYYY[-MM[-DD]]
                      'renderer': 'text',  # either text, rtf, ... TODO only handles text for now
                      'chapters' : [('Prologue','Some content ...'),
                                    ('The Light of Ancient Mistakes', 'more content...\n etc'),
                                    ('Winter Storm','Lots of text\nAnother line ...\nthird line')]
               }

            thus,

            >>> from build_epub import Ebook
            >>> book = Ebook()
            >>>
            >>> book.isbn           = "0743421922"
            >>> book.primary_author = 'Banks, Iain M.'
            >>> book.date           = '2002'
            >>> book.chapters       = [('Prologue','Some content ...'),
                                       ('The Light of Ancient Mistakes', 'more content...\n etc'),
                                       ('Winter Storm','Lots of text\nAnother line ...\nthird line')]

            >>> create_ebook_from_dictionary( ebook) 

            would create a 'Banks, Iain M. - Look to windward.epub' in the folder 'ebooks'


        '''


        # book details and content
        self._isbn              = isbn
        self._cover_art         = cover_art
        self._title             = title
        self._primary_author    = primary_author
        self._secondary_authors = secondary_authors
        self._language          = language
        self._publisher         = publisher
        self._date              = date
        self._renderer          = renderer
        self._chapters          = chapters

        # envirnoment details
        self._template_folder   = template_folder
        self._output_folder     = output_folder

    @prop
    def isbn(): pass

    @prop
    def cover_art(): pass

    @prop
    def title(): pass

    @prop
    def primary_author(): pass

    @prop
    def secondary_authors(): pass

    @prop
    def language(): pass

    @prop
    def publisher(): pass

    @prop
    def date(): pass

    @prop
    def renderer(): pass

    @prop
    def chapters():
        '''e.g.  chapters = [('Prologue','Some content ...'),
                             ('Chapter 1: Soup', 'first line\nsecond line\n')]
        '''
        pass

    @prop
    def template_folder(): pass

    @prop
    def output_folder(): pass


    def save(self, overrided_name=None):

        if not path.exists(self._output_folder):
            raise Exception, "Folder [%s] doesn't exisit"%self._output_folder

        # book file name
        epub_filename = path.join(self._output_folder,
                                     "%s - %s.epub" %(self._primary_author ,
                                                      self._title))

        # create the ebook
        epub_book = Epub(epub_filename,'w', ZIP_DEFLATED)

        # add cover art to the book
        if self._cover_art is not None:
            # convert to greyscale
            #handle,temp_filename = mkstemp(suffix='.jpg')
            #im = Image.open(self._cover_art).convert("L")
            #im.save(temp_filename)
            #epub_book.write(temp_filename, arcname='cover.jpg')
            #remove(temp_filename)
            epub_book.write(self._cover_art, arcname='cover.jpg')

        # add varous meta files, that describe the book
        for filename in ['stylesheet.css', 'mimetype', 'titlepage.xhtml' ,'META-INF/container.xml']:
            src = path.join(self._template_folder, filename)
            epub_book.write(src, arcname=filename )

        # build the main content files
        __book = {'isbn':self._isbn,
                  'title':self._title,
                  'primary_author':self._primary_author,
                  'secondary_authors':self._secondary_authors,
                  'language':self._language,
                  'publisher':self._publisher,
                  'date':self._date,
                  'cover_art':self._cover_art,
                  'chapters':self._chapters
                }

        for template in ['content.opf', 'toc.ncx']:
            template_file = path.join(self._template_folder,template)
            xml_content =  Template( filename=template_file).render(**__book)
            epub_book.writecontent(template, xml_content)

        # add the content of each chapter
        for i,chapter in enumerate(self._chapters):

            xml = None
            if self._renderer == 'text':
                xml = Template( filename=path.join(self._template_folder,'chapter_template_plain_text.xhtml')).render(title=chapter[0],
                                                                                                           content=chapter[1])
            elif self._renderer == 'rtf':
                raise Exception,"don't have a template for rtf !"

            if xml is not None:
                epub_book.writecontent('chapter_%03d.xhtml'%i,xml)


if __name__ == '__main__':


    book = Ebook( output_folder = 'ebooks')

    book.isbn     = '0743421922'
    book.chapters =  [('Prologue','Some content ...'),
                      ('The Light of Ancient Mistakes', 'more content...\n<i>etc</i>'),
                      ('Winter Storm','Lots of text\nAnother <b>line</b>...\nthird line\nfourth line')]

    book.cover_art      = 'test/cover.jpg'
    book.primary_author = 'Banks, Iain M.'
    book.title          = 'Look to windward'

    book.save()

