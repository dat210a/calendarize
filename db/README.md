# calendarize database
This contains the schema for the database, and once the database is complete, or mostly complete, 
also tools to populate and test it.

Current overview of the database:

```
calendarize_db
├── users
│   ├── user_id [INT(11)]
│   ├── user_type [INT(11)]
│   ├── user_name [VARCHAR(45)]
│   ├── user_email [VARCHAR(45)]
│   ├── user_phone [INT(11)]
│   ├── user_role [VARCHAR(45)]
│   ├── user_password [VARCHAR(45)]
│   ├── user_friends [VARCHAR(45)]
│   ├── user_calendars [VARCHAR(45)]
│   ├── user_events [VARCHAR(45)]
│   ├── user_extra [VARCHAR(45)]
│   └── deleted [INT(11)]
├── userconfig
│   ├── user_config_id [INT(11)]
│   ├── user_config_password [VARCHAR(45)]
│   └── user_config_extra [VARCHAR(45)]
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
│   ├── calendar_events [VARCHAR(45)]
│   ├── calendar_admins [VARCHAR(45)]
│   └── deleted [INT(11)]
└── events
    ├── event_id [INT(11)]
    ├── event_name [VARCHAR(45)]
    ├── event_date_created [DATE]
    ├── event_details [VARCHAR(45)]
    ├── event_location [VARCHAR(45)]
    ├── event_start [DATE]
    ├── event_end [DATE]
    ├── event_time [VARCHAR(45)]
    ├── event_members [VARCHAR(45)]
    ├── event_belongs_to [VARCHAR(45)]
    ├── event_extra [VARCHAR(45)]
    └── deleted [INT(11)]
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