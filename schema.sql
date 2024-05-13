CREATE TABLE public.products (
	id serial4 NOT NULL,
	"name" varchar(100) NOT NULL,
	price float8 NOT NULL,
	created_at timestamp NULL,
	updated_at timestamp NULL,
	is_deleted bool NULL,
	CONSTRAINT products_pkey PRIMARY KEY (id)
);