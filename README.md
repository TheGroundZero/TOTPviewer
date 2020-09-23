# TOTPviewer

Display credentials and TOTP tokens of multiple accounts


## Usage

Create one or more CSV files containing the credentials

| username | password | totp       |
|----------|----------|------------|
|foobar    | Pa$$w0rd | TOTPsecret |

Execute the script:

```bash
chmod u+x TOTPviewer.py
./TOTPviewer.py -i creds.csv [creds2.csv creds3.csv ...]
```

Copy/paste credentials into the login form

------------------------- | --------------------------------- | -------- | -----
username                  | password                          |   totp   | timer
------------------------- | --------------------------------- | -------- | -----
foobar                    | Pa$$w0rd                          |  836015  |  10  


TOTP tokens refresh automatically

Use Ctrl+C to stop the script
