# TOTPviewer

Display credentials and TOTP tokens of multiple accounts

Works in different modes:

- `files`  
  Provide one or more CSV files with usernames (optional), passwords (optional) and TOTP secrets.
- `single`  
  Provide a single credentials via the command line (username (optional), password (optional) and TOTP secret)
- `show`  
  Prints and returns the current TOTP pin for the provided TOTP secret

```bash
$ ./TOTPviewer.py -h
usage: TOTPcodes [-h] {files,single,show} ...

Display TOTP tokens for multiple accounts

positional arguments:
  {files,single,show}  sub-command help
    files              files help
    single             single help
    show               show help

optional arguments:
  -h, --help           show this help message and exit
```

## Files

```bash
$ ./TOTPviewer.py files -h
usage: TOTPcodes files [-h] -i INPUT_FILES [INPUT_FILES ...]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILES [INPUT_FILES ...], --input INPUT_FILES [INPUT_FILES ...]
                        Input CSV file(s) with TOTP tokens
```

### CSV files

Create one or more CSV files containing the credentials

| username | password | totp       |
|----------|----------|------------|
| foobar   | Pa$$w0rd | TOTPsecret |
| johndoe  | hunter2  | TOTPsecret |

```csv
username,password,totp
foobar,Pa$$w0rd,TOTPsecret
```

Execute the script:

```bash
chmod u+x TOTPviewer.py
./TOTPviewer.py files -i creds.csv [creds2.csv creds3.csv ...]
```

Copy/paste credentials into the login form

username                  | password                          |   totp   | timer
------------------------- | --------------------------------- | -------- | -----
foobar                    | Pa$$w0rd                          |  836015  |  10  
johndoe                   | hunter2                           |  264830  |  10  


TOTP tokens refresh automatically

Use Ctrl+C to stop the script


## Single

Provide the username, password and TOTP secret for 1 account via parameters

```bash
$ ./TOTPviewer.py single -h
usage: TOTPcodes single [-h] [-u [USER]] [-p [PASSWORD]] -t [TOTP]

optional arguments:
  -h, --help            show this help message and exit
  -u [USER], --user [USER]
                        Username
  -p [PASSWORD], --pass [PASSWORD]
                        Password
  -t [TOTP], --totp [TOTP]
                        TOTP
```

```bash
./TOTPviewer.py single -u foobar -p Pa$$w0rd -t TOTP_SECRET
```

Copy/paste credentials into the login form

username                  | password                          |   totp   | timer
------------------------- | --------------------------------- | -------- | -----
foobar                    | Pa$$w0rd                          |  836015  |  10  


TOTP tokens refresh automatically

Use Ctrl+C to stop the script



## Show

Retrieve the current TOTP pin for a single TOTP secret

```bash
$ ./TOTPviewer.py show -h
usage: TOTPcodes show [-h] -t [TOTP]

optional arguments:
  -h, --help            show this help message and exit
  -t [TOTP], --totp [TOTP]
                        TOTP
```

```bash
./TOTPviewer.py show -t TOTP_SECRET

304925
```
