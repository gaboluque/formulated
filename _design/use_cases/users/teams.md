## Teams

### Use Case: List Teams
#### Description
A user can view a list of all teams in the system. The system will display team details such as name, description, members, and status.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to view teams.
- There are teams available in the system.
#### Postconditions
- The user can view the list of teams.
#### Main Flow
1. User navigates to the teams page.
2. System retrieves the list of teams from the database.
3. System displays the list of teams with their details (name, description, members, status).
4. User can filter or search for specific teams (by name or status).
5. User can click on a team to view more details.

### Use Case: View Team Details
#### Description
A user can view detailed information about a specific team. The system will display the team's name, description, members, status, points, and other relevant details.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to view team details.
- The team exists in the system.
#### Postconditions
- The user can view the team's details.
#### Main Flow
1. User clicks on a team from the list of teams.
2. System retrieves the team's details from the database.
3. System displays the team's name, description, members, status, and other relevant details.

### Use Case: Like a Team
#### Description
A user can like a team to show their support. The system will update the team's like count.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to like teams.
- The team exists in the system.
#### Postconditions
- The team's like count is updated.
#### Main Flow
1. User views a team's details.
2. User clicks the like button.
3. System checks if the user has already liked the team.
4. If not, system increments the team's like count.
5. System updates the team's like count in the database.

### Use Case: Un-like a Team
#### Description
A user can un-like a team to remove their support. The system will update the team's like count.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to un-like teams.
- The team exists in the system.
#### Postconditions
- The team's like count is updated.
#### Main Flow
1. User views a team's details.
2. User clicks the un-like button.
3. System checks if the user has already liked the team.
4. If the user has liked the team, system decrements the team's like count.
5. System updates the team's like count in the database.

### Use Case: Review a Team
#### Description
A user can review a team to provide feedback or comments. The system will allow the user to submit a review and display it on the team's page.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to review teams.
- The team exists in the system.
#### Postconditions
- The user's review is submitted and displayed on the team's page.
#### Main Flow
1. User views a team's details.
2. User clicks the review button.
3. System displays a review form.
4. User enters their review and submits it.
5. System validates the review input.
6. System saves the review to the database.
7. System displays the review on the team's page.

### Use Case: Edit Team Review
#### Description
A user can edit their review of a team. The system will allow the user to update their review and save the changes.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to edit their review.
- The user has previously submitted a review for the team.
#### Postconditions
- The user's review is updated and displayed on the team's page.
#### Main Flow
1. User views their review on the team's page.
2. User clicks the edit button next to their review.
3. System displays the review in an editable form.
4. User modifies their review and submits it.
5. System validates the updated review input.
6. System updates the review in the database.
7. System displays the updated review on the team's page.

### Use Case: Delete Team Review
#### Description
A user can delete their review of a team. The system will remove the review from the team's page and update the database.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to delete their review.
- The user has previously submitted a review for the team.
#### Postconditions
- The user's review is deleted and no longer displayed on the team's page.
#### Main Flow
1. User views their review on the team's page.
2. User clicks the delete button next to their review.
3. System prompts the user for confirmation to delete the review.
4. User confirms the deletion.
5. System removes the review from the database.
6. System updates the team's page to reflect the deletion.