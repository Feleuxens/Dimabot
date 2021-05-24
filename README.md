[![DeepSource](https://deepsource.io/gh/Feleuxens/Dimabot.svg/?label=active+issues)](https://deepsource.io/gh/Feleuxens/Dimabot/?ref=repository-badge)
# Dimabot
Discord Bot for the server of vDimatrix

## How to add the bot to a server?
Currently, the bot does not support multiple servers and won't until some neccessary 
features are implemented. Feel free to host it yourself.

Note: If you want to host it yourself you might need to change some hardcoded ids.


## Development
### Requirements

- [Python](https://www.python.org/) >=3.8 (you might need to adjust the Python version in the Pipfile)
- [Pipenv](https://pypi.org/project/pipenv/)
- [Git](https://git-scm.com/)

### Cloning the repository

#### SSH
```
git clone git@github.com:Feleuxens/Dimabot.git
```
#### HTTPS
```
git clone https://github.com/Feleuxens/Dimabot.git
```
#### Using GitHub CLI
```
gh repo clone Feleuxens/Dimabot
```

### Install dependencies
This project uses Pipenv for virtual environments. After cloning the repository 
you can set up the environment with `pipenv install`. Be sure to be in the root folder
of this project.

### Changing variables
The enivronment variables are loaded using dotenv. For this you need to create a file
named `.env` (see `sample.env`). A list of all [environment variables](#environment-variables)
is listed below.

### Structure
The Bot is split into different parts. The Bot itself has a few core modules and 
utilities located in the [utils subdfolder](dimabot/utils) and extensions with 
hot-swapping support (you can change code and reload them without restarting the
whole programm) located in the [extensions subfolder](dimabot/extensions).

# Installation
Docker support isn't added yet. For now, you can clone the repository and run it in 
a [screen session](https://linuxize.com/post/how-to-use-linux-screen/) (if you don't
want this just ignore the first command).
```shell
session -S dimabot
cd path/to/Dimabot-root
pipenv shell
python dimabot/main.py
```

# Environment variables
| Variable | Description | Required? | Default |
| :--- | :--- | :---: | :--- |
| TOKEN | Discord Bot Token | :heavy_check_mark: |
| VERBOSITY | Verbosity of console output. Possible values are `DEBUG`, `INFO`, `WARNING`, `ERROR` and `CRITICAL`. [See](https://discordpy.readthedocs.io/en/latest/logging.html) for more information. | :heavy_multiplication_x: | `INFO` |
| | | | |
| SENTRY_DSN | [Sentry DSN](https://docs.sentry.io/product/sentry-basics/dsn-explainer/) if you want to track errors with SENTRY | :heavy_multiplication_x: | |
| SENTRY_ENVIRONMENT | If you're using Sentry you can specify environment like `dev`, `production`, etc. | :heavy_multiplication_x: | `dev` |
