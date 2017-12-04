# calendarize database
This contains the schema for the database, and once the database is complete, or mostly complete, 
also tools to populate and test it.

**NOTE** Below information not up to date...
Current overview of the database as found in the c_db_norm_0_2.sql file:  
Note: The unique_id is an auto-incrementing primary key that allows for proper foreign keys.  
Also note that foreign keys are not currently implemented.

```
calendarize_db
├── users
│   ├── user_id [INT(11)]
│   ├── user_type [INT(11)]
│   ├── user_name [VARCHAR(45)]
│   ├── user_email [VARCHAR(45)]
│   ├── user_phone [INT(11)]
│   ├── user_password [VARCHAR(45)]
│   ├── user_extra [VARCHAR(45)]
│   └── deleted [TINYINT(1)]
│
├── user_calendars
│   ├── user_id [INT]
│   ├── calendar_id [INT]
│   └── unique_id [INT]
│
├── user_friends
│   ├── user_id [INT]
│   ├── friend_id [INT]
│   └── unique_id [INT]
│
├── userconfig
│   ├── user_config_id [INT(11)]
│   ├── user_config_password [VARCHAR(45)]
│   └── user_config_extra [VARCHAR(45)]
│
├── calendars
│   ├── calendar_id [INT(11)]
│   ├── calendar_name [VARCHAR(45)]
│   ├── calendar_date_created [DATE]
│   ├── calendar_details [VARCHAR(45)]
│   ├── calendar_owner [VARCHAR(45)]
│   ├── calendar_members [VARCHAR(45)]
│   ├── calendar_time [INT(11)]
│   ├── calendar_day [INT(11)]
│   ├── calendar_month [INT(11)]
│   ├── calendar_year [INT(11)]
│   ├── calendar_extra [VARCHAR(45)]
│   └── deleted [TINYINT(1)]
│
├── calendar_events
│   ├── calendar_id [INT]
│   ├── event_id [INT]
│   └── unique_id [INT]
│
├── calendar_roles
│   ├── calendar_id [INT]
│   ├── role [INT]
│   ├── user_id [INT]
│   └── unique_id [INT]
│
├── event_files
│   ├── event_id [INT]
│   ├── file_name [VARCHAR(160)]
│   ├── recurring [TINYINT]
│   └── unique_id [INT]
│
├── event_recurrences
│   ├── event_id [INT]
│   ├── event_recurrence_no [BIGINT]
│   └── unique_id [INT]
│
└── events
    ├── event_id [INT(11)]
    ├── event_name [VARCHAR(45)]
    ├── event_date_created [DATE]
    ├── event_details [VARCHAR(45)]
    ├── event_location [VARCHAR(45)]
    ├── event_start [DATE]
    ├── event_end [DATE]
    ├── event_time [VARCHAR(45)]
    ├── event_extra [VARCHAR(45)]
    ├── recurring [INT]
    ├── recurrences [BIGINT]
    └── deleted [TINYINT(1)]
```

### TODO list for database
Expand this checklist as needed.
- [ ] Create appropriate foreign keys
- [ ] Change data-types for marked attributes
    - [x] deleted to TINYINT(1)
- [x] Conform naming across all tables
    - Naming changed to conform with pythonic variable names.
    - The prefix_ is unnecessary, but left in for now
- [ ] Set necessary default values
