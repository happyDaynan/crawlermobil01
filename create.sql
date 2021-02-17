CREATE Database car;

use car;


CREATE table if not exists brand_info(
	`brand_id` int not null PRIMARY KEY,
	`country` char(3) not null,
	`brand_name` char(20) not null
);

CREATE  table if not exists brand_href(
	article_id int not null PRIMARY KEY,
	country char(3) not null,
	brand int not null,
	href varchar(40) not null,
	todbtime datetime,
	articletype char(2)
);

INSERT into brand_info (brand_id, country, brand_name)
VALUES 
(261, "jp", "honda"),
(449, "jp", "infiniti"),
(346,"jp", "lexus"),
(276,"jp", "mazda"),
(262,"jp", "mitsubishi"),
(263,"jp", "nissan"),
(336,"jp", "subaru"),
(277,"jp", "suzuki"),
(264,"jp", "toyota"),
(444,"tw", "luxgen"),
(585,"kr", "hyundai"),
(691, "kr", "kia"),
(260, "us", "ford"),
(616, "us", "gm"),
(741, "us", "tesla"),
(606, "de", "audi"),
(275, "de", "bmw"),
(303, "de", "benz"),
(369, "de", "opel"),
(608, "de", "porsche"),
(623, "de", "skoda"),
(609, "de", "volkswagen");