# Database Schema.  Used if a new database is created.

DB_SCHEMA = """
--
-- PostgreSQL database dump
--

-- Dumped from database version 15.5 (Ubuntu 15.5-0ubuntu0.23.04.1)
-- Dumped by pg_dump version 15.5 (Ubuntu 15.5-0ubuntu0.23.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: service_providers; Type: TABLE; Schema: public; Owner: savonpy_user
--

CREATE TABLE public.service_providers (
    id integer NOT NULL,
    provider_name character varying NOT NULL,
    provider_url character varying NOT NULL,
    site_schema integer NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.service_providers OWNER TO savonpy_user;

--
-- Name: service_provider_id_seq; Type: SEQUENCE; Schema: public; Owner: savonpy_user
--

CREATE SEQUENCE public.service_provider_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.service_provider_id_seq OWNER TO savonpy_user;

--
-- Name: service_provider_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: savonpy_user
--

ALTER SEQUENCE public.service_provider_id_seq OWNED BY public.service_providers.id;


--
-- Name: sp_schemas; Type: TABLE; Schema: public; Owner: savonpy_user
--

CREATE TABLE public.sp_schemas (
    id integer NOT NULL,
    refresh_period bigint DEFAULT 600 NOT NULL,
    cookie_flow jsonb DEFAULT '{}'::jsonb NOT NULL
);


ALTER TABLE public.sp_schemas OWNER TO savonpy_user;

--
-- Name: sp_schema_id_seq; Type: SEQUENCE; Schema: public; Owner: savonpy_user
--

CREATE SEQUENCE public.sp_schema_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sp_schema_id_seq OWNER TO savonpy_user;

--
-- Name: sp_schema_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: savonpy_user
--

ALTER SEQUENCE public.sp_schema_id_seq OWNED BY public.sp_schemas.id;


--
-- Name: user_accounts; Type: TABLE; Schema: public; Owner: savonpy_user
--

CREATE TABLE public.user_accounts (
    id integer NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL,
    password_expires timestamp with time zone DEFAULT now() NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    sms character varying,
    email character varying
);


ALTER TABLE public.user_accounts OWNER TO savonpy_user;

--
-- Name: user_account_id_seq; Type: SEQUENCE; Schema: public; Owner: savonpy_user
--

CREATE SEQUENCE public.user_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_account_id_seq OWNER TO savonpy_user;

--
-- Name: user_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: savonpy_user
--

ALTER SEQUENCE public.user_account_id_seq OWNED BY public.user_accounts.id;


--
-- Name: user_services; Type: TABLE; Schema: public; Owner: savonpy_user
--

CREATE TABLE public.user_services (
    id integer NOT NULL,
    "user" integer NOT NULL,
    service integer NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    user_sp_username character varying NOT NULL,
    requires_otp boolean DEFAULT false NOT NULL,
    otp_method character varying,
    user_sp_password character varying
);


ALTER TABLE public.user_services OWNER TO savonpy_user;

--
-- Name: user_services_id_seq; Type: SEQUENCE; Schema: public; Owner: savonpy_user
--

CREATE SEQUENCE public.user_services_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_services_id_seq OWNER TO savonpy_user;

--
-- Name: user_services_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: savonpy_user
--

ALTER SEQUENCE public.user_services_id_seq OWNED BY public.user_services.id;


--
-- Name: service_providers id; Type: DEFAULT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.service_providers ALTER COLUMN id SET DEFAULT nextval('public.service_provider_id_seq'::regclass);


--
-- Name: sp_schemas id; Type: DEFAULT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.sp_schemas ALTER COLUMN id SET DEFAULT nextval('public.sp_schema_id_seq'::regclass);


--
-- Name: user_accounts id; Type: DEFAULT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.user_accounts ALTER COLUMN id SET DEFAULT nextval('public.user_account_id_seq'::regclass);


--
-- Name: user_services id; Type: DEFAULT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.user_services ALTER COLUMN id SET DEFAULT nextval('public.user_services_id_seq'::regclass);


--
-- Name: service_providers service_provider_pkey; Type: CONSTRAINT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.service_providers
    ADD CONSTRAINT service_provider_pkey PRIMARY KEY (id);


--
-- Name: service_providers service_providers_un; Type: CONSTRAINT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.service_providers
    ADD CONSTRAINT service_providers_un UNIQUE (provider_url);


--
-- Name: sp_schemas sp_schema_pkey; Type: CONSTRAINT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.sp_schemas
    ADD CONSTRAINT sp_schema_pkey PRIMARY KEY (id);


--
-- Name: user_accounts user_account_pkey; Type: CONSTRAINT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.user_accounts
    ADD CONSTRAINT user_account_pkey PRIMARY KEY (id);


--
-- Name: user_accounts user_accounts_un; Type: CONSTRAINT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.user_accounts
    ADD CONSTRAINT user_accounts_un UNIQUE (username);


--
-- Name: user_accounts user_accounts_un2; Type: CONSTRAINT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.user_accounts
    ADD CONSTRAINT user_accounts_un2 UNIQUE (sms);


--
-- Name: user_accounts user_accounts_un3; Type: CONSTRAINT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.user_accounts
    ADD CONSTRAINT user_accounts_un3 UNIQUE (email);


--
-- Name: user_services user_services_pkey; Type: CONSTRAINT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.user_services
    ADD CONSTRAINT user_services_pkey PRIMARY KEY (id);


--
-- Name: user_services user_services_un; Type: CONSTRAINT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.user_services
    ADD CONSTRAINT user_services_un UNIQUE ("user", service);


--
-- Name: service_providers service_provider_fk; Type: FK CONSTRAINT; Schema: public; Owner: savonpy_user
--

ALTER TABLE ONLY public.service_providers
    ADD CONSTRAINT service_provider_fk FOREIGN KEY (site_schema) REFERENCES public.sp_schemas(id);


--
-- PostgreSQL database dump complete
--

"""
DB_TEST_COMMANDS = [
    'SELECT * FROM user_accounts;',
    'SELECT * FROM control;'
]