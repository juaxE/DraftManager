CREATE TABLE "users" (
  "id" integer PRIMARY KEY,
  "username" varchar(20),
  "password" text,
  "team_id" integer UNIQUE,
  "admin" boolean,
  "created_at" timestamp
);

CREATE TABLE "teams" (
  "id" integer PRIMARY KEY,
  "name" varchar(60),
  "created_at" timestamp
);

CREATE TABLE "players" (
  "id" integer PRIMARY KEY,
  "name" varchar(100),
  "role" char(2),
  "drafted" boolean,
  "created_at" timestamp,
  "created_by" integer
);

CREATE TABLE "user_players" (
  "user_id" integer,
  "player_id" integer,
  "list_order" integer,
  "id" integer PRIMARY KEY,
  "created_at" timestamp
);

CREATE TABLE "draft_picks" (
  "id" integer PRIMARY KEY,
  "team_id" integer,
  "player_id" integer,
  "created_at" timestamp
);

CREATE TABLE "draft_configuration" (
  "id" integer PRIMARY KEY,
  "name" varchar(100),
  "participants" smallint,
  "rounds" smallint,
  "isSnake" boolean,
  "created_at" timestamp
);

ALTER TABLE "user_players" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "user_players" ADD FOREIGN KEY ("player_id") REFERENCES "players" ("id");

ALTER TABLE "draft_picks" ADD FOREIGN KEY ("team_id") REFERENCES "teams" ("id");

ALTER TABLE "draft_picks" ADD FOREIGN KEY ("player_id") REFERENCES "players" ("id");

ALTER TABLE "players" ADD FOREIGN KEY ("created_by") REFERENCES "users" ("id");

ALTER TABLE "teams" ADD FOREIGN KEY ("id") REFERENCES "users" ("team_id");
