
-- for errors ...
ALTER SEQUENCE docs01_id_seq RESTART WITH 1;
ALTER SEQUENCE invert01_id_seq RESTART WITH 1;
ALTER SEQUENCE docs02_id_seq RESTART WITH 1;
ALTER SEQUENCE invert02_id_seq RESTART WITH 1;

DELETE FROM docs01;
DELETE FROM invert01;
DELETE FROM docs02;
DELETE FROM invert02;


-- Building an Inverted Index using SQL
DROP TABLE docs01;
CREATE TABLE docs01 (id SERIAL, doc TEXT, PRIMARY KEY(id));

DROP TABLE invert01;
CREATE TABLE invert01 (
  keyword TEXT,
  doc_id INTEGER REFERENCES docs01(id) ON DELETE CASCADE
);

INSERT INTO docs01 (doc) VALUES
('error Debugging is the process of finding the cause of the error in your code'),
('When you are debugging a program and especially if you are working on a hard bug'),
('there are four things to try'),
('what you meant to say'),
('if you display the right thing at the right place in the program'),
('the problem becomes obvious but sometimes you have to spend some'),
('time to build scaffolding'),
('semantic What information can you get from the error messages or'),
('from the output of the program What kind of error could cause the'),
('problem youre seeing What did you change last before the problem');

SELECT * FROM docs01;

-- Break the document column into one row per word + primary key
SELECT id, s.keyword AS keyword
FROM docs01 AS D, unnest(string_to_array(lower(D.doc), ' ')) s(keyword)
ORDER BY id;

-- Discard duplicate rows
SELECT DISTINCT id, s.keyword AS keyword
FROM docs01 AS D, unnest(string_to_array(lower(D.doc), ' ')) s(keyword)
ORDER BY id;


-- Insert the keyword / primary key rows into a table
INSERT INTO invert01 (doc_id, keyword)
SELECT DISTINCT id, s.keyword AS keyword
FROM docs01 AS D, unnest(string_to_array(lower(D.doc), ' ')) s(keyword)
ORDER BY id;

SELECT keyword, doc_id FROM invert01 ORDER BY keyword, doc_id LIMIT 10;

------------------------------------------------------------------------------------------------------------------------------------------

-- Building an Inverted Index using SQL with stem word
DROP TABLE docs02;
CREATE TABLE docs02 (id SERIAL, doc TEXT, PRIMARY KEY(id));

DROP TABLE invert02;
CREATE TABLE invert02 (
  keyword TEXT,
  doc_id INTEGER REFERENCES docs02(id) ON DELETE CASCADE
);

INSERT INTO docs02 (doc) VALUES
('error Debugging is the process of finding the cause of the error in your code'),
('When you are debugging a program and especially if you are working on a hard bug'),
('there are four things to try'),
('what you meant to say'),
('if you display the right thing at the right place in the program'),
('the problem becomes obvious but sometimes you have to spend some'),
('time to build scaffolding'),
('semantic What information can you get from the error messages or'),
('from the output of the program What kind of error could cause the'),
('problem youre seeing What did you change last before the problem');

SELECT * FROM docs02 LIMIT 10;

-- Break the document column into one row per word + primary key
SELECT DISTINCT id, s.keyword AS keyword
FROM docs02 AS D, unnest(string_to_array(D.doc, ' ')) s(keyword)
ORDER BY id LIMIT 10;

-- Lower case it all
SELECT DISTINCT id, s.keyword AS keyword
FROM docs02 AS D, unnest(string_to_array(lower(D.doc), ' ')) s(keyword)
ORDER BY id LIMIT 10;

-- for errors
ALTER SEQUENCE stop_words_id_seq RESTART WITH 1;
DELETE FROM stop_words;
DROP TABLE stop_words;

CREATE TABLE stop_words (word TEXT unique);
INSERT INTO stop_words (word) VALUES 
('i'), ('a'), ('about'), ('an'), ('are'), ('as'), ('at'), ('be'), 
('by'), ('com'), ('for'), ('from'), ('how'), ('in'), ('is'), ('it'), ('of'), 
('on'), ('or'), ('that'), ('the'), ('this'), ('to'), ('was'), ('what'), 
('when'), ('where'), ('who'), ('will'), ('with');


-- All we do is throw out the words in the stop word list
SELECT DISTINCT id, s.keyword AS keyword
FROM docs02 AS D, unnest(string_to_array(lower(D.doc), ' ')) s(keyword)
WHERE s.keyword NOT IN (SELECT word FROM stop_words)
ORDER BY id LIMIT 10;

-- Put the stop-word free list into the GIN
INSERT INTO invert02 (doc_id, keyword)
SELECT DISTINCT id, s.keyword AS keyword
FROM docs02 AS D, unnest(string_to_array(lower(D.doc), ' ')) s(keyword)
WHERE s.keyword NOT IN (SELECT word FROM stop_words)
ORDER BY id;

SELECT keyword, doc_id FROM invert02 ORDER BY keyword, doc_id LIMIT 10;
