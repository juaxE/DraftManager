CREATE TABLE "teams" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(60) UNIQUE,
  "created_at" timestamp
);

CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "username" varchar(20) UNIQUE,
  "password" text,
  "team_id" integer UNIQUE REFERENCES teams,
  "admin" boolean,
  "created_at" timestamp
);

CREATE TABLE "players" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(100),
  "role" char(2),
  "iss" smallint,
  "drafted" boolean,
  "created_at" timestamp,
  "created_by" integer REFERENCES users
);

CREATE TABLE "user_players" (
  "id" SERIAL PRIMARY KEY,
  "user_id" integer REFERENCES users,
  "player_id" integer REFERENCES players,
  "list_order" smallint,  
  "created_at" timestamp
);

CREATE TABLE "draft_picks" (
  "id" SERIAL PRIMARY KEY,
  "order" smallint,
  "team_id" integer REFERENCES teams,
  "player_id" integer REFERENCES players,
  "created_at" timestamp
);

CREATE TABLE "draft_configuration" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(100),
  "participants" smallint,
  "rounds" smallint,
  "isSnake" boolean,
  "created_at" timestamp
);