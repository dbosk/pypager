#!/usr/bin/env python3

# Author: 	Daniel Bosk <daniel.bosk@miun.se>
# Date: 	26 October 2013

# Copyright (c) 2012, Daniel Bosk <daniel.bosk@miun.se>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
#  - Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys
import osmem # our OS memory module
import mem 	# our HW memory module
# our available page replacement algorithms
import memalg_fifo
import memalg_sc
import memalg_esc

# bug, string "1 w" crashes program (Marko Loncar)
def reference_string( instream = sys.stdin ):
	for line in instream:
		for word in line.split():
			if ( word[0].isalpha() ):
				op = word[0]
				page = int( word[1:] )
			else:
				op = 'r'
				page = int( word )
			yield (op, page)


#### THE MAIN PROGRAM ####

def main( argc, argv ):
	# change these value to experiment
	nframes = 5
	npages = 10
	alg = memalg_fifo.memalg_fifo
	#alg = memalg_sc.memalg_sc
	#alg = memalg_esc.memalg_esc

	osm = osmem.OSMemory( nframes, npages, alg )
	memory = mem.HWMemory( nframes, npages, osm )

	for (op, page) in reference_string():
		if ( op == 'r' or op == 'R' ):
			frame = memory.read( page )
		elif ( op == 'w' or op == 'W' ):
			frame = memory.write( page )
		else:
			raise Exception( "illegal memory operation: " + str( op ) )

		sys.stdout.write( "page " + str( page ) + " mapped to frame " +
					str( frame ) + "\n" )


if ( __name__ == "__main__" ):
	#main( len(sys.argv), sys.argv )
	try:
		main( len(sys.argv), sys.argv )
	except Exception as e:
		sys.stderr.write( str( e ) + "\n" )
		sys.exit( -1 )
	sys.exit( 0 )
