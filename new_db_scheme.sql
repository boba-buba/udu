CREATE TABLE prm_d.actors(
    id_actor INT AUTO_INCREMENT PRIMARY KEY,
    info JSON
);

CREATE TABLE prm_d.countries(
    id_country INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE prm_d.nationalities(
    id_nationality INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
)

CREATE TABLE prm_d.cities(
    id_city INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    country_id INT,
    latitude FLOAT,
    longitude FLOAT,
    FOREIGN KEY (country_id) REFERENCES prm_d.countries(id_country)
);

CREATE TABLE prm_d.places (
    id_place INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    details JSON,
    nation_id INT,
    city_id INT,
    FOREIGN KEY (nation_id) REFERENCES prm_d.nationalities(id_nationality),
    FOREIGN KEY (city_id) REFERENCES prm_d.cities(id_city)
);

CREATE TABLE prm_d.people (
    id_person INT AUTO_INCREMENT PRIMARY KEY,
    primary_name VARCHAR(50) NOT NULL,
    family_name VARCHAR(50),
    given_name VARCHAR(50),
    middle_name VARCHAR(50),
    nationality_id INT,
    gender VARCHAR(50),
    birth DATE,
    birth_place INT,
    death DATE,
    death_place INT,
    FOREIGN KEY (birth_place) REFERENCES prm_d.places(id_place),
    FOREIGN KEY (death_place) REFERENCES prm_d.places(id_place),
    FOREIGN KEY (nationality_id) REFERENCES prm_d.nationalities(id_nationality)
);

CREATE TABLE prm_d.place_action(
    person_id INT,
    year_start INT,
    month_start INT,
    day_start INT,
    year_end INT,
    month_end INT,
    day_end INT,
    place_id INT,
    FOREIGN KEY (person_id) REFERENCES prm_d.people(id_person),
    FOREIGN KEY (place_id) REFERENCES prm_d.places(id_place),
    PRIMARY KEY (person_id, year_start, month_start, day_start, year_end, month_end, day_end, place_id)
);

CREATE TABLE prm_d.organizations(
    id_organization INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(100),
    time_start DATE,
    time_end DATE
);

CREATE TABLE prm_d.people_organizations(
    organization_id INT NOT NULL,
    person_id INT NOT NULL,
    year_start INT,
    month_start INT,
    day_start INT,
    year_end INT,
    month_end INT,
    day_end INT,
    FOREIGN KEY (organization_id) REFERENCES prm_d.organizations(id_organization),
    FOREIGN KEY (person_id) REFERENCES prm_d.people(id_person),
    PRIMARY KEY (organization_id, person_id, year_start, month_start, day_start, year_end, month_end, day_end)
);

CREATE TABLE prm_d.organization_place(
    organization_id INT NOT NULL,
    place_id INT NOT NULL,
    year_start INT,
    month_start INT,
    day_start INT,
    year_end INT,
    month_end INT,
    day_end INT,
    FOREIGN KEY (organization_id) REFERENCES prm_d.organizations(id_organization),
    FOREIGN KEY (place_id) REFERENCES prm_d.places(id_place),
    PRIMARY KEY (organization_id, place_id, year_start, month_start, day_start, year_end, month_end, day_end)
);


CREATE TABLE prm_d.artworks(
    id_artwork INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(100),
    name VARCHAR(150) NOT NULL,
    language VARCHAR(150),
    name_lang JSON,
    production_by VARCHAR(150),
    production_year_start INT,
    production_month_start INT,
    production_day_start INT,
    production_year_end INT,
    production_month_end INT,
    production_day_end INT,
    width FLOAT,
    height FLOAT,
    place_id INT,
    actor_id INT,
    FOREIGN KEY (place_id) REFERENCES prm_d.places(id_place),
    FOREIGN KEY (actor_id) REFERENCES prm_d.actors(id_actor)

);

CREATE TABLE prm_d.magazines(
    id_magazine INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150),
    production_by_id INT,
    production_in_id INT,
    year_start INT,
    month_start INT,
    day_start INT,
    year_end INT,
    month_end INT,
    day_end INT,
    lang VARCHAR(20),
    add_info_page JSON, # muze byt nekolik takovych stranek
    FOREIGN KEY (production_in_id) REFERENCES prm_d.places(id_place),
    FOREIGN KEY (production_by_id) REFERENCES prm_d.organizations(id_organization)
);

CREATE TABLE prm_d.volumes(
    id_volume INT AUTO_INCREMENT PRIMARY KEY,
    num INT,
    magazine_id INT,
    production_by_id INT,
    production_in_id INT,
    year_start INT,
    month_start INT,
    day_start INT,
    year_end INT,
    month_end INT,
    day_end INT,
    FOREIGN KEY (magazine_id) REFERENCES prm_d.magazines(id_magazine),
    FOREIGN KEY (production_in_id) REFERENCES prm_d.places(id_place),
    FOREIGN KEY (production_by_id) REFERENCES prm_d.organizations(id_organization)
);


CREATE TABLE prm_d.issues(
    id_issue INT AUTO_INCREMENT PRIMARY KEY,
    volume_id INT,
    num INT,
    size INT,
    FOREIGN KEY (volume_id) REFERENCES prm_d.volumes(id_volume)
);



CREATE TABLE prm_d.pages(
    id_page INT AUTO_INCREMENT PRIMARY KEY,
    num INT,
    p_index VARCHAR(15),
    issue_id INT,
    num_repro INT,
    p_text VARCHAR(10),
    full_bleed VARCHAR(10),
    FOREIGN KEY (issue_id) REFERENCES prm_d.issues(id_issue)
);


CREATE TABLE prm_d.add_info(
    id_info INT AUTO_INCREMENT PRIMARY KEY,
    volume_id INT,
    issue_id INT,
    page_id INT,
    text VARCHAR(1000),
    FOREIGN KEY (issue_id) REFERENCES prm_d.issues(id_issue),
    FOREIGN KEY (volume_id) REFERENCES prm_d.volumes(id_volume),
    FOREIGN KEY (page_id) REFERENCES prm_d.pages(id_page)
);

CREATE TABLE prm_d.press_blocks(
    id_block INT AUTO_INCREMENT PRIMARY KEY,
    production_by_id INT,
    production_in_id INT,
    technique VARCHAR(100),
    negativity VARCHAR(50),
    year_start INT,
    month_start INT,
    day_start INT,
    year_end INT,
    month_end INT,
    day_end INT,
    FOREIGN KEY (production_in_id) REFERENCES prm_d.places(id_place),
    FOREIGN KEY (production_by_id) REFERENCES prm_d.organizations(id_organization)
);

CREATE TABLE prm_d.reproductions(
    id_repro INT AUTO_INCREMENT PRIMARY KEY,
    artwork_id INT,
    page_id INT,
    colour VARCHAR(50),
    press_block_id INT,
    x1 INT,
    y1 INT,
    x2 INT,
    y2 INT,
    width FLOAT,
    height FLOAT,
    dimension VARCHAR(25),
    area FLOAT,
    original_image VARCHAR(100),
    FOREIGN KEY (artwork_id) REFERENCES prm_d.artworks(id_artwork),
    FOREIGN KEY (page_id) REFERENCES prm_d.pages(id_page),
    FOREIGN KEY (press_block_id) REFERENCES prm_d.press_blocks(id_block)
);

CREATE TABLE prm_d.repro_issue(
    repro_id INT,
    issue_id INT,
    FOREIGN KEY (repro_id) REFERENCES prm_d.reproductions(id_repro),
    FOREIGN KEY (issue_id) REFERENCES prm_d.issues(id_issue),
    PRIMARY KEY (repro_id, issue_id)
);

CREATE TABLE prm_d.captions(
    id_caption INT AUTO_INCREMENT PRIMARY KEY,
    lang VARCHAR(20),
    text VARCHAR(1000),
    artwork_title VARCHAR(10),
    artwork_author VARCHAR(10),
    artwork_year VARCHAR(10),
    artwork_technique VARCHAR(10),
    artwork_size VARCHAR(10),
    repro_full VARCHAR(10),
    repro_title VARCHAR(10),
    repro_company VARCHAR(10),
    repro_technique VARCHAR(10),
    page_id INT,
    FOREIGN KEY (page_id) REFERENCES prm_d.pages(id_page)
);








