# Pardal

An acessible and customizable Twitter client

[![Build Status](https://dev.azure.com/apgomes88/apgomes88/_apis/build/status/anapaulagomes.pardal)](https://dev.azure.com/apgomes88/apgomes88/_build/latest?definitionId=1)

## Using it (Proof of Concept yet)

This is a proof of concept. It means that this project is experimental and currently
is testing what is possible to be done. Don't expect much. :) Feel free to contribute
on coding or testing it.

Run `pardal` executable as administrator. You can configure your keyboard editing the file
`keyboard.ini`.

Errors should be logged on `pardal.log` (available on same folder as the executable file).

* Supported Systems

- Linux (Antergos)
- MacOS (HighSierra)
- Windows (Win 10)

## Development

Requirements:

- Python 3.7

**IMPORTANT**: Pardal must be running using `sudo`/`administrator mode`.

### Virtual environment (optional)

We recommend using a virtual environment:

```
python -m venv venv

source venv/bin/activate
```

### Environment variables (optional)

You must be able of testing it without any problems even if no consumer key or secret are filled in.

If you'd like to test it using real data copy `.env.sample` to `.env` and replace with the values of a Twitter APP.

```
export CONSUMER_KEY=xxxx
export CONSUMER_SECRET=eeee
export FAKE_TWITTER_API=False  # default: True
```

### Dependencies

Some dependencies are specific of each operating system.

Install the general dependencies:

```
make install
```

You must install [python-espeak](https://github.com/relsi/python-espeak) or `espeak` on our OS as well.

- Linux

`sudo apt-get install -y espeak`

- MacOs

`brew install espeak`
`pip install -U pyobjc`

- Windows

`pip install -U pypiwin32`

### Initializing the database

Init the db:

```
make init-db
```

### Running the services

Run final piece of Pardal:

```
sudo make run
```

## TODO

- [ ] Config on .spec instead of Makefile: https://stackoverflow.com/a/23597180/1344295
- [ ] Check current bugs
- [ ] Check Sentry DSN being public
- [ ] Add build to Azure (generating version)
- [ ] Check if is possible to publish generated version
when merged with dev

## Troubleshooting

* `OSError: libespeak.so.1: cannot open shared object file: No such file or directory`

You must install [python-espeak](https://github.com/relsi/python-espeak) or `espeak` on our OS.

* ModuleNotFound error on MacOS?

Check your `PYTHONPATH` configuration. How to solve it [here](https://stackoverflow.com/a/27605646/1344295).

* `pyconfig.h could not be extracted!` on MacOS?

```
../../../include/python3.7m/pyconfig.h could not be extracted!
fopen: No such file or directory
```

Try to run the executable as sudo.
