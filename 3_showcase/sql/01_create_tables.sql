drop table if exists piece_units cascade;
create table piece_units (
    unit text
);

drop table if exists convert_mass_to_kg cascade;
create table convert_mass_to_kg (
    unit text,
    factor numeric
);

drop table if exists convert_volume_to_l cascade;
create table convert_volume_to_l (
    unit text,
    factor numeric
);

drop table if exists units_to_ignore cascade;
create table units_to_ignore (
    unit text
);