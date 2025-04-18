
DROP TABLE IF EXISTS bcbdb.prod.port_tonnage;

create table bcbdb.prod.port_tonnage as (
    select distinct
        pp.port,
        pp.port_name,
        pp.total as total_tonnage,
        bc.latitude,
        bc.longitude,
        cast(pp.foreign_ as FLOAT) / cast(pp.total as FLOAT) as foreign_pct,
        cast(pp.domestic as FLOAT) / cast(pp.total as FLOAT) as domestic_pct,
        cast(pp.imports as FLOAT) / cast(pp.total as FLOAT) as import_pct,
        cast(pp.exports as FLOAT) / cast(pp.total as FLOAT) as export_pct,
        case foreign_pct
            when between 0 and 0.2 then '0-20%'
            when between 0.2 and 0.4 then '20-40%'
            when between 0.4 and 0.6 then '40-60%'
            when between 0.6 and 0.8 then '60-80%'
            when between 0.8 and 1 then '80-100%'
        end as binned_foreign_pct,
        case domestic_pct
            when between 0 and 0.2 then '0-20%'
            when between 0.2 and 0.4 then '20-40%'
            when between 0.4 and 0.6 then '40-60%'
            when between 0.6 and 0.8 then '60-80%'
            when between 0.8 and 1 then '80-100%'
        end as binned_domestic_pct,
        case import_pct
            when between 0 and 0.2 then '0-20%'
            when between 0.2 and 0.4 then '20-40%'
            when between 0.4 and 0.6 then '40-60%'
            when between 0.6 and 0.8 then '60-80%'
            when between 0.8 and 1 then '80-100%'
        end as binned_import_pct,
        case export_pct
            when between 0 and 0.2 then '0-20%'
            when between 0.2 and 0.4 then '20-40%'
            when between 0.4 and 0.6 then '40-60%'
            when between 0.6 and 0.8 then '60-80%'
            when between 0.8 and 1 then '80-100%'
        end as binned_export_pct
    from
        bcbdb.public.principal_ports pp
        join bcbdb.public.border_crossings bc on pp.port = bc.port_code
);

DROP TABLE IF EXISTS bcbdb.prod.port_monthly_traffic;

create table bcbdb.prod.port_monthly_traffic as (
    select
        port_name,
        port_code,
        to_date(date, 'Mon YYYY') as month_year,
        measure as cargo_type,
        sum(value) as monthly_count
    from
        border_crossings
    group by
        1,
        2,
        3,
        4
);

DROP TABLE IF EXISTS bcbdb.prod.port_description;

create table bcbdb.prod.port_description as (
    select
        pp.port_name as long_name,
        bc.port_name as short_name,
        bc.state,
        bc.port_code
    from
        bcbdb.public.border_crossings bc
        join bcbdb.public.principal_ports pp on bc.port_code = pp.port
);