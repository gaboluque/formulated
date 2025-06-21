## Authorization and Authentication

### Use Case: User Registration
#### Description
A user can register for an account by providing their email, and password. The system will validate the input and create a new user (as "user" role).
#### Actors
- User
#### Preconditions
- The user is not already registered.
#### Postconditions
- A new user account is created with the provided email and password.
#### Main Flow
1. User navigates to the registration page.
2. User enters their email and password.
3. System validates the input.
4. System creates a new user account.

### Use Case: User Login
#### Description
A user can log in to their account using their email and password. The system will authenticate the user and provide access to their account.
#### Actors
- User
#### Preconditions
- The user has a registered account.
#### Postconditions
- The user is logged in and can access their account.
#### Main Flow
1. User navigates to the login page.
2. User enters their email and password.
3. System validates the credentials.
4. System authenticates the user and redirects them to their account page.

### Use Case: User Logout
#### Description
A user can log out of their account. The system will terminate the user's session and redirect them to the home page.
#### Actors
- User
#### Preconditions
- The user is logged in.
#### Postconditions
- The user is logged out and redirected to the home page.
#### Main Flow
1. User clicks the logout button.
2. System terminates the user's session.
3. System redirects the user to the home page.

### Use Case: Password Reset
#### Description
A user can reset their password if they forget it. The system will send a password reset link to the user's registered email.
#### Actors
- User
#### Preconditions
- The user has a registered account.
#### Postconditions
- The user receives a password reset link.
#### Main Flow
1. User navigates to the password reset page.
2. User enters their registered email.
3. System validates the email.
4. System sends a password reset link to the user's email.
5. User clicks the link and is redirected to a password reset page.
6. User enters a new password.
7. System validates the new password.
8. System updates the user's password.
