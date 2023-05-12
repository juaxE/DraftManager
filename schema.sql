CREATE TABLE "teams" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(60) UNIQUE,
  "position" smallint UNIQUE,
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
  "created_at" timestamp
);

CREATE TABLE "user_players" (
  "id" SERIAL PRIMARY KEY,
  "user_id" integer REFERENCES users ON DELETE CASCADE,
  "player_id" integer REFERENCES players ON DELETE CASCADE,
  "list_order" smallint CHECK (list_order <=100),  
  "created_at" timestamp,
  UNIQUE ("user_id", "list_order")
);

CREATE TABLE "draft_picks" (
  "id" SERIAL PRIMARY KEY,
  "pickorder" smallint UNIQUE CHECK (pickorder <=2000),
  "team_id" integer REFERENCES teams ON DELETE CASCADE,
  "player_id" integer REFERENCES players,
  "created_at" timestamp
);

CREATE TABLE "draft_configuration" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar(40),
  "participants" smallint CHECK (participants <=50),
  "rounds" smallint CHECK(rounds <= 40),
  "snake" boolean,
  "confirmed" boolean,
  "created_at" timestamp
);