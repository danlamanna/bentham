gosu postgres psql --dbname template1 <<EOSQL
    DROP DATABASE postgres;

    CREATE EXTENSION hstore;
    CREATE DATABASE bentham TEMPLATE template1;
EOSQL
