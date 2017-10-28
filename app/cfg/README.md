# cfg
**Until further notice, this README.md should be the only file in this directory on GitHub.**  
There should be files here in your local dir, but for security purposes these should not be pushed to GitHub.  
  
Current cfg folder structure should look like this:


    cfg
    └── db.json
    └── mail.json
    
  
#### File structures
It is the responsibility of whoever creates the cfg files to make sure they're distributed to the team.  
Should you need to re-create one, the data structures will be listed below.
* db.json

    ```
    {
        "username": <username>,
        "password": <password>,
        "host": <host ip>,
        "database": <db name>
    }
    ```

* mail.json

    ```
    {
        "server": <mail server>,
        "PORT": <mail port>,
        "ssl": true,
        "tls": false,
        "username": <username>,
        "password": <password>,
    }
    ```
