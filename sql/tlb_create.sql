CREATE TABLE User(
       username VARCHAR(20),
       firstname VARCHAR(20),
       lastname VARCHAR(20),
       password VARCHAR(40),
       email VARCHAR(40),
       PRIMARY KEY (username)
);

CREATE TABLE Album (
       albumid int AUTO_INCREMENT,
       title varchar(50),
       created date,
       lastupdated date,
       username varchar(20),
       FOREIGN KEY (username) REFERENCES User(username) ON DELETE CASCADE,
       PRIMARY KEY (albumid)
);


CREATE TABLE Photo (
       picid varchar(40),
       url varchar(255),
       format char(3),
       date date,
       PRIMARY KEY (picid)
);

CREATE TABLE Contain (
       albumid int,
       picid varchar(40),
       caption varchar(255),
       sequencenum int,
       FOREIGN KEY (albumid) REFERENCES Album(albumid) ON DELETE CASCADE ,
       FOREIGN KEY (picid) REFERENCES Photo(picid) ON DELETE CASCADE,
       PRIMARY KEY (albumid, picid),
       KEY (sequencenum)
);

DELIMITER $$
CREATE TRIGGER test_trigger
AFTER INSERT ON Contain
FOR EACH ROW BEGIN
    UPDATE Album
       SET Album.lastupdated=CURDATE()
     WHERE Album.albumid=NEW.albumid;
END;$$
DELIMITER ;



DELIMITER $$
CREATE TRIGGER delete_trigger
AFTER DELETE ON Contain
FOR EACH ROW BEGIN
    UPDATE Album
       SET Album.lastupdated=CURDATE()
     WHERE Album.albumid=OLD.albumid;
END;$$
DELIMITER ;
