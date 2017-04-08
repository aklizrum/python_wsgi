CREATE TABLE IF NOT EXISTS "region" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "city" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "region_id" INTEGER NOT NULL,
    "name" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "comment" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id" INTEGER NOT NULL,
    "text" TEXT
);
CREATE TABLE user (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "first_name" TEXT NOT NULL,
    "second_name" TEXT NOT NULL,
    "third_name" TEXT,
    "city" INTEGER,
    "contact_phone" TEXT,
    "email" TEXT
);

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
INSERT INTO "region" VALUES(1,'Хабаровский край');
INSERT INTO "region" VALUES(2,'Приморский край');
INSERT INTO "region" VALUES(3,'Амурская область');
INSERT INTO "city" VALUES(1,1,'Хабаровск');
INSERT INTO "city" VALUES(2,1,'Комсомольск-на-Амуре');
INSERT INTO "city" VALUES(3,1,'Николаевск-на-Амуре');
INSERT INTO "city" VALUES(4,2,'Владивосток');
INSERT INTO "city" VALUES(5,2,'Уссурийск');
INSERT INTO "city" VALUES(6,2,'Находка');
INSERT INTO "city" VALUES(7,3,'Благовещенск');
INSERT INTO "city" VALUES(8,3,'Белогорск');
INSERT INTO "city" VALUES(9,3,'Свободный');
INSERT INTO "comment" VALUES(1,7,'wYZSMEphIk');
INSERT INTO "comment" VALUES(2,7,'TP GPvjDZH');
INSERT INTO "comment" VALUES(3,7,'dsKzczTg N');
INSERT INTO "comment" VALUES(4,8,'YXLjWVXDcT');
INSERT INTO "comment" VALUES(5,8,'qdQOZEOkK');
INSERT INTO "comment" VALUES(9,9,'aqx Dln dN');
INSERT INTO "comment" VALUES(10,9,'pn CXys sz');
INSERT INTO "comment" VALUES(11,9,'GKTxH u');
INSERT INTO "comment" VALUES(12,9,'LSZhhdkil');
INSERT INTO "comment" VALUES(13,9,'lMZ OfsgEq');
INSERT INTO "comment" VALUES(14,9,'ADkD fNek');
INSERT INTO "comment" VALUES(15,9,'lIEEq LTwr');
INSERT INTO "comment" VALUES(16,10,'ZidYNkJlnZ');
INSERT INTO "comment" VALUES(17,11,'TPt AP Rv');
INSERT INTO "comment" VALUES(18,11,'zJiRFij nJ');
INSERT INTO "comment" VALUES(19,11,'kHREmHwXzF');
INSERT INTO "user" VALUES(7,'ИВАН','ИВАНОВ','ИВАНОВИЧ',2,'7(999)1111111','post@post.net');
INSERT INTO "user" VALUES(8,'cYxzJrigjs','wqvTgEzJTh','7(999)2222222',5,'dEPsxtH Dt','oVHZ nmcUZ');
INSERT INTO "user" VALUES(9,'uwAKgimpRI','asSQBMKYSE','7(999)3333333',8,'tOcwDtHLPP','PI ZyMMHB');
INSERT INTO "user" VALUES(10,'HhNfqRq lW','GA uxWNACc','7(999)4444444',1,'XtFkmkgVUJ','JTc VuJIYJ');
INSERT INTO "user" VALUES(11,'DEKfmkvaCO','Vadn XkCvf','7(999)5555555',3,'Yud KgOID','BgCGzRhmQt');
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('region',3);
INSERT INTO "sqlite_sequence" VALUES('city',9);
INSERT INTO "sqlite_sequence" VALUES('comment',23);
INSERT INTO "sqlite_sequence" VALUES('user',13);
COMMIT;
