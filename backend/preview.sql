ALEMBIC DB URL: mysql+mysqlconnector://root:EijgSkopKQOOmUEQgNvezAKaAbtYocwb@metro.proxy.rlwy.net:20825/railway
Using Alembic DATABASE_URL: mysql+mysqlconnector://root:EijgSkopKQOOmUEQgNvezAKaAbtYocwb@metro.proxy.rlwy.net:20825/railway
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> e1ce948fd311

INSERT INTO alembic_version (version_num) VALUES ('e1ce948fd311');

-- Running upgrade e1ce948fd311 -> d64c9728549a

UPDATE alembic_version SET version_num='d64c9728549a' WHERE alembic_version.version_num = 'e1ce948fd311';

-- Running upgrade d64c9728549a -> 477874b15bca

CREATE TABLE shoutouts (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    message VARCHAR(255) NOT NULL, 
    created_at DATETIME, 
    user_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE INDEX ix_shoutouts_id ON shoutouts (id);

UPDATE alembic_version SET version_num='477874b15bca' WHERE alembic_version.version_num = 'd64c9728549a';

-- Running upgrade 477874b15bca -> bcf07d6aa607

ALTER TABLE shoutouts ADD COLUMN target_user_id INTEGER;

ALTER TABLE shoutouts ADD FOREIGN KEY(target_user_id) REFERENCES users (id);

UPDATE alembic_version SET version_num='bcf07d6aa607' WHERE alembic_version.version_num = '477874b15bca';

-- Running upgrade bcf07d6aa607 -> 4653cf4cd6ae

ALTER TABLE proficiencies MODIFY user_id INTEGER NOT NULL;

ALTER TABLE proficiencies MODIFY skill_id INTEGER NOT NULL;

UPDATE alembic_version SET version_num='4653cf4cd6ae' WHERE alembic_version.version_num = 'bcf07d6aa607';

-- Running upgrade 4653cf4cd6ae -> 3675d6a85438

ALTER TABLE ce_records DROP FOREIGN KEY ce_records_ibfk_1;

ALTER TABLE ce_records ADD FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE;

ALTER TABLE proficiencies DROP FOREIGN KEY proficiencies_ibfk_1;

ALTER TABLE proficiencies DROP FOREIGN KEY proficiencies_ibfk_2;

ALTER TABLE proficiencies ADD FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE;

ALTER TABLE proficiencies ADD FOREIGN KEY(skill_id) REFERENCES skills (id) ON DELETE CASCADE;

ALTER TABLE shoutouts DROP FOREIGN KEY shoutouts_ibfk_1;

ALTER TABLE shoutouts DROP FOREIGN KEY shoutouts_ibfk_2;

ALTER TABLE shoutouts ADD FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE;

ALTER TABLE shoutouts ADD FOREIGN KEY(target_user_id) REFERENCES users (id) ON DELETE SET NULL;

ALTER TABLE skills DROP FOREIGN KEY skills_ibfk_1;

ALTER TABLE skills ADD FOREIGN KEY(category_id) REFERENCES categories (id) ON DELETE CASCADE;

UPDATE alembic_version SET version_num='3675d6a85438' WHERE alembic_version.version_num = '4653cf4cd6ae';

-- Running upgrade 3675d6a85438 -> f42a67b3525f

ALTER TABLE users ADD COLUMN is_demo_user BOOL;

UPDATE alembic_version SET version_num='f42a67b3525f' WHERE alembic_version.version_num = '3675d6a85438';

