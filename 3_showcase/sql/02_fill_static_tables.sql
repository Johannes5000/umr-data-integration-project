
insert into piece_units values 
    ('kl. Flasche/n'), ('Flasche'), ('Fläschchen'), ('Flaschen'), ('Gläser'), ('gr. Dose/n'),
    ('Dose'), ('Dose/n'), ('kl. Dose/n'), ('gr. Dose/n'), ('Dose'), ('Dose/n'), ('Wurzel'),
    ('Port.'), ('Beutel'), ('Pck.'), ('Pkt.'), ('Paket'), ('Zehe/n'), ('Blatt'), ('Knolle/n'),
    ('Tafeln'), ('Tafel'), ('kl. Stange(n)'), ('Stange/n'), ('Bund'), ('Staude(n)'), ('Bündel'),
    ('kl. Bund'), ('Kugel'), ('Rolle(n)'), ('Kugeln'), ('Kugel/n'), ('Paar'), ('Köpfe'),
    ('Tüte/n'), ('Tasse'), ('Rispe(n)'), ('dicke'), ('Ecke(n)'), ('Teil/e'), ('Riegel'),
    ('Rippe/n'), ('Platte/n'), ('Kästchen'), ('Ring/e'), ('Tube/n'), ('Würfel'), ('kl. Stück(e)'),
    ('Stück(e)'), ('Stück'), ('gr. Stück(e)'), ('großer'), ('große'), ('großes'), ('großen'),
    ('m.-großer'), ('m.-großes'), ('m.-große'), ('kleine'), ('kleiner'), ('kleines'), ('halbe');

insert into convert_mass_to_kg values
    ('mg', 0.000001), ('kg', 1), ('g', 0.001);

insert into convert_volume_to_l values
    ('Liter', 1), ('cl', 0.01 ), ('l', 1), ('ml', 0.001), ('Gläser', 0.2), ('Schuss', 0.001),
    ('gr. Gläser', 0.25), ('Glas', 0.2), ('kl. Glas', 0.15), ('gr. Glas', 0.25), ('dl', 0.1),
    ('Tasse/n', 0.2), ('Becher', 0.15), ('Tasse', 0.2), ('Schälchen', 0.25), ('TL', 0.0049),
    ('EL', 0.0148), ('Spritzer', 0.001);

insert into units_to_ignore values
    ('Prisen'), ('Prise'), ('Prise(n)'), ('Körner'), ('n. B.'), ('evtl.'), ('etwas'),
    ('wenig'), ('Spritzer'), ('Msp.');