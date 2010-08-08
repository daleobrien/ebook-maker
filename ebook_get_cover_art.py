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

import urllib,os

def retrive_cover( isbn, save_folder='covers' ):
    '''Retreve a book cover using openlibrary, e.g.

    >> retrive_cover( '0743421922', 'images')

    will result in the following file,

        images/0743421922.jpg

    note: isbn must be a string'''


    a = urllib.urlopen( "http://covers.openlibrary.org/b/isbn/%s-L.jpg"%isbn )

    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    f = open( os.path.join(save_folder,'%s.jpg'%isbn),'wb')
    content = a.read()

    # check we have actually recieved an image
    if len(content)==807:
        raise ValueError, 'Cover art for %s not found'%isbn

    f.write(content)
    f.close()

if __name__ == '__main__':

    retrive_cover( '0743421922', 'images')
