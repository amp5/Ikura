--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: cards; Type: TABLE; Schema: public; Owner: alexandraplassaras; Tablespace: 
--

CREATE TABLE cards (
    card_id integer NOT NULL,
    card_name character varying(64),
    card_debt money,
    card_apr integer,
    card_date date,
    user_id integer
);


ALTER TABLE cards OWNER TO alexandraplassaras;

--
-- Name: cards_card_id_seq; Type: SEQUENCE; Schema: public; Owner: alexandraplassaras
--

CREATE SEQUENCE cards_card_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cards_card_id_seq OWNER TO alexandraplassaras;

--
-- Name: cards_card_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alexandraplassaras
--

ALTER SEQUENCE cards_card_id_seq OWNED BY cards.card_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: alexandraplassaras; Tablespace: 
--

CREATE TABLE users (
    user_id integer NOT NULL,
    email character varying(64),
    password character varying(64)
);


ALTER TABLE users OWNER TO alexandraplassaras;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: alexandraplassaras
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO alexandraplassaras;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alexandraplassaras
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: values; Type: TABLE; Schema: public; Owner: alexandraplassaras; Tablespace: 
--

CREATE TABLE "values" (
    value_id integer NOT NULL,
    money_spent_high boolean,
    money_spent_low boolean,
    time_1 boolean,
    time_2 boolean,
    time_3 boolean,
    money_amnt_low boolean,
    money_amnt_high boolean,
    user_id integer
);


ALTER TABLE "values" OWNER TO alexandraplassaras;

--
-- Name: values_value_id_seq; Type: SEQUENCE; Schema: public; Owner: alexandraplassaras
--

CREATE SEQUENCE values_value_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE values_value_id_seq OWNER TO alexandraplassaras;

--
-- Name: values_value_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alexandraplassaras
--

ALTER SEQUENCE values_value_id_seq OWNED BY "values".value_id;


--
-- Name: card_id; Type: DEFAULT; Schema: public; Owner: alexandraplassaras
--

ALTER TABLE ONLY cards ALTER COLUMN card_id SET DEFAULT nextval('cards_card_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: alexandraplassaras
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Name: value_id; Type: DEFAULT; Schema: public; Owner: alexandraplassaras
--

ALTER TABLE ONLY "values" ALTER COLUMN value_id SET DEFAULT nextval('values_value_id_seq'::regclass);


--
-- Data for Name: cards; Type: TABLE DATA; Schema: public; Owner: alexandraplassaras
--

COPY cards (card_id, card_name, card_debt, card_apr, card_date, user_id) FROM stdin;
1	Visa 123	$2,022.00	15	\N	\N
\.


--
-- Name: cards_card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alexandraplassaras
--

SELECT pg_catalog.setval('cards_card_id_seq', 1, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: alexandraplassaras
--

COPY users (user_id, email, password) FROM stdin;
1	aplass@gmail.com	debt
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alexandraplassaras
--

SELECT pg_catalog.setval('users_user_id_seq', 1, true);


--
-- Data for Name: values; Type: TABLE DATA; Schema: public; Owner: alexandraplassaras
--

COPY "values" (value_id, money_spent_high, money_spent_low, time_1, time_2, time_3, money_amnt_low, money_amnt_high, user_id) FROM stdin;
\.


--
-- Name: values_value_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alexandraplassaras
--

SELECT pg_catalog.setval('values_value_id_seq', 1, false);


--
-- Name: cards_pkey; Type: CONSTRAINT; Schema: public; Owner: alexandraplassaras; Tablespace: 
--

ALTER TABLE ONLY cards
    ADD CONSTRAINT cards_pkey PRIMARY KEY (card_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: alexandraplassaras; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: values_pkey; Type: CONSTRAINT; Schema: public; Owner: alexandraplassaras; Tablespace: 
--

ALTER TABLE ONLY "values"
    ADD CONSTRAINT values_pkey PRIMARY KEY (value_id);


--
-- Name: cards_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alexandraplassaras
--

ALTER TABLE ONLY cards
    ADD CONSTRAINT cards_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: values_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alexandraplassaras
--

ALTER TABLE ONLY "values"
    ADD CONSTRAINT values_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: alexandraplassaras
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM alexandraplassaras;
GRANT ALL ON SCHEMA public TO alexandraplassaras;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

