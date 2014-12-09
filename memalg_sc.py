#!/usr/bin/env python3

# Author: 	Daniel Bosk <daniel.bosk@miun.se>
# Date: 	14 November 2013

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

import queue
import sys

q = queue.Queue()

def memalg_sc( osmem, p, pt ):
	if ( pt[p].valid ):
		return

	sys.stdout.write( "page " + str( p ) + " generated page fault\n" )

	# if we still have free frames, use one of these
	if ( osmem.free_total() > 0 ):
		pt[p].frame = osmem.get_free_frame()
		sys.stdout.write( "allocated free frame " + str( pt[p].frame ) +
			" to page " + str( p ) + "\n" )
	# otherwise swap out one page
	else:
		qhead = q.get()
		while ( pt[qhead].valid and pt[qhead].referenced ):
			# if page has been referenced, give a second chance
			pt[qhead].referenced = False
			q.put( qhead )
			# and move on to the next page in the queue
			qhead = q.get()

		pt[qhead].valid = False
		osmem.swap_out( qhead )
		# allocate newly freed frame
		pt[p].frame = pt[qhead].frame

	# update the queue
	q.put( p )

	# actually swap in the page
	osmem.swap_in( p )
	pt[p].valid = True
	pt[p].modified = False
	pt[p].referenced = False

