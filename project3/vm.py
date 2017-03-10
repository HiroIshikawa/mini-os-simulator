# data structures

# the PM 1024 frames * 512 words / frame = 524,288 integers
# initialize fixed sized array of 524,288 integers with the value of 0
pm = [0]*524288

PM_FRAME_SIZE = 512
PM_NUM_FRAME = 1024

PM_FRAME_PER_ST = 1
PM_FRAME_PER_PT = 2
PM_FRAME_PER_PAGE = 1

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
		print 'bitmap:'
		for e in self.bitmap:
			print '{0:032b}'.format(e),

