DROP TABLE IF EXISTS band;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS releases;
DROP TABLE IF EXISTS tracks;
DROP TABLE IF EXISTS reviews;

CREATE TABLE band (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    band_picture TEXT
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

--bands can have many releases
--can have a track listing but not required...
--release art
CREATE TABLE releases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    name TEXT NOT NULL,
    art TEXT,
  	release_type TEXT CHECK(release_type IN ('EP', 'Demo', 'LP', 'Split')) NOT NULL DEFAULT 'LP',
  	band_id INTEGER,
    FOREIGN KEY (band_id) REFERENCES band(id)
);

--releases can have many tracks
CREATE TABLE tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    length INTEGER NOT NULL,
    name TEXT NOT NULL,
    lyrics TEXT,
  	release_id INTEGER,
    FOREIGN KEY (release_id) REFERENCES releases(id)
);

--users can create many reviews
--releases can have many reviews
--WHAT FOR? (link to what is reviewed)
--WHO BY? (link to who did the reviewing)
--metadata -> score / review text / ?anything else?
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL,
    review_text TEXT,
  	user_id INTEGER,
  	release_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (release_id) REFERENCES releases(id)
);

--metal archives stores modifications by user so TBD

--TEST DATA
insert into band (name, status, band_picture) values ('cool band', 'active', 'band_pic_location');
insert into user (username, password) values ('awesomeuser', 'testpass');

insert into releases (year, name, art, release_type, band_id) values (1997, 'release 1', 'art_location', 'LP', 1);
insert into releases (year, name, art, release_type, band_id) values (2000, 'release 2', 'art_location', 'EP', 1);
insert into releases (year, name, art, release_type, band_id) values (2001, 'release 3', 'art_location', 'LP', 1);

insert into reviews (score, review_text, user_id, release_id) values (3, 'cool yay', 1, 1);
insert into reviews (score, review_text, user_id, release_id) values (8, 'cool yay 2', 1, 1);
insert into reviews (score, review_text, user_id, release_id) values (11, 'cool yay 3', 1, 1);
insert into reviews (score, review_text, user_id, release_id) values (111, 'cool yay 4', 1, 2);
insert into reviews (score, review_text, user_id, release_id) values (10, 'cool yay 5', 1, 2);
insert into reviews (score, review_text, user_id, release_id) values (1, 'cool yay 6', 1, 2);
insert into reviews (score, review_text, user_id, release_id) values (2, 'cool yay 7', 1, 2);
insert into reviews (score, review_text, user_id, release_id) values (11, 'cool yay 8', 1, 3);