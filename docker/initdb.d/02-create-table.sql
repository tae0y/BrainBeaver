BEGIN;

CREATE TABLE tb_concepts (
            id serial primary key,
            title text,
            datasource text,
            keywords text,
            category text,
            summary text,
            status text,
            filepath text,
            source_num integer,
            target_num integer,
            create_time timestamp,
            update_time timestamp,
            token_num integer,
            plaintext text,
            embedding vector(8000)
);

CREATE TABLE tb_networks (
            id serial primary key,
            source_concept_id integer,
            target_concept_id integer
);

CREATE TABLE tb_references (
            id serial primary key,
            concept_id integer,
            description text
);

END;