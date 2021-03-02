# erp-warrior
A script to help automate submitting monthly time sheets tracked in timewarrior using tags

## Config
Located in `~/.config/erp-warrior/config.json`

Format:
```json
{
  "smtp_server": "",
  "smtp_port": 0,
  "smtp_login": "",
  "smtp_password_pass_identity": "",
  "sender_email": "",
  "sender_name": "",
  "reply_to": "",
  "categories": [
    {
      "tag": "tag to filter by",
      "code": "Budget claim code",
      "auth": "Statment to put in code {} is replaced by the current date in YYYY-MM-DD format"
    }
  ]
}
```

## Auto send mail
The first 7 fields relate to the `sendmail.py` script.
This script is used to send a tabulated list of the hours done to each unit director

`smtp_password_pass_identity` is the identity named used to reference the password in `pass`
