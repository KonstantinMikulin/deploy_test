create table users (
    user_uid UUID NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

create table weight (
    weight_uid UUID NOT NULL PRIMARY KEY,
    weight NUMERIC(5, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    user_uid UUID REFERENCES users (user_uid)
);

CREATE TABLE measure (
    measure_uid UUID NOT NULL PRIMARY KEY,
    measure NUMERIC(5, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    user_uid UUID REFERENCES users (user_uid)
);

INSERT INTO users (user_uid, name, gender, created_at)
VALUES (uuid_generate_v4(), 'Dan', 'Male', NOW());

INSERT INTO users (user_uid, name, gender, created_at)
VALUES (uuid_generate_v4(), 'Anna', 'Female', NOW());
