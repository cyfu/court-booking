brew install pyenv
pyenv install --list
pyenv install 3.11.7
curl -sSL https://install.python-poetry.org | python3 -
poetry init
poetry config virtualenvs.create true --local
poetry install
git init
git branch -m main
gh repo create --public --source .
git add .
git commit -m "Initial commit"
git push --set-upstream origin main