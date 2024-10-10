# weigth
INSERT INTO weight (weight_uid, weight, created_at, user_uid)
VALUES (uuid_generate_v4(), 95, CURRENT_TIMESTAMP, '181fe249-8616-42b5-9892-ba29c5205f5f');

INSERT INTO weight (weight_uid, weight, created_at, user_uid)
VALUES (uuid_generate_v4(), 94, CURRENT_TIMESTAMP, '181fe249-8616-42b5-9892-ba29c5205f5f');

INSERT INTO weight (weight_uid, weight, created_at, user_uid)
VALUES (uuid_generate_v4(), 55, NOW(), 'c5f0fe98-a6dc-40c5-a936-b07f97502b10');

INSERT INTO weight (weight_uid, weight, created_at, user_uid)
VALUES (uuid_generate_v4(), 54, NOW(), 'c5f0fe98-a6dc-40c5-a936-b07f97502b10');

# measure
INSERT INTO measure (measure_uid, measure, created_at, user_uid)
VALUES (uuid_generate_v4(), 35, NOW(), '181fe249-8616-42b5-9892-ba29c5205f5f');

INSERT INTO measure (measure_uid, measure, created_at, user_uid)
VALUES (uuid_generate_v4(), 25, NOW(), 'c5f0fe98-a6dc-40c5-a936-b07f97502b10');
