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

class OSMemory:
	def __init__( self, nframes, npages, alg ):
		self.nframes = nframes
		self.npages = npages
		self.alg = alg

		self.free_map = [ True ] * self.nframes

	def free_total( self ):
		return self.free_map.count( True )

	def get_free_frame( self ):
		frame = self.free_map.index( True )
		self.free_map[frame] = False
		return frame

	def release_frame( self, frame ):
		self.free_map[frame] = True

	def swap_out( self, page ):
		sys.stdout.write( "swapped out page " + str( page ) + "\n" )

	def swap_in( self, page ):
		sys.stdout.write( "swapped in page " + str( page ) + "\n" )

	def memalg( self, page, pagetable ):
		self.alg( self, page, pagetable )

