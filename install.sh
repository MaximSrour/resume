export MYSQLCLIENT_CFLAGS=`pkg-config mysqlclient --cflags`
export MYSQLCLIENT_LDFLAGS=`pkg-config mysqlclient --libs`

sudo apt-get update -y

sudo apt-get install -y pkg-config
sudo apt-get install -y build-essential

sudo apt-get install -y python3-dev
sudo apt-get install -y python3.10-dev
sudo apt-get install -y python3.11-dev

sudo apt-get install -y libmysqlclient-dev
sudo apt-get install -y default-libmysqlclient-dev

sudo apt-get install -y texlive-latex-base
sudo apt-get install -y texlive-fonts-recommended
sudo apt-get install -y texlive-fonts-extra
sudo apt-get install -y texlive-latex-extra

sudo apt-get install -y texlive-xetex

pip install mysqlclient python-dotenv

#sudo cp ./Geist/Geist-Regular.otf /usr/share/fonts/truetype/
#sudo cp ./Geist/Geist-Bold.otf /usr/share/fonts/truetype/
#sudo fc-cache -f -v
