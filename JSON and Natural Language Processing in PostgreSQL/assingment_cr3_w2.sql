
-- String Array GIN Index ...

-- for errors ...
ALTER SEQUENCE docs03_id_seq RESTART WITH 1;
DELETE FROM docs03;
DROP TABLE docs03 cascade;
DROP index array03;

-- 
CREATE TABLE docs03 (id SERIAL, doc TEXT, PRIMARY KEY(id));
CREATE INDEX array03 ON docs03 USING gin(string_to_array(lower(doc), ' ')  array_ops);

INSERT INTO docs03 (doc) VALUES
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

INSERT INTO docs03 (doc) SELECT 'Neon ' || generate_series(10000,20000);

-- wait until Bitmap Index Scan ...
EXPLAIN SELECT id, doc FROM docs03 WHERE '{information}' <@ string_to_array(lower(doc), ' ');

SELECT id, doc FROM docs03 WHERE '{information}' <@ string_to_array(lower(doc), ' ');
EXPLAIN SELECT id, doc FROM docs03 WHERE '{information}' <@ string_to_array(lower(doc), ' ');


-------------------------------------------------------------------------------------------------------------------------------------------

-- for errors ...
ALTER SEQUENCE docs03_id_seq RESTART WITH 1;
DELETE FROM docs03 cascade;
DROP TABLE docs03 cascade;
DROP index fulltext03;


CREATE TABLE docs03 (id SERIAL, doc TEXT, PRIMARY KEY(id));
CREATE INDEX fulltext03 ON docs03 USING gin(to_tsvector('english', doc));

INSERT INTO docs03 (doc) VALUES
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

INSERT INTO docs03 (doc) SELECT 'Neon ' || generate_series(10000,20000);

-- wait until Bitmap Index Scan ...
EXPLAIN SELECT id, doc FROM docs03 WHERE to_tsquery('english', 'instructions') @@ to_tsvector('english', doc);

SELECT id, doc FROM docs03 WHERE to_tsquery('english', 'information') @@ to_tsvector('english', doc);
EXPLAIN SELECT id, doc FROM docs03 WHERE to_tsquery('english', 'information') @@ to_tsvector('english', doc);