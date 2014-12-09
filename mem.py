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

# this class represents an entry in the page table
class PageEntry:
	def __init__( self ):
		# the page entry points to a certain frame
		self.frame = None
		# indicates whether this entry is valid or invalid
		self.valid = False
		# indicates whether this page has been referenced or not
		self.referenced = False
		# indicates whether this page has been modified or not
		self.modified = False

class HWMemory:
	def __init__( self, sz_memory, sz_pagetable, os ):
		# keeps tracks of the size of physical memory
		self.sz_memory = sz_memory
		# the size of the pagetable
		self.sz_pagetable = sz_pagetable
		# the OS functionality, used to interrupt OS
		self.os = os

		# initialize the pagetable to the correct size
		self.pagetable = []
		for i in range( self.sz_pagetable ):
			page = PageEntry()
			self.pagetable.append( page )

	def read( self, page ):
		# as the page number is an index to the page table,
		# make sure we do not end up outside the page table.
		if ( page >= len( self.pagetable ) ):
			raise Exception( "page out of range: " + str( page ) )
		# if the valid bit in the page table is unset make the
		# paging algorithm try to swap the page in.
		elif ( not self.pagetable[page].valid ):
			self.os.memalg( page, self.pagetable )

		self.pagetable[page].referenced = True
		return self.pagetable[page].frame

	def write( self, page ):
		# as the page number is an index to the page table,
		# make sure we do not end up outside the page table.
		if ( page >= len( self.pagetable ) ):
			raise Exception( "page " + str( page ) +
				" generated abort trap: process killed" )
		# if the valid bit in the page table is unset make the
		# paging algorithm try to swap the page in.
		elif ( not self.pagetable[page].valid ):
			# interrupt to operating system handling routine, i.e.
			# to our page replacement algorithm
			self.os.memalg( page, self.pagetable )

		self.pagetable[page].referenced = True
		self.pagetable[page].modified = True

		return self.pagetable[page].frame
