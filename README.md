## Setup Python
1. `brew install asdf`
2. `asdf plugin-add python`
3. `asdf global system`
3. `asdf install $(grep python .tool-versions)`
## Setup virtual environment
1. `sudo pip install virtualenv` (virtualenvwrapper cant find virtualenv if sudo not used...)
2.`python3 -m venv plant-env`
## Setup direnv
1. `brew install direnv`
2. `echo "eval "$(direnv hook zsh)" >> ~/.zshrc && source ~/.zshrc`  
3. `direnv allow`
## Install dependencies
`pip install -r requirements.txt`
