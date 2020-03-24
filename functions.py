from model import connect_to_db, db 
from model import User, Play, Photo, Review, Interview, Film
from flask import (Flask, render_template, session, request, redirect)


UPLOAD_FOLDER = "static/uploaded_images/"



def save_photo(photo_name):
    """gets photo from form, saves to db, returns filepath"""

    photo_name = request.files["{}".format(photo_name)]
    photo_name_path = UPLOAD_FOLDER + photo_name.filename
    photo_name.save(photo_name_path)

    return "/{}".format(photo_name_path)


def login(user, password):
	print(user, password, user.password, user.user_id)
	print(password == user.password)

	try:
		if password == user.password:
			session["current_user"] = user.user_id
			return redirect("users/{}/my_homepage".format(user.user_id))
	except:
		return redirect("users/{}/homepage".format(user.user_id))


def getpages(user):

	pages = []
	for page in user.pages: 
		pages.append(page.page)

	return pages


def edit_play(id_val, value):

	attribute = id_val.split("_")[2]
	play_id = id_val.split("_")[3]
	play = Play.query.get(play_id)

	if attribute == "title":
		play.title = value
	elif attribute == "playwright":
		play.playwright = value
	elif attribute == "character":
		play.character = value
	elif attribute == "theater":
		play.theater = value
	elif attribute == "director":
		play.director = value

	db.session.commit()


def edit_film(id_val, value):

	print("infunction")

	attribute = id_val.split("_")[2]
	film_id = id_val.split("_")[3]
	film = Film.query.get(film_id)
	print(film.title)

	if attribute == "title":
		film.title = value
	elif attribute == "specifier":
		film.specifier = value
	elif attribute == "character":
		film.character = value
	elif attribute == "producer":
		film.producer = value
	elif attribute == "director":
		film.director = value

	db.session.commit()

	print(film.specifier)

# def add_headshot(headshot):
# 	"""Adds headshot to db"""

# 	kwargs = dict(
#         user_id=1,
#         headshot=headshot
#     )

#     for key in kwargs.keys():
#       if kwargs[key] == "":
#             del kwargs[key]
#     db.session.add(Headshot(**kwargs))
#     db.session.commit()


# def add_photo(photo, play):
# 	"""Adds play to db"""

# 	kwargs = dict(
#         user_id=1,
#         play_id=play, 
#         photo=photo
#     )

# 	for key in kwargs.keys():
#    	  if kwargs[key] == "":
#             del kwargs[key]
#     db.session.add(Photo(**kwargs))
#     db.session.commit()




