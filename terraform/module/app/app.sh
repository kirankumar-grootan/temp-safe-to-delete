set -e

sudo apt update
sudo apt upgrade -y
sudo apt install nginx

sudo systemctl enable nginx

sudo echo "<h1>Hello World</h1>" > /var/www/html/index.html
sudo systemctl restart nginx
