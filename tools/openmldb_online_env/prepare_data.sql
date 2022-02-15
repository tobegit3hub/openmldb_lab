CREATE DATABASE db1;
USE db1;

CREATE TABLE user (id int, name string, age int, gender string);
INSERT INTO user VALUES (1, "Venus", 18, "female");
INSERT INTO user VALUES (2, "Diana", 28, "female");
INSERT INTO user VALUES (3, "Apollo", 19, "male");
INSERT INTO user VALUES (4, "Mars", 20, "male");
INSERT INTO user VALUES (5, "Minerva", 25, "female");
INSERT INTO user VALUES (6, "Juno", 40, "female");
INSERT INTO user VALUES (7, "Neptunus", 29, "male");
INSERT INTO user VALUES (8, "Jupiter", 41, "male");

CREATE TABLE score (uid int, score float);
INSERT INTO score VALUES (1, 85.0);
INSERT INTO score VALUES (2, 80.5);
INSERT INTO score VALUES (3, 90.0);
INSERT INTO score VALUES (4, 91.5);
INSERT INTO score VALUES (5, 95.0);
INSERT INTO score VALUES (6, 99.0);
INSERT INTO score VALUES (7, 92.0);
INSERT INTO score VALUES (8, 99.9);

CREATE DATABASE db2;
USE db2;

CREATE TABLE t1 (c1 string, c2 int, c3 bigint, c4 float, c5 double, c6 timestamp, c7 date);
INSERT INTO t1 VALUES ("aa", 13, 22, 3.2, 13.3, 1636097490000, "2021-05-20");
INSERT INTO t1 VALUES ("bb", 16, 22, 6.2, 16.3, 1636097790000, "2021-05-20");
INSERT INTO t1 VALUES ("cc", 17, 22, 7.2, 17.3, 1636097890000, "2021-05-26");
