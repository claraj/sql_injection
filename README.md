# sql_injection in Python

## SQL injection example: Java with MySQL

Subtitle: how not to write a login screen

Here's some valid passwords from the application's database. 

```
name, username, password
'Abby Admin', 'admin', 'kittens'
'Ben SysAdmin', 'ben', 'octopus'
'Carl ComputerTech', 'carl', 'mouse'
'Deb Developer', 'deb', 'zebra'
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

Maybe we'd like to create a new account for ourselves. Enter any username, and this password

    ' ; insert into passwords values ('evil', 'New Evil User', 'password'); select * from passwords where '1'='1

And then you should be able to log in with the username `evil` and password `password`.

The `;` signifies the end of a SQL command, so you can add your own SQL command afterwards. Remember to add a SQL statement at the end that can use the final `'` that your code is adding to the SQL.

The `select * from passwords where '1'='1` part doesn't do anything related to creating a new user, but it uses up the spare `'` to make the sequence of commands valid. 

Another approach is to write SQL that comments out the last comma.

And how about simply deleting the whole database? Enter anything for the username and this for the password,

    ' ; drop table passwords  ; select * from passwords where '1'='1

You'll see the Access Denied message, but if you try and log in with a valid account you'll see an error that the database table doesn't exist any more.

Try it out - can you do these things?

* Can you create yourself a new account?
* Can you delete someone else's account?
* Can you change someone's password? 
* Can you discover someone's password?
* What if you program's database user has permissions to create other users. Could you create a new database user and grant that user permissions?


Consider this could be a login form on a website that anyone could access. This is a huge problem. 

And this is just the tip of the iceberg of SQL injection. There are many more variations which can be used to discover your database table names, columns, and all of the data within. If you don't filter user input, a malicious user can potentially read all of your data and/or destroy your database. Think about databases of usernanmes and passwords, or credit card data, or names and social security numbers; for example LinkedIn (millions of username and passwords stolen) or the Heartland data breach (millions of credit cards stolen), VTech, the Wall Street Journal, the TalkTalk ISP, many government organization, and many more...

SQL injection hall of shame (Code Curmudgeon): http://codecurmudgeon.com/wp/sql-injection-hall-of-shame/
 
OK, so how to fix? One very useful preventative measure is parameterized queries. Try replacing the SQL statement at PasswordDatabase's authenticateUser() method with a parameterized query, and then try the evil SQL again. It shouldn't work. This is why you should always user parameterized queries, you should always validate user input, and doubly always when user input is involved!
