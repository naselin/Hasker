--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE hasker;
ALTER ROLE hasker WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'md58e95863b42897a11e4ff17463717a758';
CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS;






--
-- Database creation
--

CREATE DATABASE hasker WITH TEMPLATE = template0 OWNER = postgres;
GRANT ALL ON DATABASE hasker TO hasker;
REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


\connect hasker

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 10.6
-- Dumped by pg_dump version 10.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
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


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO hasker;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO hasker;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO hasker;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO hasker;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO hasker;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO hasker;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO hasker;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO hasker;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO hasker;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO hasker;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO hasker;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO hasker;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO hasker;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO hasker;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO hasker;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO hasker;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO hasker;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO hasker;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO hasker;

--
-- Name: qna_answer; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.qna_answer (
    id integer NOT NULL,
    text text NOT NULL,
    post_time timestamp with time zone NOT NULL,
    rating integer NOT NULL,
    author_id integer NOT NULL,
    question_id integer NOT NULL
);


ALTER TABLE public.qna_answer OWNER TO hasker;

--
-- Name: qna_answer_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.qna_answer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.qna_answer_id_seq OWNER TO hasker;

--
-- Name: qna_answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.qna_answer_id_seq OWNED BY public.qna_answer.id;


--
-- Name: qna_question; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.qna_question (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    text text NOT NULL,
    post_time timestamp with time zone NOT NULL,
    slug character varying(200) NOT NULL,
    num_answers integer NOT NULL,
    rating integer NOT NULL,
    author_id integer NOT NULL,
    correct_answer_id integer,
    CONSTRAINT qna_question_num_answers_check CHECK ((num_answers >= 0))
);


ALTER TABLE public.qna_question OWNER TO hasker;

--
-- Name: qna_question_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.qna_question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.qna_question_id_seq OWNER TO hasker;

--
-- Name: qna_question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.qna_question_id_seq OWNED BY public.qna_question.id;


--
-- Name: qna_question_tags; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.qna_question_tags (
    id integer NOT NULL,
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.qna_question_tags OWNER TO hasker;

--
-- Name: qna_question_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.qna_question_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.qna_question_tags_id_seq OWNER TO hasker;

--
-- Name: qna_question_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.qna_question_tags_id_seq OWNED BY public.qna_question_tags.id;


--
-- Name: qna_tag; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.qna_tag (
    id integer NOT NULL,
    tag_text character varying(30) NOT NULL
);


ALTER TABLE public.qna_tag OWNER TO hasker;

--
-- Name: qna_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.qna_tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.qna_tag_id_seq OWNER TO hasker;

--
-- Name: qna_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.qna_tag_id_seq OWNED BY public.qna_tag.id;


--
-- Name: qna_vote; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.qna_vote (
    id integer NOT NULL,
    activity_type character varying(1) NOT NULL,
    object_id integer NOT NULL,
    content_type_id integer NOT NULL,
    user_id integer NOT NULL,
    CONSTRAINT qna_vote_object_id_check CHECK ((object_id >= 0))
);


ALTER TABLE public.qna_vote OWNER TO hasker;

--
-- Name: qna_vote_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.qna_vote_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.qna_vote_id_seq OWNER TO hasker;

--
-- Name: qna_vote_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.qna_vote_id_seq OWNED BY public.qna_vote.id;


--
-- Name: users_haskeruser; Type: TABLE; Schema: public; Owner: hasker
--

CREATE TABLE public.users_haskeruser (
    id integer NOT NULL,
    avatar character varying(100),
    user_id integer NOT NULL
);


ALTER TABLE public.users_haskeruser OWNER TO hasker;

--
-- Name: users_haskeruser_id_seq; Type: SEQUENCE; Schema: public; Owner: hasker
--

CREATE SEQUENCE public.users_haskeruser_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_haskeruser_id_seq OWNER TO hasker;

--
-- Name: users_haskeruser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hasker
--

ALTER SEQUENCE public.users_haskeruser_id_seq OWNED BY public.users_haskeruser.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: qna_answer id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_answer ALTER COLUMN id SET DEFAULT nextval('public.qna_answer_id_seq'::regclass);


--
-- Name: qna_question id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_question ALTER COLUMN id SET DEFAULT nextval('public.qna_question_id_seq'::regclass);


--
-- Name: qna_question_tags id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_question_tags ALTER COLUMN id SET DEFAULT nextval('public.qna_question_tags_id_seq'::regclass);


--
-- Name: qna_tag id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_tag ALTER COLUMN id SET DEFAULT nextval('public.qna_tag_id_seq'::regclass);


--
-- Name: qna_vote id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_vote ALTER COLUMN id SET DEFAULT nextval('public.qna_vote_id_seq'::regclass);


--
-- Name: users_haskeruser id; Type: DEFAULT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.users_haskeruser ALTER COLUMN id SET DEFAULT nextval('public.users_haskeruser_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add vote	1	add_vote
2	Can change vote	1	change_vote
3	Can delete vote	1	delete_vote
4	Can add question	2	add_question
5	Can change question	2	change_question
6	Can delete question	2	delete_question
7	Can add answer	3	add_answer
8	Can change answer	3	change_answer
9	Can delete answer	3	delete_answer
10	Can add tag	4	add_tag
11	Can change tag	4	change_tag
12	Can delete tag	4	delete_tag
13	Can add hasker user	5	add_haskeruser
14	Can change hasker user	5	change_haskeruser
15	Can delete hasker user	5	delete_haskeruser
16	Can add log entry	6	add_logentry
17	Can change log entry	6	change_logentry
18	Can delete log entry	6	delete_logentry
19	Can add group	7	add_group
20	Can change group	7	change_group
21	Can delete group	7	delete_group
22	Can add permission	8	add_permission
23	Can change permission	8	change_permission
24	Can delete permission	8	delete_permission
25	Can add user	9	add_user
26	Can change user	9	change_user
27	Can delete user	9	delete_user
28	Can add content type	10	add_contenttype
29	Can change content type	10	change_contenttype
30	Can delete content type	10	delete_contenttype
31	Can add session	11	add_session
32	Can change session	11	change_session
33	Can delete session	11	delete_session
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
3	pbkdf2_sha256$36000$jKdB8kIcqKER$8NBihIhKOInya07sKvDyJVc79ZE+a7BbnP/Pf6Q4CvE=	2019-11-06 14:43:26.766556+00	f	Fry			fry@selin.com.ru	f	t	2019-11-06 14:43:26.684515+00
2	pbkdf2_sha256$36000$i2SzGQtckCJU$MtH+v4pNV6CqSpDg4sajlj3a1l6gSC7NQCuVua+ju9g=	2019-11-06 14:48:49.58125+00	f	Leela			leela@selin.com.ru	f	t	2019-11-06 14:42:53.66989+00
1	pbkdf2_sha256$36000$HDSQENSKEjkt$F9Qr5Cy0+F9T3rCEerCAoYr1iLRwQafnd1xhS1yip50=	2019-11-06 14:49:27.148722+00	f	Hermes			hermes@selin.com.ru	f	t	2019-11-06 14:42:21.371676+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	qna	vote
2	qna	question
3	qna	answer
4	qna	tag
5	users	haskeruser
6	admin	logentry
7	auth	group
8	auth	permission
9	auth	user
10	contenttypes	contenttype
11	sessions	session
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2019-11-06 11:54:41.58709+00
2	auth	0001_initial	2019-11-06 11:54:41.671764+00
3	admin	0001_initial	2019-11-06 11:54:41.700631+00
4	admin	0002_logentry_remove_auto_add	2019-11-06 11:54:41.719192+00
5	contenttypes	0002_remove_content_type_name	2019-11-06 11:54:41.752202+00
6	auth	0002_alter_permission_name_max_length	2019-11-06 11:54:41.763261+00
7	auth	0003_alter_user_email_max_length	2019-11-06 11:54:41.781738+00
8	auth	0004_alter_user_username_opts	2019-11-06 11:54:41.796841+00
9	auth	0005_alter_user_last_login_null	2019-11-06 11:54:41.812003+00
10	auth	0006_require_contenttypes_0002	2019-11-06 11:54:41.814292+00
11	auth	0007_alter_validators_add_error_messages	2019-11-06 11:54:41.831997+00
12	auth	0008_alter_user_username_max_length	2019-11-06 11:54:41.876142+00
13	qna	0001_initial	2019-11-06 11:54:42.014763+00
14	sessions	0001_initial	2019-11-06 11:54:42.030338+00
15	users	0001_initial	2019-11-06 11:54:42.057415+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: qna_answer; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.qna_answer (id, text, post_time, rating, author_id, question_id) FROM stdin;
1	Answer #1	2019-11-06 14:48:38.907171+00	0	1	2
2	Ответ #2	2019-11-06 14:49:14.630925+00	0	2	2
\.


--
-- Data for Name: qna_question; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.qna_question (id, title, text, post_time, slug, num_answers, rating, author_id, correct_answer_id) FROM stdin;
1	Test #1	Test question #1.	2019-11-06 14:47:19.293025+00	test-1	0	1	1	\N
3	Test #3	New test question #3	2019-11-06 14:48:06.136928+00	test-3	0	-1	1	\N
2	Test #2	Question #2	2019-11-06 14:47:41.492842+00	test-2	2	1	1	2
\.


--
-- Data for Name: qna_question_tags; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.qna_question_tags (id, question_id, tag_id) FROM stdin;
1	1	1
2	2	2
3	3	1
4	3	2
5	3	3
\.


--
-- Data for Name: qna_tag; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.qna_tag (id, tag_text) FROM stdin;
1	tag1
2	tag2
3	tag3
\.


--
-- Data for Name: qna_vote; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.qna_vote (id, activity_type, object_id, content_type_id, user_id) FROM stdin;
1	U	1	2	1
2	U	2	2	1
3	D	3	2	1
\.


--
-- Data for Name: users_haskeruser; Type: TABLE DATA; Schema: public; Owner: hasker
--

COPY public.users_haskeruser (id, avatar, user_id) FROM stdin;
1	avatars/Hermes_Hermes..jpg	1
2	avatars/Leela_Leela..jpeg	2
3	avatars/default.png	3
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 33, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 3, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 11, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 15, true);


--
-- Name: qna_answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.qna_answer_id_seq', 2, true);


--
-- Name: qna_question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.qna_question_id_seq', 3, true);


--
-- Name: qna_question_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.qna_question_tags_id_seq', 5, true);


--
-- Name: qna_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.qna_tag_id_seq', 3, true);


--
-- Name: qna_vote_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.qna_vote_id_seq', 3, true);


--
-- Name: users_haskeruser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hasker
--

SELECT pg_catalog.setval('public.users_haskeruser_id_seq', 3, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: qna_answer qna_answer_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_answer
    ADD CONSTRAINT qna_answer_pkey PRIMARY KEY (id);


--
-- Name: qna_question qna_question_correct_answer_id_key; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_question
    ADD CONSTRAINT qna_question_correct_answer_id_key UNIQUE (correct_answer_id);


--
-- Name: qna_question qna_question_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_question
    ADD CONSTRAINT qna_question_pkey PRIMARY KEY (id);


--
-- Name: qna_question qna_question_slug_key; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_question
    ADD CONSTRAINT qna_question_slug_key UNIQUE (slug);


--
-- Name: qna_question_tags qna_question_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_question_tags
    ADD CONSTRAINT qna_question_tags_pkey PRIMARY KEY (id);


--
-- Name: qna_question_tags qna_question_tags_question_id_tag_id_30b172a6_uniq; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_question_tags
    ADD CONSTRAINT qna_question_tags_question_id_tag_id_30b172a6_uniq UNIQUE (question_id, tag_id);


--
-- Name: qna_tag qna_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_tag
    ADD CONSTRAINT qna_tag_pkey PRIMARY KEY (id);


--
-- Name: qna_vote qna_vote_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_vote
    ADD CONSTRAINT qna_vote_pkey PRIMARY KEY (id);


--
-- Name: users_haskeruser users_haskeruser_pkey; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.users_haskeruser
    ADD CONSTRAINT users_haskeruser_pkey PRIMARY KEY (id);


--
-- Name: users_haskeruser users_haskeruser_user_id_key; Type: CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.users_haskeruser
    ADD CONSTRAINT users_haskeruser_user_id_key UNIQUE (user_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: qna_answer_author_id_4f6db6b5; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX qna_answer_author_id_4f6db6b5 ON public.qna_answer USING btree (author_id);


--
-- Name: qna_answer_question_id_79273aeb; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX qna_answer_question_id_79273aeb ON public.qna_answer USING btree (question_id);


--
-- Name: qna_question_author_id_af82ee61; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX qna_question_author_id_af82ee61 ON public.qna_question USING btree (author_id);


--
-- Name: qna_question_slug_184e5ab0_like; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX qna_question_slug_184e5ab0_like ON public.qna_question USING btree (slug varchar_pattern_ops);


--
-- Name: qna_question_tags_question_id_a89e7bd0; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX qna_question_tags_question_id_a89e7bd0 ON public.qna_question_tags USING btree (question_id);


--
-- Name: qna_question_tags_tag_id_a8cc31d7; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX qna_question_tags_tag_id_a8cc31d7 ON public.qna_question_tags USING btree (tag_id);


--
-- Name: qna_vote_content_type_id_e9b46976; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX qna_vote_content_type_id_e9b46976 ON public.qna_vote USING btree (content_type_id);


--
-- Name: qna_vote_user_id_7effef33; Type: INDEX; Schema: public; Owner: hasker
--

CREATE INDEX qna_vote_user_id_7effef33 ON public.qna_vote USING btree (user_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: qna_answer qna_answer_author_id_4f6db6b5_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_answer
    ADD CONSTRAINT qna_answer_author_id_4f6db6b5_fk_auth_user_id FOREIGN KEY (author_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: qna_answer qna_answer_question_id_79273aeb_fk_qna_question_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_answer
    ADD CONSTRAINT qna_answer_question_id_79273aeb_fk_qna_question_id FOREIGN KEY (question_id) REFERENCES public.qna_question(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: qna_question qna_question_author_id_af82ee61_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_question
    ADD CONSTRAINT qna_question_author_id_af82ee61_fk_auth_user_id FOREIGN KEY (author_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: qna_question qna_question_correct_answer_id_e02724f1_fk_qna_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_question
    ADD CONSTRAINT qna_question_correct_answer_id_e02724f1_fk_qna_answer_id FOREIGN KEY (correct_answer_id) REFERENCES public.qna_answer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: qna_question_tags qna_question_tags_question_id_a89e7bd0_fk_qna_question_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_question_tags
    ADD CONSTRAINT qna_question_tags_question_id_a89e7bd0_fk_qna_question_id FOREIGN KEY (question_id) REFERENCES public.qna_question(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: qna_question_tags qna_question_tags_tag_id_a8cc31d7_fk_qna_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_question_tags
    ADD CONSTRAINT qna_question_tags_tag_id_a8cc31d7_fk_qna_tag_id FOREIGN KEY (tag_id) REFERENCES public.qna_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: qna_vote qna_vote_content_type_id_e9b46976_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_vote
    ADD CONSTRAINT qna_vote_content_type_id_e9b46976_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: qna_vote qna_vote_user_id_7effef33_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.qna_vote
    ADD CONSTRAINT qna_vote_user_id_7effef33_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_haskeruser users_haskeruser_user_id_700ed95c_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: hasker
--

ALTER TABLE ONLY public.users_haskeruser
    ADD CONSTRAINT users_haskeruser_user_id_700ed95c_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\connect postgres

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 10.6
-- Dumped by pg_dump version 10.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- PostgreSQL database dump complete
--

\connect template1

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 10.6
-- Dumped by pg_dump version 10.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE template1; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

