//zatim neni photofraphy and exhibition
CREATE TABLE prm_d.actors(
    id INT AUTO_INCREMENT PRIMARY KEY,
    info JSON
);

CREATE TABLE prm_d.nations(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE prm_d.cities(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    country_id INT,
    latitude FLOAT,
    longitude FLOAT,
    FOREIGN KEY (country_id) REFERENCES prm_d.nations(id)
);

CREATE TABLE prm_d.places (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    details JSON,
    nation_id INT,
    city_id INT,
    FOREIGN KEY (nation_id) REFERENCES prm_d.nations(id),
    FOREIGN KEY (city_id) REFERENCES prm_d.cities(id)
);


CREATE TABLE prm_d.people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    primary_name VARCHAR(50) NOT NULL,
    family_name VARCHAR(50),
    given_name VARCHAR(50),
    middle_name VARCHAR(50),
    nationality_id INT,
    ethnicity_id INT,
    gender VARCHAR(50),
    birth DATE,
    birth_place INT,
    death DATE,
    death_place INT,
    FOREIGN KEY (birth_place) REFERENCES prm_d.places(id),
    FOREIGN KEY (death_place) REFERENCES prm_d.places(id),
    FOREIGN KEY (nationality_id) REFERENCES prm_d.nations(id),
    FOREIGN KEY (ethnicity_id) REFERENCES prm_d.nations(id)
);

CREATE TABLE prm_d.place_action(
    person_id INT,
    start_time DATE,
    finish_time DATE,
    place_id INT,
    FOREIGN KEY (person_id) REFERENCES prm_d.people(id),
    FOREIGN KEY (place_id) REFERENCES prm_d.places(id),
    PRIMARY KEY (person_id, start_time, finish_time, place_id)

);
CREATE TABLE prm_d.organizations(
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(100),
    time_start DATE,
    time_end DATE
);

CREATE TABLE prm_d.people_organizations(
    organization_id INT NOT NULL,
    person_id INT NOT NULL,
    time_start DATE,
    time_end DATE,
    FOREIGN KEY (organization_id) REFERENCES prm_d.organizations(id),
    FOREIGN KEY (person_id) REFERENCES prm_d.people(id),
    PRIMARY KEY (organization_id, person_id, time_start, time_end)
);

CREATE TABLE prm_d.organization_place(
    organization_id INT NOT NULL,
    place_id INT NOT NULL,
    time_start DATE,
    time_end DATE,
    FOREIGN KEY (organization_id) REFERENCES prm_d.organizations(id),
    FOREIGN KEY (place_id) REFERENCES prm_d.places(id),
    PRIMARY KEY (organization_id, place_id, time_start, time_end)
);


CREATE TABLE prm_d.artwork(
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(100),
    name VARCHAR(150) NOT NULL,
    language VARCHAR(150),
    name_lang JSON,
    production_by VARCHAR(150),
    production_time_start DATE,
    production_time_end DATE,
    width FLOAT,
    height FLOAT,
    place_id INT,
    actor_id INT,
    FOREIGN KEY (place_id) REFERENCES prm_d.places(id),
    FOREIGN KEY (actor_id) REFERENCES prm_d.actors(id)

);

#CREATE TABLE prm_d.artwork_lang( #mozna jen v predchozi tabulce bude polozak name_lang JSON kde bude "lang" : "name in lang"
#    artwork_id INT, 
#    lang VARCHAR(20),
#    name_lang VARCHAR(150),
#    FOREIGN KEY (artwork_id) REFERENCES prm_d.artwork(id),
#    PRIMARY KEY (artwork_id, lang)
#);

CREATE TABLE prm_d.magazines(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150),
    production_by_id INT,
    production_in_id INT,
    production_time_start DATE,
    production_time_end DATE,
    lang VARCHAR(20),
    add_info_page INT,
    FOREIGN KEY (production_in_id) REFERENCES prm_d.places(id),
    FOREIGN KEY (production_by_id) REFERENCES prm_d.organizations(id)
);

CREATE TABLE prm_d.volumes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    num INT,
    magazine_id INT,
    production_by_id INT,
    production_in_id INT,
    timespan_start DATE,
    timespan_end DATE,
    FOREIGN KEY (magazine_id) REFERENCES prm_d.magazines(id),
    FOREIGN KEY (production_in_id) REFERENCES prm_d.places(id),
    FOREIGN KEY (production_by_id) REFERENCES prm_d.organizations(id)
);

CREATE TABLE prm_d.issues(
    id INT AUTO_INCREMENT PRIMARY KEY,
    volume_id INT,
    num INT,
    size INT,
    FOREIGN KEY (volume_id) REFERENCES prm_d.volumes(id)
);


CREATE TABLE prm_d.pages(
    id INT AUTO_INCREMENT PRIMARY KEY,
    num INT,
    p_index INT,
    issue_id INT,
    num_repro INT,
    p_text VARCHAR(10),
    full_bleed VARCHAR(10),
    FOREIGN KEY (issue_id) REFERENCES prm_d.issues(id)
);

CREATE TABLE prm_d.add_info(
    id INT AUTO_INCREMENT PRIMARY KEY,
    volume_id INT,
    issue_id INT,
    page_id INT,
    text VARCHAR(1000),
    FOREIGN KEY (issue_id) REFERENCES prm_d.issues(id),
    FOREIGN KEY (volume_id) REFERENCES prm_d.volumes(id),
    FOREIGN KEY (page_id) REFERENCES prm_d.pages(id)
);

CREATE TABLE prm_d.press_blocks(
    id INT AUTO_INCREMENT PRIMARY KEY,
    production_by_id INT,
    production_in_id INT,
    technique VARCHAR(100),
    negativity VARCHAR(50),
    timespan_start DATE,
    timespan_end DATE,
    FOREIGN KEY (production_in_id) REFERENCES prm_d.places(id),
    FOREIGN KEY (production_by_id) REFERENCES prm_d.organizations(id)
);

CREATE TABLE prm_d.reproductions(
    id INT AUTO_INCREMENT PRIMARY KEY,
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
    FOREIGN KEY (artwork_id) REFERENCES prm_d.artwork(id),
    FOREIGN KEY (page_id) REFERENCES prm_d.pages(id),
    FOREIGN KEY (press_block_id) REFERENCES prm_d.press_blocks(id)
);

CREATE TABLE prm_d.repro_issue(
    repro_id INT,
    issue_id INT,
    FOREIGN KEY (repro_id) REFERENCES prm_d.reproductions(id),
    FOREIGN KEY (issue_id) REFERENCES prm_d.issues(id),
    PRIMARY KEY (repro_id, issue_id)
);


CREATE TABLE prm_d.captions(
    id INT AUTO_INCREMENT PRIMARY KEY,
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
    FOREIGN KEY (page_id) REFERENCES prm_d.pages(id)
);





























