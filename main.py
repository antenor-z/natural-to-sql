import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = """
Given the following tables
```
CREATE TABLE movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT,
    genre_id INT,
    director_id INT,
    budget FLOAT,
    revenue FLOAT,
    description TEXT,
    rating DECIMAL(3,1),
    runtime_minutes INT,
    poster_url VARCHAR(255),
    trailer_url VARCHAR(255),
);

CREATE TABLE genres (
    genre_id INT PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL,
    description TEXT,
);

CREATE TABLE directors (
    director_id INT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    birth_date DATE,
    nationality VARCHAR(50),
);

ALTER TABLE movies ADD CONSTRAINT fk_genre_id FOREIGN KEY (genre_id) REFERENCES genres(genre_id);
ALTER TABLE movies ADD CONSTRAINT fk_director_id FOREIGN KEY (director_id) REFERENCES directors(director_id);

CREATE TABLE actors (
    actor_id INT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    birth_date DATE,
    nationality VARCHAR(50),
);

CREATE TABLE movies_actors (
    movie_id INT,
    actor_id INT,
    PRIMARY KEY (movie_id, actor_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
);
```

You convert a question in English about movies to an SQL query considering the tables given above.

Rules:
  - If the question isn't about movies, return 'FAIL'.
  - If the question cant be converted to SQL considering the tables above, return 'FAIL'.
  - You return only the query without delimiters.
  - You don't give an explanation about the query.
"""

question = input(">> ")
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": MODEL},
        {"role": "user", "content": "What movie did Tom Cruise participate in 1997?"},
        {"role": "assistant", "content": """SELECT m.title
FROM movies m
INNER JOIN movies_actors ma ON m.movie_id = ma.movie_id
INNER JOIN actors a ON ma.actor_id = a.actor_id
WHERE a.name = 'Tom Cruise' AND m.release_year = 1997;"""},
        
        {"role": "user", "content": "What is the square root of 100?"},
        {"role": "assistant", "content": "FAIL"},

        {"role": "user", "content": "What is the best action movie?"},
        {"role": "assistant", "content": "FAIL"},

        {"role": "user", "content": "Who's the lead star in Oppenheimer?"},
        {"role": "assistant", "content": """SELECT a.name
FROM movies m
INNER JOIN actors a ON m.actor_id = a.actor_id
WHERE m.title = 'Oppenheimer';"""},

        {"role": "user", "content": question}
    ]
)

print(response['choices'][0]['message']['content'])
