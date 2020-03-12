GRANT ALL PRIVILEGES ON TABLE user TO dbcarpool;
DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
	"first_name" VARCHAR NOT NULL,
	"last_name" VARCHAR NOT NULL,
	"email" VARCHAR PRIMARY KEY,
	"password" VARCHAR NOT NULL,
	"joined_on" TIMESTAMP
);