gosu postgres psql --dbname template1 <<EOSQL
    DROP DATABASE postgres;

    CREATE DATABASE bentham TEMPLATE template1;
EOSQL
