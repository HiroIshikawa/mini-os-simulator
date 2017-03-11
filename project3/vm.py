

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
	
	def print_bin(self):
		"""Print the bitmap in binary format for integer data type (32bits)"""
		print 'bitmap:'
		for e in self.bitmap:
			print '{0:032b}'.format(e),

class Frame():
	"""
	Representation of the frame in physical memory

	Attributes:
		entries: physical memory address assigned in the particular frame
	"""

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
		pm: array of the representationo of physical memory with configuration above
		bitmap: bitmap manages whether a frame is free/occupied
	"""
	def __init__(self, num_frames=1024, frame_size=512, st_size=1, pt_size=2, pg_size=1):
		self.num_frames = num_frames
		self.frame_size = frame_size
		self.st_size = 1
		self.pt_size = 2
		self.pg_size = 1
		self.pm = [None]*num_frames  # 1024 frames * 512 words / frame = 524,288 ints
		self.pm[0] = Frame()  # the sgmentation table resides [0] always
		self.bitmap = BitMap()
		self.bitmap.occupy(0)  # register the ocuupation of [0]

class SegmentationTable:
	"""
	Segmentation Table implementation

	Attributes:
		entries: each entry points to pagin table
	"""

	def __init__(self, st_size=512):
		self.st_size = st_size
		self.entries = [0]*self.st_size

class VirtualMemory():
	"""
	Virtual Memory (VM)) impolementation.
	
	Attributes:
		st: segmentation table
		pt: paging table
	"""
	def __init__(self):
		self.vm = [0]*512
