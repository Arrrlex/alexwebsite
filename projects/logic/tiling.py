import ast
import collections

class TileFragmentCollection:

	# A tile fragments collection consists of the fragments of tile that are 
	# needed to complete the tiling of the floor

	def __init__(self, righttiles_length, righttiles_number, 
			bottomtiles_length, bottomtiles_number):
		self.righttiles_length = righttiles_length
		self.righttiles_number = righttiles_number
		self.bottomtiles_length = bottomtiles_length
		self.bottomtiles_number = bottomtiles_number

	def __str__(self):
		"""
		returns a string of the form
		{ righttiles_length: righttiles_number, 
			bottomtiles_length: bottomtiles_number}
		if righttiles_length and bottomtiles_length are different, and 
		{ righttiles_length: self.count() }
		if they're the same.

		This is useful, as performing ast.literal_eval will turn it into a
		dictionary mapping length of fragment to number of instances of 
		fragment.
		"""
		if self.righttiles_length == self.bottomtiles_length:
			return "{{ {0}: {1} }}".format(self.righttiles_length, self.count())
		else:
			return "{{ {0}: {1}, {2}: {3} }}".format(
				self.righttiles_length, self.righttiles_number, 
				self.bottomtiles_length, self.bottomtiles_number)

	def length(self):
		"""
		returns the total 'length' of tile in this collection of fragments.
		"""
		return (self.righttiles_number * self.righttiles_length + 
			self.bottomtiles_number * self.bottomtiles_length)

	def count(self):
		"""
		returns the total number of fragments in this collection
		"""
		return self.righttiles_number + self.bottomtiles_number

	def __gt__(self, coll2):
		"""
		Used for ordering TileFragmentCollections in order to use the most 
		useful ones first
		"""
		if self.length() != coll2.length():
			return self.length() > coll2.length()
		if self.righttiles_length != 0 and self.bottomtiles_length != 0 and (
				coll2.righttiles_length == 0 or 
				coll2.bottomtiles_length == 0):
			return True
		if (self.righttiles_number ==0 or self.bottomtiles_number == 0) and (
				coll2.bottomtiles_number != 0 and coll2.bottomtiles_number != 0):
			return False
		return self.count() > coll2.count()

def get_tiles(width, height, side_length):
	"""
	Given the width and height of a rectangular floor, and the side length of 
	the square tiles to be laid on the floor, calculates how many tiles will 
	need to be bought to cover the floor.
	"""

	# First the easy bit: calculate how many tiles can be placed whole

	whole_rows, rem_height = divmod(height, side_length)
	whole_cols, rem_width = divmod(width, side_length)

	whole_tiles = whole_cols * whole_rows

	# Now we specify exactly what tile fragments we need.

	tile_fragments = TileFragmentCollection(
		rem_width, whole_rows, 
		rem_height, whole_cols)

	# Add the corner piece - for our purposes, we can treat it as another side 
	# piece (the small rectangle we're adding on here would only be wasted 
	# anyway)
	if tile_fragments.righttiles_length > tile_fragments.bottomtiles_length:
		tile_fragments.bottomtiles_number += 1
	else:
		tile_fragments.righttiles_number += 1

	# Next we get a list of combinations of our tile fragments that fit inside a
	# tile

	combinations = []

	# width_multiple and height_multiple are the maximum number of width-type 
	# and height-type tile fragments we can fit in a single tile, respectively.
	width_multiple = side_length // tile_fragments.righttiles_length
	height_multiple = side_length // tile_fragments.bottomtiles_length

	for w in range(0, width_multiple + 1):
		for h in range(0, height_multiple + 1):
			frag_coll = TileFragmentCollection(rem_width, w, rem_height, h)
			if 0 < frag_coll.length() <= side_length:
				combinations.append(frag_coll)

	# Sort the list, greatest first

	combinations.sort(reverse=True)

	# Now, we "fill in" the tile fragments in the combinations given above

	extra_tiles = []
	current = 0 # index of combinations list

	while tile_fragments.count() != 0:
		# check if we can use currently selected combination
		if (combinations[current].bottomtiles_number > tile_fragments.bottomtiles_number or 
				combinations[current].righttiles_number > tile_fragments.righttiles_number):
			current += 1
		else:
			tile_fragments.righttiles_number -= combinations[current].righttiles_number
			tile_fragments.bottomtiles_number -= combinations[current].bottomtiles_number
			extra_tiles.append(combinations[current])


	# Finally, we count and calculate cost

	total_tiles = whole_tiles + len(extra_tiles)
	return total_tiles, whole_rows, whole_cols, extra_tiles, rem_width, rem_height

def birds_eye(whole_rows, whole_cols, side_length, rem_width, rem_height, width, height):
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

	result = []

	# First, we add the list item for the whole tiles.

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

def cut_tiles(side_length, extra_tiles):
	"""
	Returns the data required to draw the tiles to be cut up, in the following
	format:
	[
		{
			'num': (number of such tiles),
			'fragments': [
				{
					'x': (assumed to be 0 if omitted),
					'y'
					'width': (assumed to be side_length if omitted)
					'height'
					'class': (if 'discard' marked as for discarding)
				},
				...
			]
		},
		...

	]
	"""
	result = []

	# Because we treated the corner piece as just any old piece in get_tiles,
	# we now have to pick one piece with a shorter height and designate it
	# the corner piece. 
	# We choose the first piece we come across with the right height

	if len(extra_tiles) != 0:
		tile = extra_tiles[0]
		small_height, width = (
			min(tile.righttiles_length, tile.bottomtiles_length), 
			max(tile.righttiles_length, tile.bottomtiles_length))
	# We add a flag to ensure only one piece is turned into a corner piece
	done_corner_piece = False

	# extra_tiles_dict is a dictionary mapping TileFragmentCollection strings
	# to the number of times that type of tile occurs in extra_tiles.

	extra_tiles_dict = dict(collections.Counter(map(str, extra_tiles)))
	for tile in extra_tiles_dict.keys():
		tile_item = {
			'num': extra_tiles_dict[tile],
			'fragments': []
		}
		# tile_dict maps the .._length to the .._number attributes of the tile
		tile_dict = ast.literal_eval(tile)
		y = 0
		for (height, count) in tile_dict.items():
			for num in range(1, count+1):
				tile_item['fragments'].append({
					'y':y,
					'height':height
				})
				if height == small_height and not done_corner_piece:
					tile_item['fragments'][-1]['width'] = width
					tile_item['fragments'].append({
						'y':y,
						'x':width,
						'height':height,
						'width': side_length - width,
						'class':'discard'
					})
					done_corner_piece = True
				y += height
		if y < side_length:
			tile_item['fragments'].append({
				'y':y,
				'height':side_length - y,
				'class': 'discard'
			})
		result.append(tile_item)
	return result
