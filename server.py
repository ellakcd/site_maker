"""Greeting Flask app."""

from random import choice
from model import connect_to_db, db 
from model import User, Play, Photo, Headshot, Miscphoto, Review, Award, Film, Video, Interview, Reading, Training, Colorscheme, Customcolorscheme, Page, Agency, Agent, Union, UserUnion
from flask import (Flask, render_template, flash, session, request, redirect, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
import functions
import smtplib
import sys
from flask_mail import Mail, Message
import os
import urls
import json



# "__name__" is a special Python variable for the name of the current module
# Flask wants to know this to know what any imported things are relative to.
app = Flask(__name__)
# Also expose "app" as "application" for gunicorn.
application = app
app.secret_key = "Super Secret"
# app.jinja_env.undefined = StrictUndefined

MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


app.config.update(dict(
  MAIL_SERVER = 'smtp.gmail.com',
  MAIL_PORT = 587, 
  MAIL_USERNAME = 'ellaactingsite@gmail.com',
  MAIL_PASSWORD = MAIL_PASSWORD, 
  # MAIL_USE_SSL = True, 
  MAIL_USE_TLS = True,
  MAIL_DEFAULT_SENDER = 'ellaactingsite@gmail.com',
))

# Initialize the database!!!
app.config.update(dict(
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql:///site_maker'),
  SQLALCHEMY_TRACK_MODIFICATIONS = False,
))
#db.app = app
db.init_app(app)


# Set up email support
mail = Mail(app)




#LANDING PAGES

@app.route("/")
def registration_page():
    """register new users"""

    colors = Colorscheme.query.all()

    return render_template("/registration.html", colors=colors)


@app.route("/<user_id>/")
def homepage(user_id):
    """Home page."""

    user = User.query.get(user_id)

    return render_template("homepage.html", user=user)


@app.route("/<user_id>/my_homepage")
def my_homepage(user_id):
    """Home page."""

    user = User.query.get(user_id)
    colors = Colorscheme.query.all()
    page_options = ["resume", "photos", "press", "videos", "contact"]
    all_unions = Union.query.all()
    pages = functions.getpages(user)
    user_unions = []
    for union in user.unions: 
      user_unions.append(union.union)

    if "current_user" in session and session["current_user"] == user.user_id: 
      return render_template("my_homepage.html", user=user, colors=colors, page_options=page_options, all_unions=all_unions, pages=pages, user_unions=user_unions)
    else: 
      return redirect("/{}/".format(user_id))


@app.route("/resume")
def display_resume():
    """shows current resume"""

    user = User.query.get(1)
    ordered_plays = Play.query.filter(Play.user_id == user.user_id).order_by(Play.resume_order)
    ordered_plays = [play for play in ordered_plays if not play.hidden]
    ordered_films = Film.query.filter(Film.user_id == user.user_id).order_by(Film.resume_order)
    ordered_films = [film for film in ordered_films if not film.hidden]
    categories = set()
    for play in user.plays: 
      categories.add(play.category) 
    print(categories)
    pages = functions.getpages(user)

    return render_template("resume.html", user=user, ordered_plays=ordered_plays, ordered_films = ordered_films, pages=pages)


@app.route("/my_resume")
def display_my_resume():
    """shows current resume"""

    user = User.query.get(1)
    ordered_plays = Play.query.filter(Play.user_id == user.user_id).order_by(Play.resume_order)
    ordered_films = Film.query.filter(Film.user_id == user.user_id).order_by(Film.resume_order)

    if "current_user" in session and session["current_user"] == user.user_id: 
      return render_template("my_resume.html", user=user, ordered_plays=ordered_plays, ordered_films=ordered_films)
    else: 
      return redirect("/resume")
   

@app.route("/photos")
def display_photos():
    """shows current photos"""

    user = User.query.get(1)
    # ordered_plays = Play.query.filter(Play.user_id == user.user_id).order_by(Play.resume_order)
    ordered_photos = Photo.query.filter(Photo.user_id == user.user_id).order_by(Photo.order)
    ordered_headshots = Headshot.query.filter(Headshot.user_id == user.user_id).order_by(Headshot.order)
    ordered_misc_photos = Miscphoto.query.filter(Miscphoto.misc_photo_id == user.user_id).order_by(Miscphoto.order)
    pages = functions.getpages(user)

    return render_template("photos.html", user=user, ordered_photos=ordered_photos, ordered_headshots=ordered_headshots, ordered_misc_photos=ordered_misc_photos, pages=pages)


@app.route("/my_photos")
def display_my_photos():
    """shows current photos"""

    user = User.query.get(1)
    # ordered_plays = Play.query.filter(Play.user_id == user.user_id).order_by(Play.resume_order)
    ordered_photos = Photo.query.filter(Photo.user_id == user.user_id).order_by(Photo.order)
    ordered_headshots = Headshot.query.filter(Headshot.user_id == user.user_id).order_by(Headshot.order)
    ordered_misc_photos = Miscphoto.query.filter(Miscphoto.user_id == user.user_id).order_by(Miscphoto.order)

    if "current_user" in session and session["current_user"] == user.user_id: 
      return render_template("my_photos.html", user=user, ordered_photos=ordered_photos, ordered_headshots=ordered_headshots, ordered_misc_photos=ordered_misc_photos)
    else:
      return redirect("/photos")


@app.route("/press")
def display_press():
    """shows current press"""

    user = User.query.get(1)
    ordered_plays = Play.query.filter(Play.user_id == user.user_id).order_by(Play.review_order)
    pages = functions.getpages(user)


    return render_template("press.html", user=user, ordered_plays=ordered_plays, pages=pages)


@app.route("/my_press")
def display_my_press():
    """shows current press"""

    print("in my press")
    user = User.query.get(1)
    ordered_plays = Play.query.filter(Play.user_id == user.user_id).order_by(Play.review_order).all()
    for play in ordered_plays:
      print(play.play_id, play.review_order)

    if "current_user" in session and session["current_user"] == user.user_id: 
      return render_template("my_press.html", user=user, ordered_plays=ordered_plays)
    else:
      return redirect("/press")



@app.route("/videos")
def display_video():
    """shows current video"""

    user = User.query.get(1)
    videos = user.videos
    videos = [video for video in videos if not video.hidden]
    interviews = [video for video in videos if video.category == "interview"]
    theater_clips = [video for video in videos if video.category == "theater"]
    film_clips = [video for video in videos if video.category == "film"]
    pages = functions.getpages(user)
  
    return render_template("videos.html", user=user, interviews=interviews, theater_clips=theater_clips, film_clips=film_clips, pages=pages)


@app.route("/my_videos")
def display_my_video():
    """shows current video"""

    user = User.query.get(1)
    videos = user.videos
    interviews = [video for video in videos if video.category == "interview"]
    theater_clips = [video for video in videos if video.category == "theater"]
    film_clips = [video for video in videos if video.category == "film"]
  
    if "current_user" in session and session["current_user"] == user.user_id: 
      return render_template("my_videos.html", user=user, interviews=interviews, theater_clips=theater_clips, film_clips=film_clips)
    else:
      return redirect("/videos")


@app.route("/contact")
def display_contact():
    """shows current contact info"""

    user = User.query.get(1)
    pages = functions.getpages(user)

    return render_template("contact.html", user=user, pages=pages)


@app.route("/my_contact")
def display_my_contact():
    """shows current contact info"""

    user = User.query.get(1)

    if "current_user" in session and session["current_user"] == user.user_id: 
      return render_template("my_contact.html", user=user)
    else: 
      return redirect("contact.html")



#REGISTRATION ROUTES

@app.route("/add_user", methods=['POST'])
def add_user():
      """add a new user"""

      name = request.form.get("name")
      email = request.form.get("email")
      password = request.form.get("password")
      bio = request.form.get("bio")
      photo = functions.save_photo("pic")
      imdb = request.form.get("imdb")
      current_link = request.form.get("current_link")
      color_scheme = request.form.get("color")

      print(name, email, password, bio, imdb, current_link, color_scheme)

      kwargs = dict(
      name = name,
      email = email,
      password = password,
      bio = bio,
      photo = photo, 
      imdb = imdb, 
      current_link = current_link, 
      color_scheme_id = color_scheme
     )

      print("test")
      print(kwargs)

      keys_to_remove = []

    #   for key in kwargs.keys(): 
    #     if kwargs[key] == "":
    #      keys_to_remove.append(key)

    #   for key in keys_to_remove:
    #     del kwargs[key]

    #   user = User(**kwargs)
      
    # #add data
    #   db.session.add(user)
    # #commit
    #   db.session.commit()

    #   user = User.query.filter(User.email == email).first()
    #   print (user)

    #   return redirect("/{}/my_homepage".format(user.user_id))
      return redirect("/")



#HOMEPAGE ROUTES


@app.route("/login", methods=['POST'])
def login():
    """Log In user"""

    try: 
        password = request.form.get("password")
        user = User.query.get(1)
        if password == user.password:
            session["current_user"] = user.user_id
            return redirect("/my_homepage")
    except: 
        return redirect("/")


@app.route("/logout")
def logout():
    """Log Out user."""

    user_id = session["current_user"]
    del session['current_user']

    return redirect("/")


@app.route("/update_color", methods=["POST"])
def update_color():
    """change site color"""

    user_id = session["current_user"]
    user = User.query.get(user_id)
    new_color = request.form.get("color")
    user.color_scheme_id = new_color
    db.session.commit()

    return redirect("/my_homepage")


@app.route("/make_custom_color_scheme", methods=["POST"])
def make_custom_color_scheme():

  user_id = session["current_user"]
  user = User.query.get(user_id)
  new_color = request.form.get("name")
  color_1 = request.form.get("color_1")
  color_2 = request.form.get("color_2")
  color_3 = request.form.get("color_3")
  color_4 = request.form.get("color_4")
  color_5 = "black"
  color_6 = "white"


  kwargs = dict(
    custom_name=new_color, 
    user_id=user_id, 
    color_one=color_1, 
    color_two=color_2, 
    color_three=color_3, 
    color_four=color_4, 
    color_five=color_5, 
    color_six=color_6
        )
      
  keys_to_remove = []
      
  for key in kwargs.keys(): 
      if kwargs[key] == "":
        keys_to_remove.append(key)
      for key in keys_to_remove:
        del kwargs[key]

  db.session.add(Customcolorscheme(**kwargs))
  db.session.commit()

  new_color = Customcolorscheme.query.filter_by(custom_name=new_color).first()
  user.color_scheme_id = new_color.color_scheme_id
  db.session.commit()

  return redirect("/my_homepage")


@app.route("/update_pages", methods=["POST"])
def update_pages():
  """change what pages to display"""

  user_id = session["current_user"]
  user = User.query.get(user_id)
  new_pages = request.form.getlist("pages")
  print(new_pages)
  Page.query.filter_by(user_id=user_id).delete()
  

  for page in new_pages: 
    kwargs = dict(
        user_id=user_id, 
        page=page
      )
    db.session.add(Page(**kwargs))
  db.session.commit()

  print(user.pages)

  return redirect("/my_homepage")


@app.route("/update_unions", methods=["POST"])
def update_unions(): 

  user_id = session["current_user"]
  user = User.query.get(user_id)
  new_unions = request.form.getlist("unions")
  print(new_unions)

  UserUnion.query.filter_by(user_id=user_id).delete()

  for union_id in new_unions:
    kwargs = dict(
        user_id=user_id, 
        union_id=union_id
      )
    db.session.add(UserUnion(**kwargs))
  db.session.commit()

  print(user.unions)

  return redirect("/my_homepage")


@app.route("/edit_homepage", methods=["POST"])
def edit_homepage(): 
  """edit homepage"""

  id_val = request.form.get("id")
  value = request.form.get("value")
  print("id", id_val, "value", value)

  attribute = id_val.split("_")[2]
  user_id = session["current_user"]
  user = User.query.get(user_id)
  if attribute=="name": 
    user.name = value
  elif attribute=="email":
    user.email = value
  elif attribute=="imdb":
    user.imdb = value
  elif attribute=="bio":
    user.bio = value
  elif attribute=="current":
    user.current_link = value

  db.session.commit()
  # print(attribute)
  # print(user.attribute)
  # user_id = session["current_user"]
  # user = User.query.get(user_id)
  print(user)
  # print(attribute)
  

  info = {
    "element_id": id_val, 
    "element_value": value
  }

  return jsonify(info)



#RESUME ROUTES

@app.route("/add_play", methods=["POST"])
def add_play(): 
    """add play info to database"""


    kwargs = dict(
        user_id = 1,
        title=request.form.get("title"),
        playwright=request.form.get("playwright"),
        character=request.form.get("character"),
        theater=request.form.get("theater"),
        director=request.form.get("director"),      
        link=request.form.get("link"),
    )

    keys_to_remove = []
    
    for key in kwargs.keys(): 
        if kwargs[key] == "":
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del kwargs[key]
    db.session.add(Play(**kwargs))
    db.session.commit()

    return redirect("/my_resume")


@app.route("/add_reading", methods=["POST"])
def add_reading(): 
    """add reading info to database"""

    kwargs = dict(
        user_id = 1,
        reading=request.form.get("reading")
    )

    keys_to_remove = []
    
    for key in kwargs.keys(): 
        if kwargs[key] == "":
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del kwargs[key]

    db.session.add(Reading(**kwargs))
    db.session.commit()

    return redirect("/my_resume")


@app.route("/add_training", methods=["POST"])
def add_training(): 
    """add training info to database"""

    kwargs = dict(
        user_id = 1,
        training=request.form.get("training")
    )

    keys_to_remove = []
    
    for key in kwargs.keys(): 
        if kwargs[key] == "":
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del kwargs[key]

    db.session.add(Training(**kwargs))
    db.session.commit()

    return redirect("/my_resume")


@app.route("/edit_resume", methods=["POST"])
def edit_resume(): 
  """edit resume"""

  id_val = request.form.get("id")
  value = request.form.get("value")
  # print("id", id_val, "value", value)

  project_type = id_val.split("_")[1]


  # attribute = id_val.split("_")[2]
  # project_id = id_val.split("_")[3]


  # user_id = session["current_user"]
  # user = User.query.get(user_id)
  # user.attribute = value

  # print(project_type)
  # print(project_type == "film")

  if project_type == "play": 
    functions.edit_play(id_val, value)

  if project_type == "film": 
    functions.edit_film(id_val, value)


  # play = Play.query.get(play_id)
  # # play.attribute = value
  # if attribute == "title":
  #   play.title = value
  # elif attribute == "playwright": 
  #   play.playwright = value
  # elif attribute == "character": 
  #   play.character = value
  # elif attribute == "theater":
  #   play.theater = value
  # elif attribute == "director": 
  #   play.director = value
  # db.session.commit()
  # print(attribute)
  # print(user.attribute)
  # user_id = session["current_user"]
  # user = User.query.get(user_id)
  # print(play)
  # print(attribute)
  # print(play.attribute)

  info = {
    "element_id": id_val, 
    "element_value": value
  }

  return jsonify(info)


#PHOTO ROUTES

@app.route("/add_photo", methods=["POST"])
def add_photo(): 
    """add photo to database"""

    
    category = request.form.get("category").split("|")
    photo = functions.save_photo("pic")

    print(category)
    print(category[0])
    print (category[0] == "play")

    if category[0] == "headshot":
        kwargs = dict(
          user_id=1, 
          headshot=photo
        )
      
        keys_to_remove = []
      
        for key in kwargs.keys(): 
            if kwargs[key] == "":
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del kwargs[key]

        db.session.add(Headshot(**kwargs))
        db.session.commit()
    elif category[0] == "misc":
        kwargs = dict(
          user_id=1, 
          misc_photo=photo
        )
      
        keys_to_remove = []
      
        for key in kwargs.keys(): 
            if kwargs[key] == "":
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del kwargs[key]

        db.session.add(Miscphoto(**kwargs))
        db.session.commit()
    elif category[0] == "play": 
        kwargs = dict(
          user_id=1,
          play_id=category[1], 
          photo=photo
        )

        keys_to_remove = []

        for key in kwargs.keys(): 
            if kwargs[key] == "":
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del kwargs[key]

        db.session.add(Photo(**kwargs))
        db.session.commit()
    elif category[0] == "film": 
        kwargs = dict(
          user_id=1,
          film_id=category[1], 
          photo=photo
        )

        keys_to_remove = []

        for key in kwargs.keys(): 
            if kwargs[key] == "":
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del kwargs[key]

        db.session.add(Photo(**kwargs))
        db.session.commit()

    return redirect("/my_photos")




#PRESS ROUTES

@app.route("/add_review", methods=["POST"])
def add_review(): 
    """add review to database"""

    
    play = request.form.get("title")
    photo = request.form.get("photo")
    # photo = functions.save_photo("photo")
    content = request.form.get("quote")
    publication = request.form.get("publication")
    writer = request.form.get("critic")
    link = request.form.get("link")

    
    kwargs = dict(
      user_id=1, 
      play_id=play, 
      photo_id=photo, 
      content=content, 
      publication=publication, 
      writer=writer, 
      link=link
      )
    
    db.session.add(Review(**kwargs))
    db.session.commit()

    user = User.query.get(1)
    for review in user.reviews:
      print(review.content)

    return redirect("/my_press")



#VIDEO ROUTES

@app.route("/add_video", methods=["POST"])
def add_video(): 
    """add video to database"""

    
    category = request.form.get("category")
    youtube = request.form.get("youtube")

    print(category)
    print(youtube)

    if youtube: 
      kwargs = dict(
        user_id=1, 
        video=youtube, 
        category=category, 
        youtube=True)

      db.session.add(Video(**kwargs))
      db.session.commit()
      print("added youtube")

    else: 
      video = functions.save_photo("video")
      print(video)

      kwargs = dict(
        user_id=1, 
        video=video, 
        category=category, 
        youtube=False)

      db.session.add(Video(**kwargs))
      db.session.commit()
      print("added vid")

    user = User.query.get(1)
    for vid in user.videos:
      print(vid.video, vid.category, vid.youtube)


    return redirect("/my_videos")


@app.route("/hide_video", methods=["POST"])
def hide_video():

  video_id = request.form.get("video_id")
  print(video_id)
  video = Video.query.get(video_id)
  print(video)
  video.hidden = True
  db.session.commit()

  return redirect("/my_videos")


@app.route("/show_video", methods=["POST"])
def show_video():

  video_id = request.form.get("video_id")
  print(video_id)
  video = Video.query.get(video_id)
  video.hidden = False
  print(video)
  db.session.commit()

  return redirect("/my_videos")


#CONTACT ROUTES

@app.route("/send_message", methods=["POST"])
def send_message():
    """Contact user of site"""

    user_id = request.form.get("user_id")
    user = User.query.get(user_id)
    sender_email = request.form.get("email")
    receiver = user.email
    sender_name = request.form.get("name")
    subject = request.form.get("subject")
    message = request.form.get("message")

    try:
        with mail.connect() as conn:
          msg = Message("{}".format(subject), recipients=["{}".format(receiver)])
          msg.html = "Name: {} <br> Email: {} <br><br><br><br> Message: {}".format(sender_name, sender_email, message)
          conn.send(msg)
        flash("Message Sent to {}!".format(user.name))
        return redirect("/contact")
    except Exception as e:
        # info = e if session["current_user"] == user_id else ""
        flash("Couldn't send message to {}; error: {}".format(user.name, str(e)))
        return redirect("/contact")



@app.route("/add_rep", methods=["POST"])
def add_rep():

  agency = request.form.get("agency")
  agent = request.form.get("agent")
  email = request.form.get("email")
  phone = request.form.get("phone")

  user_id = session["current_user"]
  user = User.query.get(user_id)

  user_agencies = [agency.agency for agency in user.agencies]
  print(user_agencies)
  print(agency)
  if agency not in user_agencies: 
    kwargs = dict(
      user_id = 1, 
      agency = agency
      )

    db.session.add(Agency(**kwargs))
    db.session.commit()
    print("agency added")

  agency_id = Agency.query.filter_by(agency=agency).first().agency_id
    
  kwargs = dict(
      user_id = 1, 
      agency_id = agency_id, 
      agent = agent, 
      email = email, 
      phone = phone
    )

  db.session.add(Agent(**kwargs))
  db.session.commit()

  return redirect("/my_contact")


@app.route("/hide_agent", methods=["POST"])
def hide_agent():

  agent_id = request.form.get("agent_id")
  print(agent_id)
  agent = Agent.query.get(agent_id)
  agent.hidden = True
  db.session.commit()

  return redirect("/my_contact")


@app.route("/show_agent", methods=["POST"])
def show_agent():

  agent_id = request.form.get("agent_id")
  print(agent_id)
  agent = Agent.query.get(agent_id)
  agent.hidden = False
  db.session.commit()

  return redirect("/my_contact")


#AJAX ROUTES

#HOMEPAGE

@app.route("/change_main_photo", methods=["POST"])
def change_main_photo():

  print("in function")
  photo = functions.save_photo("image")
  print("saved photo")
  user_id = session["current_user"]
  user = User.query.get(user_id)
  user.photo = photo
  db.session.commit()

  return redirect("/my_homepage")


#RESUME

@app.route("/save_play_order", methods=["POST"])
def save_play_order():

  new_order = request.form.get("order")
  counter = 1
  new_order = json.loads(new_order)
  
  for play_id in new_order:
      play = Play.query.get(play_id)
      play.resume_order = counter
      counter += 1

  db.session.commit()

  flash("saved new order")

  return redirect("/my_resume")


@app.route("/save_film_order", methods=["POST"])
def save_film_order():

  new_order = request.form.get("order")
  print(new_order)
  counter = 1
  new_order = json.loads(new_order)
  print(new_order)
  
  for film_id in new_order:
      film = Film.query.get(film_id)
      print(film)
      film.resume_order = counter
      counter += 1

  db.session.commit()


  user = User.query.get(1)
  for film in user.films: 
    print(film.resume_order)

  flash("saved new order")

  return redirect("/my_resume")


@app.route("/delete_project", methods=["POST"])
def delete_project():

  print("server")
  project_id = request.form.get("project_id")
  project_type = request.form.get("project_type")
  print(project_id, project_type)

  if project_type == "play": 
    play = Play.query.get(project_id)
    # for photo in play.photos: 
    #   photo.play_id = None
    # for review in play.reviews: 
    #   review.play_id = None
    play.hidden = True
    # db.session.commit()
    # Play.query.filter_by(play_id=project_id).delete()
  elif project_type == "film": 
    film = Film.query.get(project_id)
    film.hidden = True
    # for photo in film.photos: 
    #   photo.film_id = None
    #   db.session.commit()
    # Film.query.filter_by(film_id=project_id).delete()
  elif project_type == "reading": 
    reading = Reading.query.get(project_id)
    reading.hidden = True
  elif project_type == "training": 
    # Training.query.filter_by(training_id=project_id).delete()
    training = Training.query.get(project_id)
    training.hidden = True
  elif project_type == "award": 
    award = Award.query.get(project_id)
    award.hidden = True

  db.session.commit()

  return redirect("/my_resume")


@app.route("/include_project", methods=["POST"])
def include_project():

  print("server")
  project_id = request.form.get("project_id")
  project_type = request.form.get("project_type")
  print(project_id, project_type)

  if project_type == "play": 
    play = Play.query.get(project_id)
    # for photo in play.photos: 
    #   photo.play_id = None
    # for review in play.reviews: 
    #   review.play_id = None
    play.hidden = False
    # db.session.commit()
    # Play.query.filter_by(play_id=project_id).delete()
  elif project_type == "film": 
    film = Film.query.get(project_id)
    film.hidden = False
    # for photo in film.photos: 
    #   photo.film_id = None
    #   db.session.commit()
    # Film.query.filter_by(film_id=project_id).delete()
  elif project_type == "reading": 
    reading = Reading.query.get(project_id)
    reading.hidden = False
  elif project_type == "training": 
    # Training.query.filter_by(training_id=project_id).delete()
    training = Training.query.get(project_id)
    training.hidden = False
  elif project_type == "award": 
    award = Award.query.get(project_id)
    award.hidden = False

  db.session.commit()

  return redirect("/my_resume")

#PHOTOS

@app.route("/save_misc_photo_order", methods=["POST"])
def save_misc_photo_order():

  new_order = request.form.get("order")
  counter = 1
  new_order = json.loads(new_order)
  
  for misc_photo_id in new_order:
      misc_photo = Miscphoto.query.get(misc_photo_id)
      misc_photo.order = counter
      counter += 1

  db.session.commit()

  flash("saved new order")

  return redirect("/my_photos")


@app.route("/save_headshot_order", methods=["POST"])
def save_headshot_order():

  new_order = request.form.get("order")
  counter = 1
  new_order = json.loads(new_order)
  
  for headshot_id in new_order:
      headshot = Headshot.query.get(headshot_id)
      headshot.order = counter
      counter += 1

  db.session.commit()

  flash("saved new order")

  return redirect("/my_photos")


@app.route("/save_show_photo_order", methods=["POST"])
def save_show_photo_order():

  print("server")
  new_order = request.form.get("order")
  counter = 1
  new_order = json.loads(new_order)
  print(new_order)
  
  for photo_id in new_order:
      photo = Photo.query.get(photo_id)
      photo.order = counter
      counter += 1

  db.session.commit()

  flash("saved new order")

  return redirect("/my_photos")


@app.route("/delete_photo", methods=["POST"])
def delete_photo():

  photo_id = request.form.get("photo_id")
  photo_type = request.form.get("photo_type")

  if photo_type == "misc": 
    misc_photo = Miscphoto.query.get(photo_id)
    misc_photo.hidden = True
  elif photo_type == "headshot": 
    headshot = Headshot.query.get(photo_id)
    headshot.hidden = True
  elif photo_type == "production": 
    photo = Photo.query.get(photo_id)
    photo.hidden = True

  db.session.commit()

  return redirect("/my_photos")


@app.route("/include_photo", methods=["POST"])
def include_photo():

  photo_id = request.form.get("photo_id")
  photo_type = request.form.get("photo_type")

  if photo_type == "misc": 
    misc_photo = Miscphoto.query.get(photo_id)
    misc_photo.hidden = False
  elif photo_type == "headshot": 
    headshot = Headshot.query.get(photo_id)
    headshot.hidden = False
  elif photo_type == "production": 
    photo = Photo.query.get(photo_id)
    photo.hidden = False

  db.session.commit()

  return redirect("/my_photos")


@app.route("/make_main_photo", methods=["POST"])
def make_main_photo():

  print("server")
  photo_id = request.form.get("photo_id")
  # photo_type = request.form.get("photo_type")
  print(photo_id)

  user_id = session["current_user"]
  user = User.query.get(user_id)
  headshot = Headshot.query.get(photo_id)

  user.photo = headshot.headshot

  db.session.commit()

  return redirect("/my_homepage")

#PRESS

@app.route("/save_review_order", methods=["POST"])
def save_review_order():

  print("server")
  new_order = request.form.get("order")
  counter = 1
  new_order = json.loads(new_order)
  print(new_order)
  
  for play_id in new_order:
      play = Play.query.get(play_id)
      play.review_order = counter
      counter += 1

  db.session.commit()

  return redirect("/my_press")

#VIDEO

#CONTACT








if __name__ == "__main__":

    # app.debug = True
  app.jinja_env.auto_reload = app.debug
  app.config['TEMPLATES_AUTO_RELOAD'] = app.debug

  app.run(port=5001, host='0.0.0.0')
  # if len(sys.argv) > 1:
  #   port = sys.argv[1]
  # else:
  #   port = 5000
  # app.run(port=port)