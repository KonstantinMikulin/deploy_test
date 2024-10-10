create table user (
    user_uid UUID NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table weight (
    weight_uid UUID NOT NULL PRIMARY KEY,
    weight NUMERIC(5, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_uid UUID REFERENCES user (user_uid),
    UNIQUE(user_uid)
);