#!/usr/bin/env python3

# Author: 	Daniel Bosk <daniel.bosk@miun.se>
# Date: 	17 November 2013

# Copyright (c) 2013, Daniel Bosk <daniel.bosk@miun.se>
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

queue = []
qhead = 0

def remove_from_queue( n ):
	if ( n >= len( queue ) ):
		raise Exception( "cannot remove element outside of queue" )
	i = ( qhead + n ) % len(queue)
	while ( i != qhead ):
		queue[i] = queue[ (i+1) % len(queue) ]
		i = ( i + 1 ) % len(queue)

def memalg_esc( osmem, p, pt ):
	global qhead

	if ( pt[p].valid ):
		return

	sys.stdout.write( "page " + str( p ) + " generated page fault\n" )

	# if we still have free frames, use one of these
	if ( osmem.free_total() > 0 ):
		pt[p].frame = osmem.get_free_frame()
		sys.stdout.write( "allocated free frame " + str( pt[p].frame ) +
			" to page " + str( p ) + "\n" )
		queue.append( p )
	# otherwise swap out one page
	else:
		# before starting the level should be higher than any level
		best_lvl = 5
		# we start at qhead, so it's best so far
		best_idx = qhead

		for i in range( len( queue ) ):
			cur = qhead % len( queue )
			page = pt[ queue[ cur ] ]

			# check the different classes
			if ( not page.referenced and not page.modified and best_lvl > 1 ):
				best_idx = cur
				best_lvl = 1

			elif ( not page.referenced and page.modified and best_lvl > 2 ):
				best_idx = cur
				best_lvl = 2

			elif ( page.referenced and not page.modified and best_lvl > 3 ):
				best_idx = cur
				best_lvl = 3

			elif ( page.referenced and page.modified and best_lvl > 4 ):
				best_idx = cur
				best_lvl = 4

			# reset the referenced bit to see which are used to next time
			page.referenced = False
			qhead = ( qhead + 1 ) % len( queue )

		qhead = best_idx

		# swap-out the best choice
		pn = queue[ qhead ]
		pt[pn].valid = False
		osmem.swap_out( pn )
		# allocate newly freed frame
		pt[p].frame = pt[pn].frame

		# update the queue, add the new page to the end of the queue
		queue[ qhead % len(queue) ] = p
		qhead = ( qhead + 1 ) % len( queue )

	# actually swap in the page
	osmem.swap_in( p )
	pt[p].valid = True
	pt[p].modified = False
	pt[p].referenced = False

