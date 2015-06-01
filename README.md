# Reporty
Command line tool for logging work with the Reportronic project management software

## INSTALLATION
```
npm install -g phantomjs && pip install -r requirements.txt
```

## USAGE
```
Usage: reporty.py [OPTIONS]

  Command line tool for interacting with Reportronic

Options:
  --date TEXT    Work date. Default is today
  --desc TEXT    Work description.
  --hours FLOAT  Working hours.
  --help         Show this message and exit.
```

So for example:

```
python reporty.py --desc 'Fix bugs, write documentation' --hours 7.25

```
Remember to set your username and password in config.json...
