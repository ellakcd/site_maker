"""Models and database functions for RooMatch"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""Model definitions"""


class User(db.Model):
	"""Users of acting site"""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	has_domain = db.Column(db.Boolean, nullable=True, default=False)
	domain = db.Column(db.String(100), nullable=True)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(100), nullable=False)
	bio = db.Column(db.String(100), nullable=True)
	photo = db.Column(db.String(100), nullable=False)
	imdb = db.Column(db.String(150), nullable=True)
	current_link = db.Column(db.String(150), nullable=True)
	color_scheme_id = db.Column(db.Integer, db.ForeignKey("color_schemes.color_scheme_id"), nullable=False)
	background_image = db.Column(db.String(150), nullable=True)

	color_scheme = db.relationship("Colorscheme", backref="users")

	unions = db.relationship("Union", 
                                secondary="user_unions")


	def __repr__(self):
		"""helper"""

		return "<User name={} user_id={}> user_email={}>".format(self.name, self.user_id, self.email)


class Play(db.Model):
	"""Plays on acting site"""

	__tablename__ = "plays"

	play_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	resume_order = db.Column(db.Integer, nullable=True)
	review_order = db.Column(db.Integer, nullable=True)
	title = db.Column(db.String(100), nullable=False)
	playwright = db.Column(db.String(100), nullable=True)
	character = db.Column(db.String(100), nullable=False)
	theater = db.Column(db.String(100), nullable=False)
	director = db.Column(db.String(100), nullable=True)
	link = db.Column(db.String(500), nullable=True)
	category = db.Column(db.String(500), nullable=True)
	hidden = db.Column(db.Boolean, nullable=True, default=False)
	
	user = db.relationship("User", backref="plays")


class Film(db.Model):
	"""TV and Film on acting site"""

	__tablename__ = "films"

	film_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	resume_order = db.Column(db.Integer, nullable=True)
	review_order = db.Column(db.Integer, nullable=True)
	title = db.Column(db.String(100), nullable=False)
	specifier = db.Column(db.String(100), nullable=True)
	character = db.Column(db.String(100), nullable=False)
	producer = db.Column(db.String(100), nullable=True)
	director = db.Column(db.String(100), nullable=True)
	link = db.Column(db.String(500), nullable=True)
	hidden = db.Column(db.Boolean, nullable=True, default=False)
	
	user = db.relationship("User", backref="films")


class Training(db.Model):
	"""Training on acting site"""

	__tablename__ = "trainings"

	training_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	training = db.Column(db.String(100), nullable=False)
	hidden = db.Column(db.Boolean, nullable=True, default=False)
	
	user = db.relationship("User", backref="trainings")


class Reading(db.Model):
	"""Readings on acting site"""

	__tablename__ = "readings"

	reading_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	reading = db.Column(db.String(100), nullable=False)
	hidden = db.Column(db.Boolean, nullable=True, default=False)
	
	user = db.relationship("User", backref="readings")


class Video(db.Model):
	"""Videos on acting site"""

	__tablename__ = "videos"

	video_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	video = db.Column(db.String(100), nullable=False)
	category = db.Column(db.String(100), nullable=False)
	youtube = db.Column(db.Boolean, nullable=True, default=False)
	hidden = db.Column(db.Boolean, nullable=True, default=False)
	
	user = db.relationship("User", backref="videos")


class Photo(db.Model):
	"""Photos from shows on acting site"""

	__tablename__ = "photos"

	photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	play_id = db.Column(db.Integer, db.ForeignKey("plays.play_id"), nullable=True)
	order = db.Column(db.Integer, nullable=True)
	film_id = db.Column(db.Integer, db.ForeignKey("films.film_id"), nullable=True)
	photo = db.Column(db.String(200), nullable=False)
	hidden = db.Column(db.Boolean, nullable=True, default=False)
	
	user = db.relationship("User", backref="photos")
	play = db.relationship("Play", backref="photos")
	film = db.relationship("Film", backref="photos")


class Miscphoto(db.Model):
	"""Misc photos on acting site"""

	__tablename__ = "misc_photos"

	misc_photo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	order = db.Column(db.Integer, nullable=True)
	misc_photo = db.Column(db.String(200), nullable=False)
	hidden = db.Column(db.Boolean, nullable=True, default=False)
	
	user = db.relationship("User", backref="misc_photos")


class Headshot(db.Model):
	"""Headshots on acting site"""

	__tablename__ = "headshots"

	headshot_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	order = db.Column(db.Integer, nullable=True)
	headshot = db.Column(db.String(200), nullable=False)
	hidden = db.Column(db.Boolean, nullable=True, default=False)
	
	user = db.relationship("User", backref="headshots")


class Review(db.Model):
	"""Reviews from shows on acting site"""

	__tablename__ = "reviews"

	review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	play_id = db.Column(db.Integer, db.ForeignKey("plays.play_id"), nullable=True)
	photo_id = db.Column(db.Integer, db.ForeignKey("photos.photo_id"), nullable=False)
	order = db.Column(db.Integer, nullable=True)
	content = db.Column(db.String(1000), nullable=False)
	publication = db.Column(db.String(100), nullable=True)
	writer = db.Column(db.String(100), nullable=True)
	link = db.Column(db.String(1000), nullable=True)
	hidden = db.Column(db.Boolean, nullable=True, default=False)

	user = db.relationship("User", backref="reviews")
	play = db.relationship("Play", backref="reviews")
	photo = db.relationship("Photo", backref="reviews")


class Award(db.Model):
	"""Awards from shows on acting site"""

	__tablename__ = "awards"

	award_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	play_id = db.Column(db.Integer, db.ForeignKey("plays.play_id"), nullable=True)
	award = db.Column(db.String(1000), nullable=False)
	winner_or_nominee = db.Column(db.String(1000), nullable=False)
	category = db.Column(db.String(1000), nullable=False)
	hidden = db.Column(db.Boolean, nullable=True, default=False)

	user = db.relationship("User", backref="awards")
	play = db.relationship("Play", backref="awards")


class Filmaward(db.Model):
	"""Awards from films on acting site"""

	__tablename__ = "film_awards"

	film_award_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	film_id = db.Column(db.Integer, db.ForeignKey("films.film_id"), nullable=True)
	film_award = db.Column(db.String(1000), nullable=False)
	winner_or_nominee = db.Column(db.String(1000), nullable=False)
	category = db.Column(db.String(1000), nullable=False)
	hidden = db.Column(db.Boolean, nullable=True, default=False)

	user = db.relationship("User", backref="film_awards")
	film = db.relationship("Film", backref="film_awards")


class Interview(db.Model):
	"""Interviews on acting site"""

	__tablename__ = "interviews"

	interview_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	link = db.Column(db.String(500), nullable=False)
	photo = db.Column(db.String(100), nullable=False)
	hidden = db.Column(db.Boolean, nullable=True, default=False)

	user = db.relationship("User", backref="interviews")


# class Colors(db.Model):
# 	"""Colors on acting site"""

# 	__tablename__ = "colors"

# 	color_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
# 	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
# 	color = db.Column(db.String(100), nullable=False)

# 	user = db.relationship("User", backref="colors")

class Colorscheme(db.Model):
	"""Color schemes on acting site"""

	__tablename__ = "color_schemes"

	color_scheme_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	color_name = db.Column(db.String(100), nullable=False)
	color_one = db.Column(db.String(100), nullable=False)
	color_two = db.Column(db.String(100), nullable=False)
	color_three = db.Column(db.String(100), nullable=False)
	color_four = db.Column(db.String(100), nullable=False)
	color_five = db.Column(db.String(100), nullable=False)
	color_six = db.Column(db.String(100), nullable=False)


class Customcolorscheme(db.Model):
	"""Color schemes on acting site"""

	__tablename__ = "custom_color_schemes"

	custom_color_scheme_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	custom_name = db.Column(db.String(100), nullable=False)
	color_one = db.Column(db.String(100), nullable=False)
	color_two = db.Column(db.String(100), nullable=False)
	color_three = db.Column(db.String(100), nullable=False)
	color_four = db.Column(db.String(100), nullable=False)

	user = db.relationship("User", backref="customcolorschemes")


class Page(db.Model):
	"""Pages to display on acting site"""

	__tablename__ = "pages"

	page_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	page = db.Column(db.String(100), nullable=False)
	hidden = db.Column(db.Boolean, nullable=True, default=False)

	user = db.relationship("User", backref="pages")


class Agency(db.Model):
	"""Agencies on acting site"""

	__tablename__ = "agencies"

	agency_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	agency = db.Column(db.String(100), nullable=False)
	hidden = db.Column(db.Boolean, nullable=True, default=False)

	user = db.relationship("User", backref="agencies")
	

class Agent(db.Model):

	__tablename__ = "agents"

	agent_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
	agency_id = db.Column(db.Integer, db.ForeignKey("agencies.agency_id"), nullable=False)
	agent = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=True)
	phone = db.Column(db.String(100), nullable=True)
	hidden = db.Column(db.Boolean, nullable=True, default=False)

	agency = db.relationship("Agency", backref="agents")
	user = db.relationship("User", backref="agents")


class Union(db.Model):

	__tablename__ = "unions"

	union_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	union = db.Column(db.String(100), nullable=False)


class UserUnion(db.Model):
    """Users and unions on acting site"""

    __tablename__ = "user_unions"

    user_union_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    union_id = db.Column(db.Integer, db.ForeignKey("unions.union_id"), nullable=False)




# Helper Functions

def connect_to_db(app):
    """Connect the database to our Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///site_maker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print ("Connected to DB.")