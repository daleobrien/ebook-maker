## ebook-maker

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


### Dependencies


[Mako](http://www.makotemplates.org/) , which is used for templating. 

[docopt](https://github.com/docopt/docopt), which is used for command line options