curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt install nodejs
npm install pm2@latest -g
virtualenv env -p python3
env/bin/pip install -r requirements.txt
env/bin/python manage.py migrate
sudo ufw allow 21/tcp
sudo ufw allow 8000/tcp
