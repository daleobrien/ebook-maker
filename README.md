## ebook-maker

Simple script to create an ebook in epub format.

### Dependencies

[Mako](http://www.makotemplates.org/) , which is used for templating. 

### Usage

  from ebook_maker import Ebook
  book = Ebook( output_folder = 'ebooks')

  book.isbn     = '0743421922'
  book.chapters =  [('Prologue','Some content ...'),
                    ('The Light of Ancient Mistakes', 'more content\n<i>etc</i>'),
                    ('Winter Storm','Lots of text\nAnother <b>line</b>\nthird line\nfourth line')]
  
  book.cover_art      = 'test/cover.jpg'
  book.primary_author = 'Banks, Iain M.'
  book.title          = 'Look to windward'
  
  book.save()

This will then create a book in the folder "ebooks" called "Banks, Iain M. - Look to windward.epub", 
provided the folder "ebooks" exists.

