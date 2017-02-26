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

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

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
-- Name: id; Type: DEFAULT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY tasks ALTER COLUMN id SET DEFAULT nextval('tasks_id_seq'::regclass);


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: hunter
--

COPY tasks (id, latlng, server) FROM stdin;
147	{"minLngE6": 37537039, "maxLatE6": 50049217, "minLatE6": 42567670, "maxLngE6": 45031767}	test
156	{"minLngE6": 45031767, "maxLatE6": 65012312, "minLatE6": 57530764, "maxLngE6": 52526495}	test
39	{"maxLatE6": -24987688, "minLngE6": -179957689, "maxLngE6": -149978777, "minLatE6": -54913877}	test
165	{"minLatE6": 42567670, "maxLngE6": -89978777, "maxLatE6": 50049217, "minLngE6": -97473505}	test
174	{"minLngE6": -89957689, "maxLatE6": 42567670, "minLatE6": 35086123, "maxLngE6": -82462961}	test
183	{"minLngE6": -82462961, "maxLatE6": 57530764, "minLatE6": 50049217, "maxLngE6": -74968233}	test
193	{"maxLngE6": 21223, "minLatE6": 65086123, "minLngE6": -59957689, "maxLatE6": 78000000}	test
48	{"maxLatE6": 65012312, "minLngE6": -149957689, "maxLngE6": -119978777, "minLatE6": 35086123}	test
57	{"maxLatE6": -24987688, "minLngE6": -89957689, "maxLngE6": -59978777, "minLatE6": -54913877}	test
66	{"maxLatE6": 65012312, "minLngE6": -59957689, "maxLngE6": -29978777, "minLatE6": 35086123}	test
75	{"maxLatE6": -24987688, "minLngE6": 42311, "maxLngE6": 30021223, "minLatE6": -54913877}	test
93	{"maxLatE6": -24987688, "minLngE6": 90042311, "maxLngE6": 120021223, "minLatE6": -54913877}	test
148	{"minLngE6": 45031767, "maxLatE6": 50049217, "minLatE6": 42567670, "maxLngE6": 52526495}	test
157	{"minLngE6": 52526495, "maxLatE6": 65012312, "minLatE6": 57530764, "maxLngE6": 60021223}	test
166	{"minLatE6": 50049217, "maxLngE6": -112462961, "maxLatE6": 57530764, "minLngE6": -119957689}	test
175	{"minLngE6": -82462961, "maxLatE6": 42567670, "minLatE6": 35086123, "maxLngE6": -74968233}	test
184	{"minLngE6": -74968233, "maxLatE6": 57530764, "minLatE6": 50049217, "maxLngE6": -67473505}	test
194	{"maxLngE6": 60021223, "minLatE6": 65086123, "minLngE6": 42311, "maxLatE6": 78000000}	test
102	{"maxLatE6": 65012312, "minLngE6": 120042311, "maxLngE6": 150021223, "minLatE6": 35086123}	test
129	{"minLatE6": 35086123, "maxLngE6": 30021223, "minLngE6": 22526495, "maxLatE6": 42567670}	test
138	{"minLatE6": 57530764, "maxLngE6": 7537039, "minLngE6": 42311, "maxLatE6": 65012312}	test
130	{"minLatE6": 42567670, "maxLngE6": 7537039, "minLngE6": 42311, "maxLatE6": 50049217}	test
139	{"minLatE6": 57530764, "maxLngE6": 15031767, "minLngE6": 7537039, "maxLatE6": 65012312}	test
40	{"maxLatE6": 5012312, "minLngE6": -179957689, "maxLngE6": -149978777, "minLatE6": -24913877}	test
58	{"maxLatE6": 5012312, "minLngE6": -89957689, "maxLngE6": -59978777, "minLatE6": -24913877}	test
76	{"maxLatE6": 5012312, "minLngE6": 42311, "maxLngE6": 30021223, "minLatE6": -24913877}	test
94	{"maxLatE6": 5012312, "minLngE6": 90042311, "maxLngE6": 120021223, "minLatE6": -24913877}	test
140	{"minLatE6": 57530764, "maxLngE6": 22526495, "minLngE6": 15031767, "maxLatE6": 65012312}	test
149	{"minLngE6": 52526495, "maxLatE6": 50049217, "minLatE6": 42567670, "maxLngE6": 60021223}	test
158	{"minLatE6": 35086123, "maxLngE6": -112462961, "maxLatE6": 42567670, "minLngE6": -119957689}	test
167	{"minLatE6": 50049217, "maxLngE6": -104968233, "maxLatE6": 57530764, "minLngE6": -112462961}	test
176	{"minLngE6": -74968233, "maxLatE6": 42567670, "minLatE6": 35086123, "maxLngE6": -67473505}	test
185	{"minLngE6": -67473505, "maxLatE6": 57530764, "minLatE6": 50049217, "maxLngE6": -59978777}	test
195	{"maxLngE6": 120021223, "minLatE6": 65086123, "minLngE6": 60042311, "maxLatE6": 78000000}	test
41	{"maxLatE6": 35012312, "minLngE6": -179957689, "maxLngE6": -149978777, "minLatE6": 5086123}	test
59	{"maxLatE6": 35012312, "minLngE6": -89957689, "maxLngE6": -59978777, "minLatE6": 5086123}	test
77	{"maxLatE6": 35012312, "minLngE6": 42311, "maxLngE6": 30021223, "minLatE6": 5086123}	test
95	{"maxLatE6": 35012312, "minLngE6": 90042311, "maxLngE6": 120021223, "minLatE6": 5086123}	test
131	{"minLatE6": 42567670, "maxLngE6": 15031767, "minLngE6": 7537039, "maxLatE6": 50049217}	test
141	{"minLatE6": 57530764, "maxLngE6": 30021223, "minLngE6": 22526495, "maxLatE6": 65012312}	test
150	{"minLngE6": 30042311, "maxLatE6": 57530764, "minLatE6": 50049217, "maxLngE6": 37537039}	test
159	{"minLatE6": 35086123, "maxLngE6": -104968233, "maxLatE6": 42567670, "minLngE6": -112462961}	test
168	{"minLatE6": 50049217, "maxLngE6": -97473505, "maxLatE6": 57530764, "minLngE6": -104968233}	test
177	{"minLngE6": -67473505, "maxLatE6": 42567670, "minLatE6": 35086123, "maxLngE6": -59978777}	test
186	{"minLngE6": -89957689, "maxLatE6": 65012312, "minLatE6": 57530764, "maxLngE6": -82462961}	test
196	{"maxLngE6": 180021223, "minLatE6": 65086123, "minLngE6": 120042311, "maxLatE6": 78000000}	test
42	{"maxLatE6": 65012312, "minLngE6": -179957689, "maxLngE6": -149978777, "minLatE6": 35086123}	test
51	{"maxLatE6": -24987688, "minLngE6": -119957689, "maxLngE6": -89978777, "minLatE6": -54913877}	test
69	{"maxLatE6": -24987688, "minLngE6": -29957689, "maxLngE6": 21223, "minLatE6": -54913877}	test
87	{"maxLatE6": -24987688, "minLngE6": 60042311, "maxLngE6": 90021223, "minLatE6": -54913877}	test
96	{"maxLatE6": 65012312, "minLngE6": 90042311, "maxLngE6": 120021223, "minLatE6": 35086123}	test
105	{"maxLatE6": -24987688, "minLngE6": 150042311, "maxLngE6": 180021223, "minLatE6": -54913877}	test
132	{"minLatE6": 42567670, "maxLngE6": 22526495, "minLngE6": 15031767, "maxLatE6": 50049217}	test
142	{"minLngE6": 30042311, "maxLatE6": 42567670, "minLatE6": 35086123, "maxLngE6": 37537039}	test
151	{"minLngE6": 37537039, "maxLatE6": 57530764, "minLatE6": 50049217, "maxLngE6": 45031767}	test
160	{"minLatE6": 35086123, "maxLngE6": -97473505, "maxLatE6": 42567670, "minLngE6": -104968233}	test
169	{"minLatE6": 50049217, "maxLngE6": -89978777, "maxLatE6": 57530764, "minLngE6": -97473505}	test
178	{"minLngE6": -89957689, "maxLatE6": 50049217, "minLatE6": 42567670, "maxLngE6": -82462961}	test
187	{"minLngE6": -82462961, "maxLatE6": 65012312, "minLatE6": 57530764, "maxLngE6": -74968233}	test
52	{"maxLatE6": 5012312, "minLngE6": -119957689, "maxLngE6": -89978777, "minLatE6": -24913877}	test
70	{"maxLatE6": 5012312, "minLngE6": -29957689, "maxLngE6": 21223, "minLatE6": -24913877}	test
88	{"maxLatE6": 5012312, "minLngE6": 60042311, "maxLngE6": 90021223, "minLatE6": -24913877}	test
106	{"maxLatE6": 5012312, "minLngE6": 150042311, "maxLngE6": 180021223, "minLatE6": -24913877}	test
133	{"minLatE6": 42567670, "maxLngE6": 30021223, "minLngE6": 22526495, "maxLatE6": 50049217}	test
143	{"minLngE6": 37537039, "maxLatE6": 42567670, "minLatE6": 35086123, "maxLngE6": 45031767}	test
152	{"minLngE6": 45031767, "maxLatE6": 57530764, "minLatE6": 50049217, "maxLngE6": 52526495}	test
161	{"minLatE6": 35086123, "maxLngE6": -89978777, "maxLatE6": 42567670, "minLngE6": -97473505}	test
170	{"minLatE6": 57530764, "maxLngE6": -112462961, "maxLatE6": 65012312, "minLngE6": -119957689}	test
179	{"minLngE6": -82462961, "maxLatE6": 50049217, "minLatE6": 42567670, "maxLngE6": -74968233}	test
188	{"minLngE6": -74968233, "maxLatE6": 65012312, "minLatE6": 57530764, "maxLngE6": -67473505}	test
53	{"maxLatE6": 35012312, "minLngE6": -119957689, "maxLngE6": -89978777, "minLatE6": 5086123}	test
71	{"maxLatE6": 35012312, "minLngE6": -29957689, "maxLngE6": 21223, "minLatE6": 5086123}	test
89	{"maxLatE6": 35012312, "minLngE6": 60042311, "maxLngE6": 90021223, "minLatE6": 5086123}	test
107	{"maxLatE6": 35012312, "minLngE6": 150042311, "maxLngE6": 180021223, "minLatE6": 5086123}	test
134	{"minLatE6": 50049217, "maxLngE6": 7537039, "minLngE6": 42311, "maxLatE6": 57530764}	test
144	{"minLngE6": 45031767, "maxLatE6": 42567670, "minLatE6": 35086123, "maxLngE6": 52526495}	test
153	{"minLngE6": 52526495, "maxLatE6": 57530764, "minLatE6": 50049217, "maxLngE6": 60021223}	test
171	{"minLatE6": 57530764, "maxLngE6": -104968233, "maxLatE6": 65012312, "minLngE6": -112462961}	test
180	{"minLngE6": -74968233, "maxLatE6": 50049217, "minLatE6": 42567670, "maxLngE6": -67473505}	test
189	{"minLngE6": -67473505, "maxLatE6": 65012312, "minLatE6": 57530764, "maxLngE6": -59978777}	test
45	{"maxLatE6": -24987688, "minLngE6": -149957689, "maxLngE6": -119978777, "minLatE6": -54913877}	test
63	{"maxLatE6": -24987688, "minLngE6": -59957689, "maxLngE6": -29978777, "minLatE6": -54913877}	test
72	{"maxLatE6": 65012312, "minLngE6": -29957689, "maxLngE6": 21223, "minLatE6": 35086123}	test
81	{"maxLatE6": -24987688, "minLngE6": 30042311, "maxLngE6": 60021223, "minLatE6": -54913877}	test
90	{"maxLatE6": 65012312, "minLngE6": 60042311, "maxLngE6": 90021223, "minLatE6": 35086123}	test
99	{"maxLatE6": -24987688, "minLngE6": 120042311, "maxLngE6": 150021223, "minLatE6": -54913877}	test
108	{"maxLatE6": 65012312, "minLngE6": 150042311, "maxLngE6": 180021223, "minLatE6": 35086123}	test
126	{"minLatE6": 35086123, "maxLngE6": 7537039, "minLngE6": 42311, "maxLatE6": 42567670}	test
135	{"minLatE6": 50049217, "maxLngE6": 15031767, "minLngE6": 7537039, "maxLatE6": 57530764}	test
162	{"minLatE6": 42567670, "maxLngE6": -112462961, "maxLatE6": 50049217, "minLngE6": -119957689}	test
145	{"minLngE6": 52526495, "maxLatE6": 42567670, "minLatE6": 35086123, "maxLngE6": 60021223}	test
154	{"minLngE6": 30042311, "maxLatE6": 65012312, "minLatE6": 57530764, "maxLngE6": 37537039}	test
163	{"minLatE6": 42567670, "maxLngE6": -104968233, "maxLatE6": 50049217, "minLngE6": -112462961}	test
172	{"minLatE6": 57530764, "maxLngE6": -97473505, "maxLatE6": 65012312, "minLngE6": -104968233}	test
181	{"minLngE6": -67473505, "maxLatE6": 50049217, "minLatE6": 42567670, "maxLngE6": -59978777}	test
191	{"maxLngE6": -119978777, "minLatE6": 65086123, "minLngE6": -179957689, "maxLatE6": 78000000}	test
46	{"maxLatE6": 5012312, "minLngE6": -149957689, "maxLngE6": -119978777, "minLatE6": -24913877}	test
64	{"maxLatE6": 5012312, "minLngE6": -59957689, "maxLngE6": -29978777, "minLatE6": -24913877}	test
82	{"maxLatE6": 5012312, "minLngE6": 30042311, "maxLngE6": 60021223, "minLatE6": -24913877}	test
100	{"maxLatE6": 5012312, "minLngE6": 120042311, "maxLngE6": 150021223, "minLatE6": -24913877}	test
127	{"minLatE6": 35086123, "maxLngE6": 15031767, "minLngE6": 7537039, "maxLatE6": 42567670}	test
136	{"minLatE6": 50049217, "maxLngE6": 22526495, "minLngE6": 15031767, "maxLatE6": 57530764}	test
146	{"minLngE6": 30042311, "maxLatE6": 50049217, "minLatE6": 42567670, "maxLngE6": 37537039}	test
155	{"minLngE6": 37537039, "maxLatE6": 65012312, "minLatE6": 57530764, "maxLngE6": 45031767}	test
164	{"minLatE6": 42567670, "maxLngE6": -97473505, "maxLatE6": 50049217, "minLngE6": -104968233}	test
173	{"minLatE6": 57530764, "maxLngE6": -89978777, "maxLatE6": 65012312, "minLngE6": -97473505}	test
182	{"minLngE6": -89957689, "maxLatE6": 57530764, "minLatE6": 50049217, "maxLngE6": -82462961}	test
192	{"maxLngE6": -59978777, "minLatE6": 65086123, "minLngE6": -119957689, "maxLatE6": 78000000}	test
47	{"maxLatE6": 35012312, "minLngE6": -149957689, "maxLngE6": -119978777, "minLatE6": 5086123}	test
65	{"maxLatE6": 35012312, "minLngE6": -59957689, "maxLngE6": -29978777, "minLatE6": 5086123}	test
83	{"maxLatE6": 35012312, "minLngE6": 30042311, "maxLngE6": 60021223, "minLatE6": 5086123}	test
101	{"maxLatE6": 35012312, "minLngE6": 120042311, "maxLngE6": 150021223, "minLatE6": 5086123}	test
128	{"minLatE6": 35086123, "maxLngE6": 22526495, "minLngE6": 15031767, "maxLatE6": 42567670}	test
137	{"minLatE6": 50049217, "maxLngE6": 30021223, "minLngE6": 22526495, "maxLatE6": 57530764}	test
\.


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hunter
--

SELECT pg_catalog.setval('tasks_id_seq', 199, true);


--
-- Name: tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: hunter
--

ALTER TABLE ONLY tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

