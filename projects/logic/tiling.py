import ast
from collections import Counter

class TileFragment:
	"""A fragment of a square tile"""

	def __init__(self, width, height):
		self.width = width
		self.height = height

	def rotate(self):
		return TileFragment(self.height, self.width)

	def length(self):
		return min(self.width, self.height)

	def __eq__(self, other):
		if isinstance(other, TileFragment):
			return self.width == other.width and self.height == other.height
		return False

	def __hash__(self):
		"""
		Cantor's pairing function
		"""
		return hash((self.width, self.height))

	def __repr__(self):
		return "{} x {} fragment".format(self.width, self.height)

def total_length(tilefrag_list):
	"""Given list of TileFragment objects, returns total length"""
	return sum([frag.length() for frag in tilefrag_list])

def get_key(tilefrag_list):
	"""Returns a key for sorting lists of tile fragments"""
	return (total_length(tilefrag_list), len(tilefrag_list))

def subset(list1, list2):
	"""
	Returns True if list1 is a subset of list2 (counting duplicate elements
	as different)
	"""
	return all(list1.count(item) <= list2.count(item) for item in list1)

def get_tiles(width, height, side_length):

	# First the easy bit: calculate how many tiles can be placed whole
	whole_rows, rem_height = divmod(height, side_length)
	whole_cols, rem_width = divmod(width, side_length)
	whole_rows, whole_cols = int(whole_rows), int(whole_cols)
	whole_tiles = whole_cols * whole_rows

	# If there's no space on the floor left over, we're done

	if rem_width == rem_height == 0:
		return whole_tiles, []

	# Now we create collections of the tile fragments left over

	frags_dict = {
		# Fragments on the bottom side of the floor
		TileFragment(side_length, rem_height): (
			whole_cols if (rem_height != 0) else 0),
		# Fragments on the right-hand side of the floor
		TileFragment(rem_width, side_length): (
			whole_rows if (rem_width != 0) else 0),
		# Fragment in the bottom-right corner of the floor
		TileFragment(rem_width, rem_height): (
			1 if (rem_height != 0 != rem_width) else 0)
	}

	remaining_fragments = list(Counter(frags_dict).elements())

	# Figuring out combinations

	combinations = []

	width_multiple = (int(side_length // rem_width) 
		if (rem_width != 0) 
		else 0)
	height_multiple = (int(side_length // rem_height) 
		if (rem_height != 0) 
		else 0)
	for w in range(0, width_multiple + 1):
		for h in range(0, height_multiple + 1):
			for c in range(0, 2):
				combination = list(Counter({
					TileFragment(rem_width, side_length): w,
					TileFragment(side_length, rem_height): h,
					TileFragment(rem_width, rem_height): c
				}).elements())
				# If current combination fits inside a tile, add it to list
				if 0 < total_length(combination) <= side_length:
					combinations.append(combination)

	# Rank combinations, according to the following order:
	# If A has greater total length than B, then A > B
	# Otherwise, if A has a greater number of fragments than B, then A > B
	combinations.sort(key=get_key, reverse=True)

	extra_tiles = []
	current = 0 # index of combinations list

	# Now we remove fragments from remaining_fragments, according to the 
	# combinations of fragments listed in combinations
	while len(remaining_fragments) != 0:
		# if currently selected combination is not a sub-multiset of remaining
		# tile frags:
		if not subset(combinations[current], remaining_fragments):
			current += 1
		else:
			rem_frags_counter = (
				Counter(remaining_fragments) - Counter(combinations[current]))
			remaining_fragments = list(rem_frags_counter.elements())
			extra_tiles.append(combinations[current])

	# Finally, we count and calculate cost

	total_tiles = whole_tiles + len(extra_tiles)
	return total_tiles, extra_tiles

def cut_tiles(side_length, extra_tiles):
	# First, we normalise the tile fragments so that the long side is
	# always the width, and the side length is 100. We also put the
	# corner fragment first.
	normal_tiles = []
	for tile in extra_tiles:
		normal_tile = []
		for frag in tile:
			w, h = frag.width, frag.height
			if w < h:
				w, h = h, w
			w = 100 * (w / side_length)
			h = 100 * (h / side_length)
			normal_tile.append(TileFragment(w, h))
		normal_tile.sort(key=(lambda x: max(x.width, x.height)))
		normal_tiles.append(normal_tile)
	result = []
	for tile in normal_tiles:
		tile_data = []
		y = 0
		for frag in tile:
			frag_data = {
				'x':0, 'y':y, 'width':frag.width, 'height':frag.height}
			tile_data.append(frag_data)
			y += frag.height
		result.append(tile_data)
	return result

def birds_eye(side_length, width, height):
	"""
	Returns the data required to draw the bird's eye view of the tiled floor,
	in the following format:
	[
		{
			'width':(width for this particular collection of tiles),
			'height'
			'class':(either whole, for a whole tile, or fragment)
			'positions': [
				{ 'x' 'y'},
				...
			]
		},
		...
	]
	"""

	# First, we normalise so that the width is 700px
	norm = lambda x: x * 700 / width
	side_length, width, height = norm(side_length), norm(width), norm(height)

	whole_rows, rem_height = divmod(height, side_length)
	whole_cols, rem_width = divmod(width, side_length)
	whole_rows, whole_cols = int(whole_rows), int(whole_cols)

	result = []

	# We add the list item for the whole tiles.

	whole_tiles_data = {
		'width': side_length,
		'height': side_length,
		'class': 'whole',
		'positions': []
	}

	for x in range(whole_cols):
		for y in range(whole_rows):
			whole_tiles_data['positions'].append({
				'x': x * side_length,
				'y': y * side_length
			})

	result.append(whole_tiles_data)

	# Now we add the fragments to the right.

	whole_section_width = whole_cols * side_length

	if whole_section_width < width:
		right_fragments_data = {
			'width': width - whole_section_width,
			'height': side_length,
			'class': 'fragment',
			'positions': []
		}

		for y in range(whole_rows):
			right_fragments_data['positions'].append({
				'x': whole_section_width,
				'y': y * side_length
			})

		result.append(right_fragments_data)

	# Now the same but for the fragments on the bottom.

	whole_section_height = whole_rows * side_length

	if whole_section_height < height:
		bottom_fragments_data = {
			'width': side_length,
			'height': height - whole_section_height,
			'class': 'fragment',
			'positions': []
		}

		for x in range(whole_cols):
			bottom_fragments_data['positions'].append({
				'x': x * side_length,
				'y': whole_section_height
				})

		result.append(bottom_fragments_data)

	# Finally we add the corner piece

	if whole_section_height < height and whole_section_width < width:
		corner_fragment_data = {
			'width': width - whole_section_width,
			'height': height - whole_section_height,
			'class': 'fragment',
			'positions': [{
				'x': whole_section_width,
				'y': whole_section_height
			}]
		}

		result.append(corner_fragment_data)

	return result
