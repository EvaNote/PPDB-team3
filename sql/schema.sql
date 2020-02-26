DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
	"first_name" VARCHAR NOT NULL,
	"last_name" VARCHAR NOT NULL,
	"email" VARCHAR PRIMARY KEY,
	"password" VARCHAR NOT NULL,
	"joined_on" TIMESTAMP
);

-- TODO create trigger for adding joined_on
INSERT INTO "user" VALUES ('Arno', 'Troch', 'arnotroch@login.com', 'arnotroch', now());
INSERT INTO "user" VALUES ('Eva', 'Note', 'evanote@login.com', 'evanote', now());
INSERT INTO "user" VALUES ('Jana', 'Osstyn', 'janaosstyn@login.com', 'janaosstyn', now());
INSERT INTO "user" VALUES ('John', 'Castillo', 'johncastillo@login.com', 'johncastillo', now());
INSERT INTO "user" VALUES ('Robbe', 'Lauwers', 'robbelauwers@login.com', 'robbelauwers', now());



