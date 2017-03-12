

class BitMap():
	"""
	Bitmap using array of ints.

	Attributes:
		num_blocks: the number of blocks contained in this bitmap
		block_size: the size of each block in the bitmap
		bitmap: the bitmap with the size of blocksize
		mask_1: operate masking to assign 1 in ith bit of the target block
		mask_0: operate masking to assign 0 in ith bit of the target block
	"""

	def __init__(self, num_blocks=32, block_size=32):
		"""initiate a bitmap"""
		self.num_blocks = num_blocks
		self.block_size = block_size
		self.bitmap = [0]*self.num_blocks
		self.mask_1 = [0]*self.block_size
		self.mask_1[self.block_size-1] = 1
		for i, e in reversed(list(enumerate(self.mask_1))):
			if i <= 30:
				self.mask_1[i] = self.mask_1[i+1] << 1
		# self.mask_0 = [4294967295]*self.block_size
		self.mask_0 = [2**self.block_size-1]*self.block_size
		for i, e in enumerate(self.mask_0):
			self.mask_0[i] = self.mask_0[i] ^ self.mask_1[i]

	def occupy(self, i):
		"""Assign 1 to the index i to represent occupied frame"""
		offset = i % self.num_blocks
		ith  = i / self.num_blocks
		try:
			self.bitmap[ith] = self.bitmap[ith] | self.mask_1[offset]
		except IndexError:
			print 'List index out of range. Nothing changed'

	def free(self, i):
		"""Assign 0 to the index i to represent free frame"""
		offset = i % self.num_blocks
		ith  = i / self.num_blocks
		try:
			self.bitmap[ith] = self.bitmap[ith] & self.mask_0[offset]
		except IndexError:
			print 'List index out of range. Nothing changed'

	def resides(self,i):
		offset = i % self.num_blocks
		ith  = i / self.num_blocks
		return self.bitmap[ith+offset]

	def first_fit_one(self):
		for i,e in enumerate(self.bitmap):
			for j,b in enumerate(mask_1):
				if e & b:
					return (i*self.block_size) + j
		return None

	def first_fit_two(self):
		for i,e in enumerate(self.bitmap):
			for j,b in enumerate(mask_1):
				if e & b:
					if j == len(mask_1)-1:
						if not i == self.num_blocks-1:
							if bitmap[i+1] & mask_1[0]:
								return (i*self.block_size) + j
					else:
						if e & mask_1[j+1]:
							return (i*self.block_size) + j


		return None
	
	def print_bin(self):
		"""Print the bitmap in binary format for integer data type (32bits)"""
		print 'bitmap:'
		# print len(self.bitmap)
		for i,e in enumerate(self.bitmap):
			print '{}'.format(i).rjust(3),
			print '{0:032b}'.format(e)

class Frame():
	"""
	Representation of the frame in physical memory

	Attributes:
		entries: physical memory address assigned in the particular frame
	"""

	def __init__(self, size=512):
		self.entries = [0]*size

class SegmentationTable():
	"""	Representation of the Segmentation Table (ST) in frame """
	def __init__(self, size=512):
		self.entries = [0]*size

class PagingTable():
	"""	Representation of the Pagin Table (ST) in frame """
	def __init__(self, size=1024):
		self.entries = [0]*size

class Page():
	""" Representation of the Page in frame"""
	def __init__(self, size=512):
		self.entries = [0]*size

class PhysicalMemory():
	"""
	Physical Memory (PM) implementation.
	
	Attributes:
		num_frames: number of frames
		frame_size: size of each frame
		st_size: how many frames a Segmentation Table occupies in physical mem
		pt_size: how many frmaes a Page Table occupies in physical mem
		pg_size: how many frames a page occupies in physical memory
		frames: array of the representationo of physical memory with configuration above
		bitmap: bitmap manages whether a frame is free/occupied
	"""
	def __init__(self, num_frames=1024, frame_size=512, st_size=1, pt_size=2, pg_size=1):
		self.num_frames = num_frames
		self.frame_size = frame_size
		self.st_size = 1
		self.pt_size = 2
		self.pg_size = 1
		self.frames = [None]*num_frames  # 1024 frames * 512 words / frame = 524,288 ints
		self.frames[0] = SegmentationTable()  # the sgmentation table resides [0] always
		self.bitmap = BitMap()
		self.bitmap.occupy(0)  # register the ocuupation of [0]


class VirtualMemory():
	"""
	Virtual Memory (VM)) impolementation.
	
	Attributes:
		st: segmentation table
		pt: paging table
	"""
	def __init__(self):
		self.vm = [0]*512

def initialize_pm(st_input, pt_input):
	pm = PhysicalMemory()

	# print pm.bitmap.print_bin()
	
	# make entries in ST
	for st_pair in st_input:
		try:
			pm.frames[0].entries[st_pair[0]] = st_pair[1]
		except IndexError:
			print 'Out of bounds for the ST size (0-511)'
		st_id = (pm.frames[0].entries[st_pair[0]] / pm.frame_size)
		if not pm.bitmap.resides(st_id) > 0:  # check if the frame is allocatable
			pm.frames[st_id] = PagingTable()
			for i in range(pm.pt_size):
				pm.bitmap.occupy(st_id+i)  # make sure the residesnts registered
	print pm.frames[0].entries

	# make entries in PT
	for pt_triple in pt_input:
		if pm.frames[0].entries[pt_triple[1]] > 0:  # the segmentation table entry resides?
			st_id = (pm.frames[0].entries[pt_triple[1]] / pm.frame_size)  # idetify the frame
			if not pm.bitmap.resides(st_id) > 0:  # check if the frame is allocatable
				pm.frames[st_id].entries[pt_triple[0]] = pt_triple[2]  # assign
				
				if pt_triple[2] > -1: 
					pt_id = (pt_triple[2] / pm.frame_size)
					if not pm.bitmap.resides(pt_id) > 0:
						pm.frames[pt_id] = Page()
					for i in range(pm.pg_size):
						pm.bitmap.occupy(pt_id+i)  # make sure the residesnts registered
	print pm.frames[4].entries

	pm.bitmap.print_bin()
	return pm

def purse_va(va):
	va = '{0:032b}'.format(va)
	# print va
	# print bits
	# lead = va[0:4]
	lead = int(va[0:4],2)
	# st   = va[4:13]
	st   = int(va[4:13],2)
	# pt   = va[13:23]
	pt   = int(va[13:23],2)
	# pg   = va[23:32]
	pg   = int(va[23:32],2)
	print lead, st, pt, pg
	return st, pt, pg

def translate_vm(pm, va_inputs):
	for va_input in va_inputs:
		op = va_input[0]
		va = va_input[1]
		st, pt, pg = purse_va(va)
		if op == 0:
			#read
			if pm.frames[0].entries[st] == -1:
				print 'pf',
			elif pm.frames[0].entries[st] == 0:
				print 'err',
			else:
				pt_id = pm.frames[0].entries[st] / pm.frame_size
				if pm.frames[pt_id].entries[pt] == -1:
					print 'pf',
				elif pm.frames[pt_id].entries[pt] == 0:
					print 'err',
				else:
					print pm.frames[pt_id].entries[pt], pg 
					pa = pm.frames[pt_id].entries[pt] + pg
					print pa,
		elif op == 1:
			# write
			# when new allocation rquird, first-fit is fine
			# the choice of algorithms should not affect the correctness of the program
			if pm.frames[0].entries[st] == -1:
				print 'pf',
			if pm.frames[0].entries[st] > 0:
				pt_id = pm.frames[0].entries[st] / pm.frame_size
				if pm.frames[pt_id].entires[pt] == -1:
					print 'pf'
			pt_id = pm.frames[0].entries[st] / pm.frame_size
			# if ST entry is 0
			if pm.frames[0].entries[st] == 0:
				# check if there's allocatable frame for a Page Table
				available_frame = pm.bitmap.first_fit_two()
				if available_frame:  # if so, make a new paging table
					pm.frames[available_frame] = PagingTable()
					for i in range(pm.pt_size):  # register it in bitmap
						pm.bitmap.occupy(pt_id+i)
					pm.frames[0].entries[st] = available_frame*pm.frame_size
				else:  # if there's no available frame, no more process
					print 'No available for the PT'
				# if PT entry is 0
				if pm.frames[pt_id].entires[pt] == 0:
					# PA = PM[ PM[s] + p ] + w
					# check if there's allocatable frame for a Page
					available_frame = pm.bitmap.first_fit()
					if available_frame:  # if so, make a new page
						pm.frames[available_frame] = Page()
						for i in range(pm.pg_size):  # register it in bitmap
							pm.bitmap.occupy()
						pm.frames[pt_id].entries[pt] = available_frame*pm.frame_size
					else:
						print 'No avaliable for the Page'
					# find the alocatable frame, 
					# translate it into address format, 
					# register it in corresponding pt entry
				else:



			# 	if pm.frames[pt_id].entries[pt] == -1:
			# 		print 'pf',
			# 	elif pm.frames[pt_id].entries[pt] == 0:
			# 		print 'err',
			# 	else:
			# 		print pm.frames[pt_id].entries[pt], pg 
			# 		pa = pm.frames[pt_id].entries[pt] + pg
			# 		print pa,

			pass
		else:
			pass
		print ''




















