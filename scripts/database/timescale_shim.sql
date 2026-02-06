-- Shim for TimescaleDB functions on standard Postgres
CREATE OR REPLACE FUNCTION create_hypertable(
    relation REGCLASS,
    dimension_column_name NAME,
    chunking_column_name NAME = NULL,
    number_partitions INTEGER = NULL,
    associated_schema_name NAME = NULL,
    associated_table_prefix NAME = NULL,
    chunk_time_interval ANYELEMENT = NULL,
    create_default_indexes BOOLEAN = TRUE,
    if_not_exists BOOLEAN = FALSE,
    partitioning_column NAME = NULL,
    partitioning_func REGPROC = NULL,
    migrate_data BOOLEAN = FALSE
) RETURNS TABLE (hypertable_id INTEGER, schema_name NAME, table_name NAME, created BOOLEAN) AS $$
BEGIN
    RETURN QUERY SELECT 0, 'public'::NAME, relation::NAME, FALSE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION time_bucket(bucket_width INTERVAL, ts TIMESTAMPTZ) RETURNS TIMESTAMPTZ AS $$
BEGIN
    RETURN date_trunc('day', ts);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Simplified first/last aggregates (not ordered, but avoids syntax errors)
CREATE OR REPLACE FUNCTION first_sfunc(anyelement, anyelement, anyelement)
RETURNS anyelement AS 'SELECT COALESCE($1, $2)' LANGUAGE SQL IMMUTABLE;

CREATE OR REPLACE AGGREGATE first(anyelement, anyelement) (
    SFUNC = first_sfunc,
    STYPE = anyelement
);

CREATE OR REPLACE FUNCTION last_sfunc(anyelement, anyelement, anyelement)
RETURNS anyelement AS 'SELECT $2' LANGUAGE SQL IMMUTABLE;

CREATE OR REPLACE AGGREGATE last(anyelement, anyelement) (
    SFUNC = last_sfunc,
    STYPE = anyelement
);
