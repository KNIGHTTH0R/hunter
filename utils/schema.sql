--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.5
-- Dumped by pg_dump version 9.5.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: truncate_tables(character varying); Type: FUNCTION; Schema: public; Owner: hunter
--

CREATE FUNCTION truncate_tables(username character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    statements CURSOR FOR
        SELECT tablename FROM pg_tables
        WHERE tableowner = username AND schemaname = 'public';
BEGIN
    FOR stmt IN statements LOOP
        EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) || ' CASCADE;';
    END LOOP;
END;
$$;


ALTER FUNCTION public.truncate_tables(username character varying) OWNER TO hunter;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: accounts; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE accounts (
    id integer NOT NULL,
    email text NOT NULL,
    gender text,
    name text,
    given_name text,
    picture text,
    verified_email text,
    family_name text,
    link text,
    status text DEFAULT 'not_activated'::text,
    gname text DEFAULT 'new'::text,
    telegram_name text,
    can_view_achives boolean DEFAULT false,
    permissions text DEFAULT 'not'::text,
    token text
);


ALTER TABLE accounts OWNER TO hunter;

--
-- Name: accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE accounts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE accounts_id_seq OWNER TO hunter;

--
-- Name: accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE accounts_id_seq OWNED BY accounts.id;


--
-- Name: achive; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE achive (
    id integer NOT NULL,
    name text,
    late6 bigint NOT NULL,
    lnge6 bigint NOT NULL,
    team integer,
    player text,
    "timestamp" bigint,
    address text,
    pguid text,
    showed boolean,
    img text,
    status text,
    ada boolean DEFAULT false,
    tile text,
    downloaded text
);


ALTER TABLE achive OWNER TO hunter;

--
-- Name: achive_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE achive_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE achive_id_seq OWNER TO hunter;

--
-- Name: achive_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE achive_id_seq OWNED BY achive.id;


--
-- Name: actions; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE actions (
    mguid text NOT NULL,
    late6 bigint,
    lnge6 bigint,
    plain smallint,
    player text,
    "timestamp" bigint,
    team smallint,
    low_name text,
    address text,
    name text
);


ALTER TABLE actions OWNER TO hunter;

--
-- Name: ada; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE ada (
    id integer NOT NULL,
    name text,
    late6 bigint NOT NULL,
    lnge6 bigint NOT NULL,
    team integer,
    player text,
    "timestamp" bigint,
    low_name text,
    status text
);


ALTER TABLE ada OWNER TO hunter;

--
-- Name: ada_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE ada_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ada_id_seq OWNER TO hunter;

--
-- Name: ada_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE ada_id_seq OWNED BY ada.id;


--
-- Name: cookies; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE cookies (
    email text NOT NULL,
    passwd text NOT NULL,
    lastaccess bigint,
    status text,
    lastupdate real,
    cookie text,
    tag text,
    additional_info text,
    scanner_cookie text,
    slastaccess bigint,
    slastupdate bigint,
    sstatus integer,
    software text,
    id integer NOT NULL
);


ALTER TABLE cookies OWNER TO hunter;

--
-- Name: cookies_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE cookies_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cookies_id_seq OWNER TO hunter;

--
-- Name: cookies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE cookies_id_seq OWNED BY cookies.id;


--
-- Name: inspector; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE inspector (
    id integer NOT NULL,
    player text,
    lvl integer,
    guid text,
    "timestamp" bigint DEFAULT '1'::bigint,
    team integer DEFAULT 3,
    task text,
    parameters text,
    late6 bigint,
    lnge6 bigint,
    tag text,
    expired bigint DEFAULT '-1'::bigint,
    mods json,
    resonators json,
    allow json
);


ALTER TABLE inspector OWNER TO hunter;

--
-- Name: inspector_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE inspector_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE inspector_id_seq OWNER TO hunter;

--
-- Name: inspector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE inspector_id_seq OWNED BY inspector.id;


--
-- Name: map; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE map (
    number bigint NOT NULL,
    country text,
    city text,
    region text,
    continent text,
    late6 bigint,
    lnge6 bigint
);


ALTER TABLE map OWNER TO hunter;

--
-- Name: player; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE player (
    player text,
    "timestamp" bigint,
    late6 bigint,
    lnge6 bigint,
    team integer,
    address text,
    plain integer,
    name text,
    player_lowercase text,
    id integer NOT NULL
);


ALTER TABLE player OWNER TO hunter;

--
-- Name: player_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE player_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE player_id_seq OWNER TO hunter;

--
-- Name: player_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE player_id_seq OWNED BY player.id;


--
-- Name: players; Type: TABLE; Schema: public; Owner: hunter
--

CREATE UNLOGGED TABLE players (
    id integer NOT NULL,
    player text,
    low_name text,
    late6 bigint,
    lnge6 bigint,
    live_in text,
    update bigint DEFAULT '1'::bigint,
    guardian integer
);


ALTER TABLE players OWNER TO hunter;

--
-- Name: players_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE players_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE players_id_seq OWNER TO hunter;

--
-- Name: players_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE players_id_seq OWNED BY players.id;


--
-- Name: profiles; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE profiles (
    id integer NOT NULL,
    playername text,
    lvl integer,
    badges json,
    metrics json,
    ap bigint,
    team integer,
    mission_badges json,
    update bigint
);


ALTER TABLE profiles OWNER TO hunter;

--
-- Name: profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE profiles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE profiles_id_seq OWNER TO hunter;

--
-- Name: profiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE profiles_id_seq OWNED BY profiles.id;


--
-- Name: public_history; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE public_history (
    id integer NOT NULL,
    agent text,
    count integer,
    "timestamp" bigint,
    team integer,
    live_in text
);


ALTER TABLE public_history OWNER TO hunter;

--
-- Name: public_history_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE public_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public_history_id_seq OWNER TO hunter;

--
-- Name: public_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE public_history_id_seq OWNED BY public_history.id;


--
-- Name: scanner_inventory; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE scanner_inventory (
    agent_id text,
    description json,
    "timestamp" bigint
);


ALTER TABLE scanner_inventory OWNER TO hunter;

--
-- Name: scanner_player_id; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE scanner_player_id (
    id integer NOT NULL,
    email text,
    agent_name text,
    agent_id text,
    cookie text,
    xsrf text,
    faction text,
    "timestamp" bigint,
    active boolean DEFAULT false,
    hide bigint
);


ALTER TABLE scanner_player_id OWNER TO hunter;

--
-- Name: scanner_player_id_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE scanner_player_id_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE scanner_player_id_id_seq OWNER TO hunter;

--
-- Name: scanner_player_id_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE scanner_player_id_id_seq OWNED BY scanner_player_id.id;


--
-- Name: short_url; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE short_url (
    id integer NOT NULL,
    url text,
    s_url text
);


ALTER TABLE short_url OWNER TO hunter;

--
-- Name: short_url_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE short_url_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE short_url_id_seq OWNER TO hunter;

--
-- Name: short_url_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE short_url_id_seq OWNED BY short_url.id;


--
-- Name: tags; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE tags (
    id integer NOT NULL,
    tag_name text NOT NULL,
    tag_value json NOT NULL,
    username text
);


ALTER TABLE tags OWNER TO hunter;

--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tags_id_seq OWNER TO hunter;

--
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE tags_id_seq OWNED BY tags.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE tasks (
    id integer NOT NULL,
    latlng json,
    server text
);


ALTER TABLE tasks OWNER TO hunter;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE tasks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tasks_id_seq OWNER TO hunter;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE tasks_id_seq OWNED BY tasks.id;


--
-- Name: telegram; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE telegram (
    id integer NOT NULL,
    username text NOT NULL,
    zoom integer DEFAULT 15,
    "timestamp" bigint DEFAULT '1000'::bigint,
    strings integer DEFAULT 50,
    chat_id bigint,
    approved boolean DEFAULT false,
    allow text,
    is_group boolean DEFAULT false,
    super_group boolean DEFAULT false
);


ALTER TABLE telegram OWNER TO hunter;

--
-- Name: telegram_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE telegram_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE telegram_id_seq OWNER TO hunter;

--
-- Name: telegram_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE telegram_id_seq OWNED BY telegram.id;


--
-- Name: userslog; Type: TABLE; Schema: public; Owner: hunter
--

CREATE TABLE userslog (
    id integer NOT NULL,
    action text,
    "timestamp" bigint,
    ip text,
    email text,
    data json
);


ALTER TABLE userslog OWNER TO hunter;

--
-- Name: userslog_id_seq; Type: SEQUENCE; Schema: public; Owner: hunter
--

CREATE SEQUENCE userslog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE userslog_id_seq OWNER TO hunter;

--
-- Name: userslog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hunter
--

ALTER SEQUENCE userslog_id_seq OWNED BY userslog.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY accounts ALTER COLUMN id SET DEFAULT nextval('accounts_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY achive ALTER COLUMN id SET DEFAULT nextval('achive_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY ada ALTER COLUMN id SET DEFAULT nextval('ada_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY cookies ALTER COLUMN id SET DEFAULT nextval('cookies_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY inspector ALTER COLUMN id SET DEFAULT nextval('inspector_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY player ALTER COLUMN id SET DEFAULT nextval('player_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY players ALTER COLUMN id SET DEFAULT nextval('players_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY profiles ALTER COLUMN id SET DEFAULT nextval('profiles_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY public_history ALTER COLUMN id SET DEFAULT nextval('public_history_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY scanner_player_id ALTER COLUMN id SET DEFAULT nextval('scanner_player_id_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY short_url ALTER COLUMN id SET DEFAULT nextval('short_url_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY tags ALTER COLUMN id SET DEFAULT nextval('tags_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY tasks ALTER COLUMN id SET DEFAULT nextval('tasks_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY telegram ALTER COLUMN id SET DEFAULT nextval('telegram_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY userslog ALTER COLUMN id SET DEFAULT nextval('userslog_id_seq'::regclass);


--
-- Name: accounts_email_key; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY accounts
    ADD CONSTRAINT accounts_email_key UNIQUE (email);


--
-- Name: accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);


--
-- Name: achive_late6_lnge6_key; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY achive
    ADD CONSTRAINT achive_late6_lnge6_key UNIQUE (late6, lnge6);


--
-- Name: achive_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY achive
    ADD CONSTRAINT achive_pkey PRIMARY KEY (id);


--
-- Name: actions_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY actions
    ADD CONSTRAINT actions_pkey PRIMARY KEY (mguid);


--
-- Name: ada_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY ada
    ADD CONSTRAINT ada_pkey PRIMARY KEY (id);


--
-- Name: ada_timestamp_key; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY ada
    ADD CONSTRAINT ada_timestamp_key UNIQUE ("timestamp");


--
-- Name: cookies_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY cookies
    ADD CONSTRAINT cookies_pkey PRIMARY KEY (email);


--
-- Name: inspector_guid_key; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY inspector
    ADD CONSTRAINT inspector_guid_key UNIQUE (guid);


--
-- Name: inspector_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY inspector
    ADD CONSTRAINT inspector_pkey PRIMARY KEY (id);


--
-- Name: map_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY map
    ADD CONSTRAINT map_pkey PRIMARY KEY (number);


--
-- Name: player_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY player
    ADD CONSTRAINT player_pkey PRIMARY KEY (id);


--
-- Name: player_player_idx; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY player
    ADD CONSTRAINT player_player_idx UNIQUE (player);


--
-- Name: CONSTRAINT player_player_idx ON player; Type: COMMENT; Schema: public; Owner: hunter
--

COMMENT ON CONSTRAINT player_player_idx ON player IS 'player_player_idx';


--
-- Name: players_low_name_key; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY players
    ADD CONSTRAINT players_low_name_key UNIQUE (low_name);


--
-- Name: players_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY players
    ADD CONSTRAINT players_pkey PRIMARY KEY (id);


--
-- Name: profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (id);


--
-- Name: public_history_agent_key; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY public_history
    ADD CONSTRAINT public_history_agent_key UNIQUE (agent);


--
-- Name: public_history_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY public_history
    ADD CONSTRAINT public_history_pkey PRIMARY KEY (id);


--
-- Name: scanner_inventory_agent_id_key; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY scanner_inventory
    ADD CONSTRAINT scanner_inventory_agent_id_key UNIQUE (agent_id);


--
-- Name: scanner_player_id_agent_id_key; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY scanner_player_id
    ADD CONSTRAINT scanner_player_id_agent_id_key UNIQUE (agent_id);


--
-- Name: scanner_player_id_agent_name_key; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY scanner_player_id
    ADD CONSTRAINT scanner_player_id_agent_name_key UNIQUE (agent_name);


--
-- Name: scanner_player_id_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY scanner_player_id
    ADD CONSTRAINT scanner_player_id_pkey PRIMARY KEY (id);


--
-- Name: short_url_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY short_url
    ADD CONSTRAINT short_url_pkey PRIMARY KEY (id);


--
-- Name: tags_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: tags_tag_name_key; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY tags
    ADD CONSTRAINT tags_tag_name_key UNIQUE (tag_name);


--
-- Name: tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: telegram_chat_id_key; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY telegram
    ADD CONSTRAINT telegram_chat_id_key UNIQUE (chat_id);


--
-- Name: telegram_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY telegram
    ADD CONSTRAINT telegram_pkey PRIMARY KEY (id);


--
-- Name: userslog_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY userslog
    ADD CONSTRAINT userslog_pkey PRIMARY KEY (id);


--
-- Name: accounts_token_idx; Type: INDEX; Schema: public; Owner: hunter
--

CREATE INDEX accounts_token_idx ON accounts USING btree (token);


--
-- Name: achive_lower_idx; Type: INDEX; Schema: public; Owner: hunter
--

CREATE INDEX achive_lower_idx ON achive USING btree (lower(player));


--
-- Name: achive_lower_idx1; Type: INDEX; Schema: public; Owner: hunter
--

CREATE INDEX achive_lower_idx1 ON achive USING btree (lower(name));


--
-- Name: achive_name_idx; Type: INDEX; Schema: public; Owner: hunter
--

CREATE INDEX achive_name_idx ON achive USING btree (name);


--
-- Name: achive_upper_idx; Type: INDEX; Schema: public; Owner: hunter
--

CREATE INDEX achive_upper_idx ON achive USING btree (upper(player));


--
-- Name: actions_late6_lnge6_idx; Type: INDEX; Schema: public; Owner: hunter
--

CREATE INDEX actions_late6_lnge6_idx ON actions USING btree (late6, lnge6);


--
-- Name: player_key; Type: INDEX; Schema: public; Owner: hunter
--

CREATE INDEX player_key ON actions USING btree (player);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

