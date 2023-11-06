delete from captions;
delete from reproductions;
delete from pages;
delete from issues;
delete from volumes;
delete from magazines;
alter table captions auto_increment=1;
alter table reproductions auto_increment=1;
alter table pages auto_increment=1;
alter table issues auto_increment=1;
alter table volumes auto_increment=1;
alter table magazines auto_increment=1;

#delete db
DROP TABLE IF EXISTS prm_d.captions;
DROP TABLE IF EXISTS prm_d.repro_issue;
DROP TABLE IF EXISTS prm_d.reproductions;
DROP TABLE IF EXISTS prm_d.press_blocks;
DROP TABLE IF EXISTS prm_d.add_info;
DROP TABLE IF EXISTS prm_d.pages;
DROP TABLE IF EXISTS prm_d.issues;
DROP TABLE IF EXISTS prm_d.volumes;
DROP TABLE IF EXISTS prm_d.magazines;
DROP TABLE IF EXISTS prm_d.artwork;
DROP TABLE IF EXISTS prm_d.organization_place;
DROP TABLE IF EXISTS prm_d.people_organizations;
DROP TABLE IF EXISTS prm_d.organizations;
DROP TABLE IF EXISTS prm_d.place_action;
DROP TABLE IF EXISTS prm_d.people;
DROP TABLE IF EXISTS prm_d.places;
DROP TABLE IF EXISTS prm_d.cities;
DROP TABLE IF EXISTS prm_d.nations;
DROP TABLE IF EXISTS prm_d.nationalities;
DROP TABLE IF EXISTS prm_d.actors;


