create table border_crossing_data
(
    port_name VARCHAR(50),
    state VARCHAR(25),
    port_code INT,
    border VARCHAR(50),
    date VARCHAR(50),
    measure VARCHAR(50),
    value INT,
    latitude FLOAT8,
    longitude FLOAT8
);

create table principal_ports
(
    fid INT,
    port INT,
    type CHAR,
    port_name VARCHAR(100),
    rank INT,
    total INT,
    foreign_amt INT,
    export_amt INT,
    import_amt INT,
    domestic_amt INT
);

create table port_statistical_areas
(
    portidpk INT,
    featuredescription VARCHAR(4096)
);
