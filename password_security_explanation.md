# 🔐 Password Security: Encryption vs Hashing

## 1️⃣ Why We Should NOT Store Plain Text Passwords

If passwords are stored as plain text in a database:

-   Anyone who accesses the database can see all user passwords.
-   If the database is hacked, all accounts are compromised.
-   Users often reuse passwords on other websites.

This is a **major security risk**.

------------------------------------------------------------------------

## 2️⃣ What is Encryption?

Encryption converts data into a secret format using a key.

-   It can be reversed (decrypted) using the correct key.
-   Used for protecting data during transmission (HTTPS, SSL).
-   Not ideal for password storage because it can be decrypted.

Example: Plain password → Encrypted text → Can be decrypted back to
original.

------------------------------------------------------------------------

## 3️⃣ What is Hashing?

Hashing converts data into a fixed-length string using a mathematical
algorithm.

-   One-way process (cannot be reversed).
-   Even small input changes create completely different hashes.
-   Ideal for password storage.

Example:

    Password: 123456
    Hashed: pbkdf2:sha256:600000$Aks83J...longstring...

You cannot convert the hash back to "123456".

------------------------------------------------------------------------

## 4️⃣ Why Hashing is Better for Passwords

✔ One-way (cannot decrypt)\
✔ Secure against database leaks\
✔ Industry standard\
✔ Used by professional applications

------------------------------------------------------------------------

## 5️⃣ How Password Verification Works During Login

When a user registers:

1.  User enters password.
2.  Server hashes the password.
3.  Hashed password is stored in database.

When user logs in:

1.  User enters password.
2.  Server retrieves stored hashed password.
3.  Server uses `check_password_hash()` to compare:

```{=html}
<!-- -->
```
    check_password_hash(stored_hash, entered_password)

4.  If match → Login successful\
5.  If not → Incorrect password

⚠ We NEVER compare plain password with hashed password directly.

------------------------------------------------------------------------

## 6️⃣ Example in Flask

### 🔹 Registration (Hashing Before Store)

``` python
from werkzeug.security import generate_password_hash

hashed_password = generate_password_hash(password)
```

### 🔹 Login Verification

``` python
from werkzeug.security import check_password_hash

if check_password_hash(stored_hash, entered_password):
    print("Login successful")
else:
    print("Incorrect password")
```

------------------------------------------------------------------------

## 7️⃣ Final Summary

  Method       Can Reverse?   Safe for Passwords?
  ------------ -------------- ---------------------
  Plain Text   Yes            ❌ No
  Encryption   Yes            ❌ Not Recommended
  Hashing      No             ✅ Yes

------------------------------------------------------------------------

# ✅ Conclusion

Always use hashing (like Werkzeug's `generate_password_hash`)\
Never store raw passwords in the database.

This is the professional and secure way to build authentication systems.




# About Session Library
    1. Session is a library. It 

    2.What Is session?
        In Flask:
        session is a dictionary
        It stores data for one user
        It stays saved in browser (secure cookie)
        It remembers the user between pages.
        ```session = {
    "user": "rahul01"}```


    3. Why Store It In Session?
        Because after login:
        We want to remember:
        Who is logged in?
        Allow access to dashboard
        Block others
