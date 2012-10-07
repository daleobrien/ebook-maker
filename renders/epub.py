# -*- coding: utf-8 -*-

from ebook import Ebook

from mako.template import Template
from os import remove, path, mkdir
from tempfile import mkstemp
from zipfile import ZipFile,  ZIP_DEFLATED


class EpubContainer(ZipFile):

    def writecontent(self, filename, content):
        ''' writestr(filename, content) seems to cause problems,
            content is ok, but the permission are wrong (atleast on OSX)

            so, what we do is:
                a) create a temp file
                b) write content to the temp file
                c) add temp file to zip
                d) remove the temp file

        '''

        handle, temp_filename = mkstemp()

        f = open(temp_filename, 'w')
        f.write(content)
        f.close()

        # actually add to the epub (zip file), override the archive name,
        # so we don't end up having the temp file as the name
        self.write(temp_filename, arcname=filename)

        # remove tempfile, we are done
        remove(temp_filename)


class Epub(Ebook):

    def save(self, overrided_name=None):

        if not path.exists(self.output_folder):
            mkdir(self.output_folder)

        # book file name
        epub_filename = path.join(self.output_folder,
                                     "%s - %s.epub" % (self.primary_author,
                                                       self.title))

        # create the ebook
        epub_book = EpubContainer(epub_filename, 'w', ZIP_DEFLATED)

        # add cover art to the book
        if self.cover_art is not None:
            epub_book.write(self.cover_art, arcname='cover.jpg')

        # add varous meta files, that describe the book
        for filename in ['stylesheet.css',
                         'mimetype',
                         'titlepage.xhtml',
                         'META-INF/container.xml']:
            src = path.join(self.template_folder, filename)
            epub_book.write(src, arcname=filename)

        # build the main content files
        book = {}
        for arg in self.__slots__:
            book[arg] = getattr(self, arg)

        for template in ['content.opf', 'toc.ncx']:
            template_file = path.join(self.template_folder, template)
            xml_content = Template(filename=template_file,
                                    default_filters=['decode.utf8'],
                                    input_encoding='utf-8').render(**book)
            epub_book.writecontent(template, xml_content)

        # add the content of each chapter
        for i, (title, content) in enumerate(self.chapters):

            xml = None
            if self.renderer == 'text':
                filename = path.join(self.template_folder,
                                     'chapter_template_plain_text.xhtml')

                content = self.escape_text_to_html(content)
                # make more html like

                xml = Template(filename=filename,
                               default_filters=['decode.utf8'],
                               input_encoding='utf-8').render(title=title,
                                                              content=content)
            elif self.renderer == 'rtf':
                raise Exception("don't have a template for rtf !")

            if xml is not None:
                epub_book.writecontent('chapter_%03d.xhtml' % i, xml)

#
