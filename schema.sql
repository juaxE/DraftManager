CREATE TABLE "teams" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(60) UNIQUE,
  "position" smallint(50) UNIQUE,
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
  "iss" smallint UNIQUE,
  "name" varchar(100),
  "role" char(2),  
  "drafted" boolean DEFAULT FALSE,
  "created_at" timestamp,
);

CREATE TABLE "user_players" (
  "id" SERIAL PRIMARY KEY,
  "user_id" integer REFERENCES users ON DELETE CASCADE,
  "player_id" integer REFERENCES players ON DELETE CASCADE,
  "list_order" smallint,  
  "created_at" timestamp
);

CREATE TABLE "draft_picks" (
  "id" SERIAL PRIMARY KEY,
  "pickorder" smallint UNIQUE,
  "team_id" integer REFERENCES teams ON DELETE CASCADE,
  "player_id" integer REFERENCES players ON DELETE CASCADE,
  "created_at" timestamp
);

CREATE TABLE "draft_configuration" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(100),
  "participants" smallint(50),
  "rounds" smallint(40),
  "snake" boolean,
  "confirmed" boolean,
  "created_at" timestamp
);