CREATE TABLE students
(
    test_id           CHAR(36)  NOT NULL,
    student_number    INT       NOT NULL,
    created_date      DATE      NOT NULL,
    created_timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (test_id),
);