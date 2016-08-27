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

def cut_tiles(side_length, extra_tiles, digs):
	# First, we normalise the tile fragments so that the long side is
	# always the width, and the side length is 100. We also put the
	# corner fragment first.
	sorted_tiles = []
	norm = lambda x: 100 * (x / side_length)
	for tile in extra_tiles:
		sorted_tile = []
		for frag in tile:
			w, h = round(frag.width, digs), round(frag.height, digs)
			if w < h:
				w, h = h, w
			sorted_tile.append(TileFragment(w, h))
		sorted_tile.sort(key=(lambda x: x.width + x.height))
		sorted_tiles.append(sorted_tile)
	result = []
	for tile in sorted_tiles:
		tile_data = []
		y = 0
		for frag in tile:
			frag_data = {
				'x':0, 'y':y, 
				'width':norm(frag.width), 'height':norm(frag.height),
				'data_width': frag.width, 'data_height': frag.height, 
				'class':'look'}
			tile_data.append(frag_data)
			y += norm(frag.height)
		result.append(tile_data)
	return result

def birds_eye(side_length, width, height, digs):
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
	whole_rows, rem_height = divmod(height, side_length)
	whole_cols, rem_width = divmod(width, side_length)

	# Check for floating point errors
	if round(rem_height, digs) == round(side_length, digs):
		rem_height = 0
		whole_rows += 1
	if round(rem_width, digs) == round(side_length, digs):
		rem_width = 0
		whole_cols += 1
	whole_rows, whole_cols = int(whole_rows), int(whole_cols)

	# Normalise so that width is 700px
	normalise = lambda x: x * 700 / width
	norm = {
		'rem_height':normalise(rem_height),
		'rem_width': normalise(rem_width),
		'side_length': normalise(side_length),
		'width': normalise(width),
		'height': normalise(height)
	}
	
	result = []

	# We add the list item for the whole tiles.

	whole_tiles_data = {
		'width': norm['side_length'],
		'height': norm['side_length'],
		'class': 'whole',
		'positions': []
	}

	for x in range(whole_cols):
		for y in range(whole_rows):
			whole_tiles_data['positions'].append({
				'x': x * norm['side_length'],
				'y': y * norm['side_length']
			})

	result.append(whole_tiles_data)

	# Now we add the fragments to the right.

	whole_sec_width = whole_cols * side_length
	norm['whole_sec_width'] = normalise(whole_sec_width)

	if norm['whole_sec_width'] < norm['width']:
		right_fragments_data = {
			'width': norm['width'] - norm['whole_sec_width'],
			'height': norm['side_length'],
			'data_width': round(width - whole_sec_width, digs),
			'data_height': side_length,
			'class': 'fragment look',
			'positions': []
		}

		for y in range(whole_rows):
			right_fragments_data['positions'].append({
				'x': norm['whole_sec_width'],
				'y': y * norm['side_length']
			})

		result.append(right_fragments_data)

	# Now the same but for the fragments on the bottom.

	whole_sec_height = whole_rows * side_length
	norm['whole_sec_height'] = normalise(whole_sec_height)

	if norm['whole_sec_height'] < norm['height']:
		bottom_fragments_data = {
			'width': norm['side_length'],
			'height': norm['height'] - norm['whole_sec_height'],
			'data_width': side_length,
			'data_height': round(height - whole_sec_height, digs),
			'class': 'fragment look',
			'positions': []
		}

		for x in range(whole_cols):
			bottom_fragments_data['positions'].append({
				'x': x * norm['side_length'],
				'y': norm['whole_sec_height']
				})

		result.append(bottom_fragments_data)

	# Finally we add the corner piece

	if (norm['whole_sec_height'] < norm['height'] and 
		norm['whole_sec_width'] < norm['width']):
		corner_fragment_data = {
			'width': norm['width'] - norm['whole_sec_width'],
			'height': norm['height'] - norm['whole_sec_height'],
			'data_width': round(width - whole_sec_width, digs),
			'data_height': round(height - whole_sec_height, digs),
			'class': 'fragment look',
			'positions': [{
				'x': norm['whole_sec_width'],
				'y': norm['whole_sec_height']
			}]
		}

		result.append(corner_fragment_data)

	return result
