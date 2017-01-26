# sql_injection in Python

## SQL injection example: Java with MySQL

Subtitle: how not to write a login screen

Here's some valid passwords from the application's database. 

```
username, name, password
admin|Abby Admin|kittens
bill|Bill S Preston|excellent!
bart|Bart Simpson|eatmyshorts
miley|Miley Cyrus|top40
```


Run the application, and try logging in with one of the valid passwords, and also try with an invalid password. You should see an appropriate success or failure message.

OK, now enter anything for the username, and this for password. 

```
whatever' or '1'='1
```

Who are you logged in as?

In addition to logging in as admin, there's more you can do with SQL injection.

Even though we can gain access to the admin account, we don't actually know the admin's password. With a little trial-and-error, we can discover the password. Try typing `admin` for the username and this for the password

    ' or password like 'a%

Put that into the SQL string, and you are asking to be logged in if our admin's password starts with `a`.
Now, try this for the password,

      ' or password like 'k%

Success! We now know our admin's password starts with `k`. An attacker can use trial and error to figure out all of the characters in the password.

    ' or password like 'ka%
    ' or password like 'kb%
    ' or password like 'kc%
    ....

It might take a while, but admin access to a server or access to a whole database full of credit card numbers is worth the effort. (And anyone smart enough to use SQL injection is probably smart enough to write a script that will do the hard work for them... or download one of the many SQL injection tools freely available on the internet, like SQLNinja or SQLMap.)

This application only allows you run one SQL statement at a time. Other databases/applications can be configured to run more than one SQL command at once - notably ASP and SQLServer - see the Visual Basic version of this project for all kinds of ways to abuse this - adding yourself as a new user, deleting the whole database... https://github.com/minneapolis-edu/vb-sql-injection

Consider this could be a login form on a website that anyone could access. This is a huge problem. 

And this is just the tip of the iceberg of SQL injection. There are many more variations which can be used to discover your database table names, columns, and all of the data within. https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/ If you don't filter user input, a malicious user can potentially read all of your data and/or destroy your database. Think about databases of usernanmes and passwords, or credit card data, or names and social security numbers; for example LinkedIn (millions of username and passwords stolen) or the Heartland data breach (millions of credit cards stolen), VTech, the Wall Street Journal, the TalkTalk ISP, many government organization, and many more...

SQL injection hall of shame (Code Curmudgeon): http://codecurmudgeon.com/wp/sql-injection-hall-of-shame/
 
OK, so how to fix? One very useful preventative measure is parameterized queries. Try replacing this line 

```
 sql_statement = '''SELECT name FROM users WHERE username = '%s' and password = '%s' ''' % (uname, password)

```

with a parameterized query, and then try the evil SQL again. It shouldn't work. This is why you should ALWAYS use parameterized queries, and validate your user input - don't trust your users!
