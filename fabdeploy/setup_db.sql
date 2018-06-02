ALTER USER {{DB_USER}} CREATEDB;
ALTER USER {{DB_USER}} SET client_encoding TO 'utf8';
ALTER USER {{DB_USER}} SET default_transaction_isolation TO 'read committed';
ALTER USER {{DB_USER}} SET timezone TO 'UTC';

