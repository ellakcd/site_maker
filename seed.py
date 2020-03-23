"""Utility file to seed database"""

from sqlalchemy import func
from model import User, Play, Film, Training, Reading, Video, Photo, Miscphoto, Headshot, Review, Award, Filmaward, Interview, Colorscheme, Customcolorscheme, Page, Agency, Agent, Union, UserUnion

from model import connect_to_db, db 
from server import app
from sqlalchemy.inspection import inspect



def load_users():
	"""Load users from seed data into database"""

	#create data
	with open("seed_data/users.txt") as users:
		for row in users:
			user = row.rstrip().split("|")

			has_domain = True if user[1] == "True" else False

			kwargs = dict(
			user_id = user[0],
			has_domain = has_domain, 
			domain = user[2],
			name = user[3],
			email = user[4],
			password = user[5],
			bio = user[6],
			photo = user[7], 
			imdb = user[8], 
			current_link = user[9], 
			color_scheme_id=user[10], 
			background_image=user[11]
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			user = User(**kwargs)
			
			#add data
			db.session.add(user)
	#commit
	db.session.commit()


def load_plays():
	"""Load plays from seed data into database"""

	with open("seed_data/plays.txt") as plays: 
		for row in plays: 
			play = row.rstrip().split("|")

			hidden = True if play[11] == "True" else False

			kwargs = dict(
			play_id = play[0],
			user_id = play[1],
			resume_order = play[2], 
			review_order = play[3],
			title = play[4],
			playwright = play[5],
			character = play[6],
			theater = play[7],
			director = play[8],
			link = play[9], 
			category = play[10], 
			hidden = hidden 
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			play = Play(**kwargs)

			db.session.add(play)

	db.session.commit()


def load_films():
	"""Load films from seed data into database"""

	with open("seed_data/films.txt") as films: 
		for row in films: 
			film = row.rstrip().split("|")

			hidden = True if film[10] == "True" else False

			kwargs = dict(
			film_id = film[0],
			user_id = film[1],
			resume_order = film[2],
			review_order = film[3],
			title = film[4],
			specifier = film[5],
			character = film[6], 
			producer = film[7],
			director = film[8],
			link = film[9],
			hidden = hidden 
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			film = Film(**kwargs)

			db.session.add(film)

	db.session.commit()


def load_trainings():
	"""Load trainings from seed data into database"""

	with open("seed_data/trainings.txt") as trainings: 
		for row in trainings: 
			training = row.rstrip().split("|")

			hidden = True if training[3] == "True" else False

			kwargs = dict(
			training_id = training[0],
			user_id = training[1],
			training = training[2],
			hidden = hidden 
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			training = Training(**kwargs)

			db.session.add(training)

	db.session.commit()


def load_readings():
	"""Load readings from seed data into database"""

	with open("seed_data/readings.txt") as readings: 
		for row in readings: 
			reading = row.rstrip().split("|")

			hidden = True if reading[3] == "True" else False

			kwargs = dict(
			reading_id = reading[0],
			user_id = reading[1],
			reading = reading[2],
			hidden = hidden 
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			reading = Reading(**kwargs)

			db.session.add(reading)

	db.session.commit()


def load_videos():
	"""Load videos from seed data into database"""

	with open("seed_data/videos.txt") as videos: 
		for row in videos: 
			video = row.rstrip().split("|")

			youtube = True if video[4] == "True" else False
			hidden = True if video[5] == "True" else False

			kwargs = dict(
			video_id = video[0],
			user_id = video[1],
			video = video[2],
			category = video[3], 
			youtube = youtube, 
			hidden = hidden 
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			video = Video(**kwargs)

			db.session.add(video)

	db.session.commit()


def load_photos():
	"""Load photos from seed data into database"""

	with open("seed_data/photos.txt") as photos: 
		for row in photos: 
			photo = row.rstrip().split("|")

			hidden = True if photo[6] == "True" else False

			kwargs = dict(
			photo_id = photo[0],
			user_id = photo[1], 
			play_id = photo[2], 
			order = photo[3],
			film_id = photo[4],
			photo = photo[5], 
			hidden = hidden 
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			photo = Photo(**kwargs)

			db.session.add(photo)

	db.session.commit()


def load_misc_photos():
	"""Load misc photos from seed data into database"""

	with open("seed_data/misc_photos.txt") as misc_photos: 
		for row in misc_photos: 
			misc_photo = row.rstrip().split("|")

			hidden = True if misc_photo[4] == "True" else False

			kwargs = dict(
			misc_photo_id = misc_photo[0],
			user_id = misc_photo[1], 
			order = misc_photo[2],
			misc_photo = misc_photo[3], 
			hidden = hidden
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			misc_photo = Miscphoto(**kwargs)

			db.session.add(misc_photo)

	db.session.commit()


def load_headshots():
	"""Load headshots from seed data into database"""

	with open("seed_data/headshots.txt") as headshots: 
		for row in headshots: 
			headshot = row.rstrip().split("|")

			hidden = True if headshot[4] == "True" else False

			kwargs = dict(
			headshot_id = headshot[0],
			user_id = headshot[1], 
			order = headshot[2],
			headshot = headshot[3], 
			hidden = hidden
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			headshot = Headshot(**kwargs)

			db.session.add(headshot)

	db.session.commit()


def load_reviews():
	"""Load reviews from seed data into database"""

	with open("seed_data/reviews.txt") as reviews: 
		for row in reviews: 
			review = row.rstrip().split("|")

			hidden = True if review[9] == "True" else False

			kwargs = dict(
			review_id = review[0],
			user_id = review[1], 
			play_id = review[2], 
			photo_id= review[3],
			order=review[4],
			content = review[5],
			publication = review[6],
			writer = review[7],
			link = review[8], 
			hidden = hidden 
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			review = Review(**kwargs)

			db.session.add(review)

	db.session.commit()


def load_awards():
	"""Load awards from seed data into database"""

	with open("seed_data/awards.txt") as awards: 
		for row in awards: 
			award = row.rstrip().split("|")

			hidden = True if award[6] == "True" else False

			kwargs = dict(
			award_id = award[0],
			user_id = award[1], 
			play_id = award[2], 
			award = award[3],
			winner_or_nominee = award[4],
			category = award[5], 
			hidden = hidden 
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			award = Award(**kwargs)

			db.session.add(award)

	db.session.commit()


def load_film_awards():
	"""Load film awards from seed data into database"""

	with open("seed_data/film_awards.txt") as film_awards: 
		for row in film_awards: 
			film_award = row.rstrip().split("|")

			hidden = True if film_award[6] == "True" else False

			kwargs = dict(
			film_award_id = film_award[0],
			user_id = film_award[1], 
			film_id = film_award[2], 
			film_award = film_award[3],
			winner_or_nominee = film_award[4],
			category = film_award[5], 
			hidden = hidden
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			film_award = Filmaward(**kwargs)

			db.session.add(film_award)

	db.session.commit()


def load_interviews():
	"""Load interviews from seed data into database"""

	with open("seed_data/interviews.txt") as interviews: 
		for row in interviews: 
			interview = row.rstrip().split("|")

			hidden = True if interview[4] == "True" else False

			kwargs = dict(
			interview_id = interview[0],
			user_id = interview[1], 
			link = interview[2], 
			photo = interview[3], 
			hidden = hidden
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			interview = Interview(**kwargs)

			db.session.add(interview)

	db.session.commit()


def load_color_schemes():
	"""Load color_schemes from seed data into database"""

	with open("seed_data/color_schemes.txt") as color_schemes: 
		for row in color_schemes: 
			color_scheme = row.rstrip().split("|")

			kwargs = dict(
			color_scheme_id = color_scheme[0],
			color_name = color_scheme[1],
			color_one = color_scheme[2], 
			color_two = color_scheme[3], 
			color_three = color_scheme[4], 
			color_four = color_scheme[5], 
			color_five = color_scheme[6], 
			color_six = color_scheme[7]
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			color_scheme = Colorscheme(**kwargs)

			db.session.add(color_scheme)

	db.session.commit()


def load_custom_color_schemes():
	"""Load color_schemes from seed data into database"""

	with open("seed_data/custom_color_schemes.txt") as custom_color_schemes: 
		for row in custom_color_schemes: 
			custom_color_scheme = row.rstrip().split("|")

			kwargs = dict(
			custom_color_scheme_id = custom_color_scheme[0],
			user_id = custom_color_scheme[1],
			custom_name = custom_color_scheme[2],
			color_one = custom_color_scheme[3], 
			color_two = custom_color_scheme[4], 
			color_three = custom_color_scheme[5], 
			color_four = custom_color_scheme[6]
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			custom_color_scheme = Customcolorscheme(**kwargs)

			db.session.add(custom_color_scheme)

	db.session.commit()


def load_pages():
	"""Load pages from seed data into database"""

	with open("seed_data/pages.txt") as pages: 
		for row in pages: 
			page = row.rstrip().split("|")

			hidden = True if page[3] == "True" else False

			kwargs = dict(
			page_id = page[0],
			user_id = page[1],
			page = page[2], 
			hidden = hidden 
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			page = Page(**kwargs)

			db.session.add(page)

	db.session.commit()


def load_agencies():
	"""Load agencies from seed data into database"""

	with open("seed_data/agencies.txt") as agencies: 
		for row in agencies: 
			agency = row.rstrip().split("|")

			hidden = True if agency[3] == "True" else False

			kwargs = dict(
			agency_id = agency[0],
			user_id = agency[1],
			agency = agency[2], 
			hidden = hidden 
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			agency = Agency(**kwargs)

			db.session.add(agency)

	db.session.commit()


def load_agents():
	"""Load agents from seed data into database"""

	with open("seed_data/agents.txt") as agents: 
		for row in agents: 
			agent = row.rstrip().split("|")

			hidden = True if agent[6] == "True" else False

			kwargs = dict(
			agent_id = agent[0],
			user_id = agent[1],
			agency_id = agent[2],
			agent = agent[3], 
			email = agent[4], 
			phone = agent[5],
			hidden = hidden 
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			agent = Agent(**kwargs)

			db.session.add(agent)

	db.session.commit()


def load_unions():
	"""Load unions from seed data into database"""

	with open("seed_data/unions.txt") as unions: 
		for row in unions: 
			union = row.rstrip().split("|")

			kwargs = dict(
			union_id = union[0],
			union = union[1]
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			union = Union(**kwargs)

			db.session.add(union)

	db.session.commit()


def load_user_unions():
	"""Load unions from seed data into database"""

	with open("seed_data/user_unions.txt") as user_unions: 
		for row in user_unions: 
			user_union = row.rstrip().split("|")

			kwargs = dict(
			user_union_id = user_union[0],
			user_id = user_union[1],
			union_id = user_union[0]
			)

			keys_to_remove = []

			for key in kwargs.keys(): 
				if kwargs[key] == "":
					keys_to_remove.append(key)

			for key in keys_to_remove:
				del kwargs[key]

			user_union = UserUnion(**kwargs)

			db.session.add(user_union)

	db.session.commit()

"""
A non-class-specific way to update postgresql's autoincrementing primary key
sequences, useful for running after data including primary key values has been
seeded.

Similar to set_val_user_id() from Ratings, but works on all classes in
model.py.

Author: Katie Byers

"""


def update_pkey_seqs():
    """Set primary key for each table to start at one higher than the current
    highest key. Helps when data has been manually seeded."""

    # get a dictionary of {classname: class} for all classes in model.py
    model_classes = db.Model._decl_class_registry

    # loop over the classes
    for class_name in model_classes:

        # the dictionary will include a helper class we don't care about, so
        # skip it
        if class_name == "_sa_module_registry":
            continue

        # get the class itself out of the dictionary
        cls = model_classes[class_name]

        # get the name of the table associated with the class and its primary
        # key
        table_name = cls.__tablename__
        pkey_column = inspect(cls).primary_key[0]
        primary_key = pkey_column.name
        
        # check to see if the primary key is an integer (which are
        # autoincrementing by default)
        # if it isn't, skip to the next class
        if (not isinstance(pkey_column.type, db.Integer) or
            pkey_column.autoincrement is not True):
            continue

        # now we know we're dealing with an autoincrementing key, so get the
        # highest id value currently in the table
        result = db.session.query(func.max(getattr(cls, primary_key))).first()

        # if the table is empty, result will be none; only proceed if it's not
        # (we have to index at 0 since the result comes back as a tuple)
        if result[0]:
            # cast the result to an int
            max_id = int(result[0])

            # set the next value to be max + 1
            query = ("SELECT setval('" + table_name + "_" + primary_key +
                     "_seq', :new_id)")
            db.session.execute(query, {'new_id': max_id + 1})
            db.session.commit()


def init_models():
	connect_to_db(app)
	db.create_all()
	load_color_schemes()
	load_custom_color_schemes()
	load_users()
	load_plays()
	load_films()
	load_trainings()
	load_readings()
	load_videos()
	load_photos()
	load_misc_photos()
	load_headshots()
	load_reviews()
	load_awards()
	load_film_awards()
	load_interviews()
	load_pages()
	load_agencies()
	load_agents()
	load_unions()
	load_user_unions()
	update_pkey_seqs()


if __name__ == "__main__":
	init_models()
