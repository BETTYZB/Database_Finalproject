-- Run this after you've created tables and loaded PostgreSQL CLI

\COPY investors FROM 'data/investor_export' WITH CSV HEADER;
\COPY entrepreneurs FROM 'data/entrepreneur_export' WITH CSV HEADER;
\COPY investments FROM 'data/investment_export' WITH CSV HEADER;
