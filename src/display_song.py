"""
Thierry Bertin-Mahieux (2010) Columbia University
tb2332@columbia.edu

Code to quickly see the content of an HDF5 file.

This is part of the Million Song Dataset project from
LabROSA (Columbia University) and The Echo Nest.


Copyright 2010, Thierry Bertin-Mahieux

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import hdf5_getters
import numpy as np
import pickle

XS_PATH = "../batch/b1_xs"
S_PATH = "../batch/b2_s"
M_PATH = "../batch/b3_m"
L_PATH = "../batch/b4_l"
 
def die_with_usage():
    """ HELP MENU """
    print 'display_song.py'
    print 'T. Bertin-Mahieux (2010) tb2332@columbia.edu'
    print 'to quickly display all we know about a song'
    print 'usage:'
    print '   python display_song.py [FLAGS] <HDF5 file> <OPT: song idx> <OPT: getter>'
    print 'example:'
    print '   python display_song.py mysong.h5 0 danceability'
    print 'INPUTS'
    print '   <HDF5 file>  - any song / aggregate /summary file'
    print '   <song idx>   - if file contains many songs, specify one'
    print '                  starting at 0 (OPTIONAL)'
    print '   <getter>     - if you want only one field, you can specify it'
    print '                  e.g. "get_artist_name" or "artist_name" (OPTIONAL)'
    print 'FLAGS'
    print '   -summary     - if you use a file that does not have all fields,'
    print '                  use this flag. If not, you might get an error!'
    print '                  Specifically desgin to display summary files'
    sys.exit(0)

def get_modified_getters():
    with open("filtered_getters.txt", 'r') as f:
            content = f.readlines()

    content = [x.strip() for x in content]
    content = ['get_' + x for x in content]
    
    temp = set(content)
    content = list(temp)
    return content

def get_song_id(path):

    parts = path.split("\\")
    parts = parts[len(parts)-1].split(".")
    return parts[0]

def get_song_info(song_path, pickle_path):

    #Create a dictionary with fields and dump in pickle
    data = {}
    data['pickle_id'] = get_song_id(song_path)
    #print data['pickle_id']

    # get params
    hdf5path = song_path
    songidx = 0
    onegetter = ''

    # if len(sys.argv) > 2:
    #     songidx = int(sys.argv[2])
    # if len(sys.argv) > 3:
    #     onegetter = sys.argv[3]

    # sanity check
    if not os.path.isfile(hdf5path):
        print 'ERROR: file',hdf5path,'does not exist.'
        sys.exit(0)
    h5 = hdf5_getters.open_h5_file_read(hdf5path)
    numSongs = hdf5_getters.get_num_songs(h5)
    if songidx >= numSongs:
        print 'ERROR: file contains only',numSongs
        h5.close()
        sys.exit(0)

    # get all getters
    getters = get_modified_getters()
    #print getters

    # print them
    for getter in getters:
        try:
            res = hdf5_getters.__getattribute__(getter)(h5,songidx)
        except AttributeError, e:
            if summary:
                continue
            else:
                print e
                print 'forgot -summary flag? specified wrong getter?'
        if res.__class__.__name__ == 'ndarray':
            print getter[4:]+": shape =",res.shape
        else:
            data[getter[4:]] = str(res)
            #print getter[4:]+":",res

    pickle.dump(data, open(pickle_path + data['pickle_id'] + ".p", "wb"))
    print "Done: ", data['pickle_id']
    h5.close()


def make_paths(filepath, fname, pickle_path):
    
    target = open(fname, 'w')

    for dirname, dirnames, filenames in os.walk(filepath):
        # print path to all subdirectories first.
        # for subdirname in dirnames:
        #     print(os.path.join(dirname, subdirname))

        # print path to all filenames.
        for filename in filenames:
            print(os.path.join(dirname, filename))
            target.write(os.path.join(dirname, filename))
            target.write("\n")
    target.close()

    with open(fname, 'r') as f:
            content = f.readlines()

    content = [x.strip() for x in content]

    #Iterate over each file path and get the song details
    count = 0
    for each_file in content:
        get_song_info(each_file, pickle_path)

if __name__ == '__main__':

     print "XS"
     #make_paths(XS_PATH, 'xs_files.txt', '../data/xs_song_data')
    
     print "S"
     #make_paths(S_PATH, 's_files.txt', '../data/s_song_data')
    
     print "M"
     #make_paths(M_PATH, 'm_files.txt', '../data/m_song_data')
    
     print "L"
     make_paths(L_PATH, 'l_files.txt', '../data/l_song_data')
