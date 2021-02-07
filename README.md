# erp-warrior
A script to help automate submitting monthly time sheets tracked in timewarrior using tags

## Config
Located in `~/.config/erp-warrior/config.json`

Format:
```json
{
  "categories": [
    {
      "tag": "tag to filter by",
      "code": "Budget claim code",
      "auth": "Statment to put in code {} is replaced by the current date in YYYY-MM-DD format"
    }
  ]
}
```
