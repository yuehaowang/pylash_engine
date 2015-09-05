import sys

sys.path.insert(0, "../../")
from pylash.utils import stage
from pylash.display import Sprite, Bitmap, BitmapData

class Item(Sprite):
	# define ourselves events
	EVENT_ADD_SCORE = "event_add_score"
	EVENT_GAME_OVER = "event_game_over"

	def __init__(self, image):
		super(Item, self).__init__()
		
		bmp = Bitmap(BitmapData(image))
		self.addChild(bmp)

		self.index = 0
		self.y = -bmp.height / 2

	def loop(self):
		player = None

		if self.parent:
			player = self.parent.hitTarget

		if player is None:
			return

		# move down
		self.y += 5

		# check collision
		if (abs(self.x + self.width / 2 - player.x - player.width / 2) <= (self.width + player.width) / 2) and (abs(self.y + self.height / 2 - player.y - player.height / 2) <= (self.height + player.height) / 2):
			if self.index <= 3:
				# dispatch ourselves event that add score
				self.dispatchEvent(Item.EVENT_ADD_SCORE)

				self.remove()
			else:
				# dispatch ourselves event that enter game over
				self.dispatchEvent(Item.EVENT_GAME_OVER)

		# remove self when this item moves out of stage
		if self.y >= stage.height:
			self.remove()