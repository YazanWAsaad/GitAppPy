::**************************************************************
echo Install pip
:: Install pip: https://pip.pypa.io/en/stable/installing/
c:
cd /
mkdir tmp
cd /tmp
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
py get-pip.py
::Install pip - installer application.
py -m pip install --upgrade pip
::Install python connector to git.
py -m pip install gitpython


:: Clone my repository.
git clone https://github.com/Danielli-Itai/GitApp.git



::**************************************************************
echo Install Matplot lib
::Install math plot library; https://matplotlib.org/users/installing.html
py -m pip install -U pip
py -m pip install -U matplotlib


::**************************************************************
:: Install SQL connector.
::py -m pip install -U mysql-connector-python
py -m pip install -U MySQL-python
::echo Install SQLAlchemy: https://pip.pypa.io/en/stable/installing/https://pypi.org/project/SQLAlchemy/1.3.0/#files
:: curl https://files.pythonhosted.org/packages/35/9e/5eb467ed50cdd8e88b808a7e65045020fa12b3b9c2ab51de0f452d269d4d/SQLAlchemy-1.3.0.tar.gz --output SQLAlchemy-1.3.0.tar.gz
:: curl https://www.7-zip.org/a/7z1900-x64.exe --output 7z.exe
:: 7z.exe SQLAlchemy-1.3.0.tar.gz

pause