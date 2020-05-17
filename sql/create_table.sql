-- Table: public.nse_cash_daily

-- DROP TABLE public.nse_cash_daily;

CREATE TABLE public.nse_cash_daily
(
    trade_date date NOT NULL,
    stock_id integer NOT NULL,
    stock_code character varying(50) COLLATE pg_catalog."default",
    series character varying(50) COLLATE pg_catalog."default",
    prev_close real,
    open real,
    high real,
    low real,
    close real,
    volume numeric,
    vwap real,
    trades integer,
    deliverable_volume numeric,
    percentage_delivery real,
    CONSTRAINT nse_daily_pkey PRIMARY KEY (trade_date, stock_id)
)

TABLESPACE pg_default;

ALTER TABLE public.nse_cash_daily
    OWNER to postgres;


-- Table: public.nse_fno_daily

-- DROP TABLE public.nse_fno_daily;

CREATE TABLE public.nse_fno_daily
(
    stock_id integer NOT NULL,
    trade_date date NOT NULL,
    stock_code character varying(50) COLLATE pg_catalog."default",
    expiry_date date NOT NULL,
    open real,
    high real,
    low real,
    close real,
    last_price real,
    settle_price real,
    no_of_contracts numeric,
    open_interest numeric,
    change_in_oi real,
    underlying real,
    CONSTRAINT nse_fno_pkey PRIMARY KEY (trade_date, stock_id, expiry_date)
)

TABLESPACE pg_default;

ALTER TABLE public.nse_fno_daily
    OWNER to postgres;

-- Table: public.nse_stock_option_daily

-- DROP TABLE public.nse_stock_option_daily;

CREATE TABLE public.nse_stock_option_daily
(
    stock_id integer NOT NULL,
    trade_date date,
    stock_code character varying(50) COLLATE pg_catalog."default",
    strike_price real NOT NULL,
    option_type character varying(10) COLLATE pg_catalog."default" NOT NULL,
    expiry_date date NOT NULL,
    identifier character varying(50) COLLATE pg_catalog."default",
    open_interest numeric,
    change_in_oi numeric,
    percent_change_in_oi real,
    total_traded_volume numeric,
    implied_volatility real,
    last_price real,
    change real,
    total_buy_quantity numeric,
    total_sell_quantity numeric,
    underlying_value real,
    CONSTRAINT nse_stock_option_daily_pkey PRIMARY KEY (stock_id, expiry_date, strike_price, option_type)
)

TABLESPACE pg_default;

ALTER TABLE public.nse_stock_option_daily
    OWNER to postgres;

-- Table: public.stock_list

-- DROP TABLE public.stock_list;

CREATE TABLE public.stock_list
(
    stock_id integer NOT NULL DEFAULT nextval('stock_list_stock_id_seq'::regclass),
    stock_code character varying(50) COLLATE pg_catalog."default",
    stock_description character varying(100) COLLATE pg_catalog."default",
    nifty50 boolean,
    nifty100 boolean,
    nifty500 boolean,
    downloaded boolean DEFAULT false,
    fno boolean DEFAULT false,
    indices boolean DEFAULT false
)

TABLESPACE pg_default;

ALTER TABLE public.stock_list
    OWNER to postgres;