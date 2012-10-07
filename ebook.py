#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
You have not received a copy of the GNU Lesser General Public License
along with this program.  Please see <http://www.gnu.org/licenses/>.

Simple script to create an ebook in epub format.

This program will scan a directory of sub-folders, where each sub-folder
resprents a book.  Within each sub-folder, there should be a series of text files for each
chapter.  For example:

    Book Title - Last Name, First Name.text
      chapter 1 - Introduction.text
      chapter 2 - More about ebooks.text
      ...

Each chapter should just be a plain text.  It can have some limited html
markup, such as bold <b>, italic <i> e.t.c.

Running example will generate an example source file to get one started.

    Usage:
        ebook -h
        ebook scan TEXT_SOURCE_FOLDER EBOOK_DESTINATION_FOLDER [-f FORMAT]
        ebook example TEXT_SOURCE_FOLDER EBOOK_DESTINATION_FOLDER
        ebook license

    Options:
        -h --help           Print this screen
        -f --format FORMAT  Ebook format [default: epub], only one option for now

'''

from os import path
from glob import glob
import re
from docopt import docopt
from renders.epub import Epub

digits = re.compile(r'(\d+)')


def natural_number_sorting(filename):
    '''helper to sort some filename naturally w.r.t. numbers.
        e.g. they should be ordered like this
            Chapter 01 - first.text
            Chapter 2 - second.text
            Chapter 3 - third.text

    '''
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))


def scan_folder_of_chapters(book_folder, output_folder):
    '''Given a folder look for text/txt files.
        The name should be of the form,

        e.g.
          chapter 01 - In the begining.txt
          chapter 02 - A little bit later.text

        and also some cover art
          cover.jpg

    '''

    book = Epub()
    book.output_folder = output_folder

    # extract book title and author form folder name
    title_author = book_folder[6:].split('-')
    if len(title_author) < 2:
        print "Warning: '%s' isn't for the form 'title - author'," +\
            " will skip this folder"
        return False

    book.title = title_author[0].strip()
    book.primary_author = "-".join(title_author[1:]).strip()

    chapters = []

    # file list, sorted
    filelist = glob("%s/*.*" % book_folder)
    filelist.sort(key=natural_number_sorting)

    for chapter in filelist:

        matched = re.match(u'.*\.[tT][xX][tT]$|.*\.[tT][eE][xX][tT]$', chapter)

        if matched:

            title = chapter.replace("%s/" % book_folder, '')
            title = "-".join(title.split('-')[1:])
            title = title.replace('.text', '')
            title = title.replace('.txt', '')

            chapters.append((title, open(chapter, 'r').read()))

    book.chapters = chapters

    # add an image file
    for image_name in ('jpg', 'JPG', 'jpeg', 'JPEG', 'Jpeg', 'Jpg'):
        image_name = '%s/cover.%s' % (book_folder, image_name)
        if path.exists(image_name):
            book.cover_art = image_name
            break
    else:
        print 'Warning: The cover art file, "%s/cover.jpg", wasn\'t found' %\
                                                                    book_folder
        book.cover_art = None

    book.save()

    return True


def scan_folder_for_books(arguments):
    '''Scan a folder, looking for folders that'''
    found = False

    for book_folder in glob("%s/*" % arguments['TEXT_SOURCE_FOLDER']):
        dest = arguments['EBOOK_DESTINATION_FOLDER']
        if scan_folder_of_chapters(book_folder, dest):
            found = True

    if not found:
        print 'Warning: No folders found in %s' %\
            arguments['TEXT_SOURCE_FOLDER']


if __name__ == '__main__':

    arguments = docopt(__doc__)

    if arguments['--format'] not in ('epub', ):
        print "ERROR: only support the epub format, '-f epub'"
        exit(-1)

    '''example ebook creation, scanning a folder'''
    if arguments['scan']:
        scan_folder_for_books(arguments)

    if arguments['license']:
        l = "\nThis program is free software: you can redistribute it "\
            "and/or modify\nit under the terms of the GNU Lesser General "\
            "Public License as published by\nthe Free Software Foundation, "\
            "either version 3 of the License, or\n(at your option) any "\
            "later version.\n\nThis program is distributed in the hope that "\
            "it will be useful,\nbut WITHOUT ANY WARRANTY; without even the "\
            "implied warranty of\nMERCHANTABILITY or FITNESS FOR A "\
            "PARTICULAR PURPOSE.  See the\nGNU Lesser General Public "\
            "License for more details.\n"
        print l
        exit(0)

    '''Creating a book programically'''
    if arguments['example']:

        print 'Not done yet!'
        exit(0)

        print 'creating a couple of chapters ... '
        # (title, content)
        chapter_1 = ('Introduction', 'Very short blob of text.')

        text = '''<b>Bold</b> short blob of text.
        <i>Italic</i> an so on.
        Another line of text, but a little longer and so on.

        Multiline gaps will be ignored.
        To create a newline, use the "<br>" tag.
        <br>
        <br>
        Line further down.
        <blockquote>Some text</blockquote>
        '''

        chapter_2 = ('Formatting', text)

        book = Epub()

        book.isbn = '0743421922'
        book.primary_author = 'Banks, Iain M.'
        book.title = 'Look to windward'
        book.cover_art = 'test/cover.jpg'

        book.chapters = [('Prologue', 'Some content ...'),
                         ('The Light of Ancient Mistakes',
                          'more content...\n<i>etc</i>'),
                         ('Winter Storm',
              'Lots of text\nAnother <b>line</b>...\nthird line\nfourth line')]

        book.save()

    ##
