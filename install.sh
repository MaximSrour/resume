sudo apt-get update -y
sudo apt-get install pkg-config -y
export MYSQLCLIENT_CFLAGS=`pkg-config mysqlclient --cflags`
export MYSQLCLIENT_LDFLAGS=`pkg-config mysqlclient --libs`
sudo apt install python3-dev default-libmysqlclient-dev build-essential -y
sudo apt-get install python3-dev python3.10-dev python3.11-dev libmysqlclient-dev -y
pip install mysqlclient python-dotenv
sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra -y

