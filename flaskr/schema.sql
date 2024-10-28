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
    release_type ENUM('EP', 'Demo', 'LP', 'Split'),
    FOREIGN KEY (band_id) REFERENCES band(id)
)

--releases can have many tracks
CREATE TABLE tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    length INTEGER NOT NULL,
    name TEXT NOT NULL,
    lyrics TEXT,
    FOREIGN KEY (release_id) REFERENCES releases(id)
)

--users can create many reviews
--releases can have many reviews
--WHAT FOR? (link to what is reviewed)
--WHO BY? (link to who did the reviewing)
--metadata -> score / review text / ?anything else?
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL,
    review_text TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (release_id) REFERENCES releases(id)
)

--metal archives stores modifications by user so TBD