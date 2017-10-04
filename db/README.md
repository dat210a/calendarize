# calendarize database
This contains the schema for the database, and once the database is complete, or mostly complete, 
also tools to populate and test it.

Current overview of the database:

```
calendarize_db
├── users
│   ├── UserID [INT(11)]
│   ├── UserType [INT(11)]
│   ├── UserName [VARCHAR(45)]
│   ├── UserEmail [VARCHAR(45)]
│   ├── UserPhone [INT(11)]
│   ├── UserRole [VARCHAR(45)]
│   ├── UserPassword [VARCHAR(45)]
│   ├── UserFriendList [VARCHAR(45)]
│   ├── UserCalendars [VARCHAR(45)]
│   ├── UserSubscribedToThisCalendar [VARCHAR(45)]
│   ├── UserEvents [VARCHAR(45)]
│   ├── UserExtra [VARCHAR(45)]
│   └── deleted [INT(11)]
├── userconfig
│   ├── UserConfigID [INT(11)]
│   ├── UserConfigPassword [VARCHAR(45)]
│   └── UserConfigExtra [VARCHAR(45)]
├── calendars
│   ├── calendarID [INT(11)]
│   ├── calendarName [VARCHAR(45)]
│   ├── calendarDateCreated [DATE]
│   ├── calendarDetails [VARCHAR(45)]
│   ├── calendarOwner [VARCHAR(45)]
│   ├── calendarMembers [VARCHAR(45)]
│   ├── calendarTime [INT(11)]
│   ├── calendarDay [INT(11)]
│   ├── calendarMonth [INT(11)]
│   ├── calendarYear [INT(11)]
│   ├── calendarExtra [VARCHAR(45)]
│   └── deleted [INT(11)]
└── events
    ├── EventID [INT(11)]
    ├── EventName [VARCHAR(45)]
    ├── EventDateCreated [DATE]
    ├── EventDetails [VARCHAR(45)]
    ├── EventLocation [VARCHAR(45)]
    ├── EventStart [DATE]
    ├── EventEnd [DATE]
    ├── EventTime [VARCHAR(45)]
    ├── EventMembers [VARCHAR(45)]
    ├── EventIsUnderThisCalendar [VARCHAR(45)]
    ├── EventExtra [VARCHAR(45)]
    └── deleted [INT(11)]
```

### TODO list for database
Expand this checklist as needed.
- [ ] Create appropriate foreign keys
- [ ] Change data-types for marked attributes
    - [ ] deleted to TINYINT(1)
- [ ] Conform naming across all tables
- [ ] Set necessary default values