# csvtosf
Read a CSV file and push it into a snowflake database using snowflake python connector

## Installing
Download / clone the repository, setup a virtualenv ( recommended to avoid package dependency conflicts ) and install the requirements using [pip](https://pip.pypa.io/en/stable/)
```
git clone git@github.com:manishbhatias/csvtosf.git
cd csvtosf
virtualenv .
pip install -r requirements.txt
```

## Usage
Optional
- Create a snowflake account
- Create a new database and warehouse
- Create a new role and grant privileges to write to the database
- Create a new user and assign role to it

Copy the following credentials from your account for use
- account - this is a combination of org-id and account-id
- user
- password
- warehouse
- database
- schema
- Run the program and follow the instructions
```bash
python csvtosf
```

## To do
- [ ] Improve validations error handling
- [ ] Refactor module and cli code into separate classes

## Built with
- [Snowflake Python Connector](https://docs.snowflake.com/en/user-guide/python-connector.html)
- [Pandas](https://pandas.pydata.org/)