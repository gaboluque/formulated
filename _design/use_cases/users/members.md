## Members

### Use Case: List Members
#### Description
A user can view a list of all members in the system. The system will display member details such as name, team, role, and status.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to view members.
- There are members available in the system.
#### Postconditions
- The user can view the list of members.
#### Main Flow
1. User navigates to the members page.
2. System retrieves the list of members from the database.
3. System displays the list of members with their details (name, description, team, role, status).
4. User can filter or search for specific members (by name, team, or role).
5. User can click on a member to view more details.

### Use Case: View Member Details
#### Description
A user can view detailed information about a specific member. The system will display the member's name, team, role, status, history, and other relevant details.
If the member is a driver, the system will also display races, positions, and points associated with the member. 
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to view member details.
- The member exists in the system.
#### Postconditions
- The user can view the member's details.
#### Main Flow
1. User clicks on a member from the list of members.
2. System retrieves the member's details from the database.
3. System displays the member's name, team, role, status, history, and other relevant details.

### Use Case: Like a Member
#### Description
A user can like a member to show their support. The system will update the member's like count.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to like members.
- The member exists in the system.
#### Postconditions
- The member's like count is updated.
#### Main Flow
1. User views a member's details.
2. User clicks the like button.
3. System checks if the user has already liked the member.
4. If not, system increments the member's like count.
5. System updates the member's like count in the database.

### Use Case: Un-like a Member
#### Description
A user can un-like a member to remove their support. The system will update the member's like count.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to like members.
- The member exists in the system.
- The user has previously liked the member.
#### Postconditions
- The member's like count is updated.
#### Main Flow
1. User views a member's details.
2. User clicks the unlike button.
3. System checks if the user has liked the member.
4. If yes, system decrements the member's like count.
5. System updates the member's like count in the database.

### Use Case: Review a Member
#### Description
A user can leave a review for a member to provide feedback. The system will store the review and associate it with the member.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to review members.
- The member exists in the system.
#### Postconditions
- The member's review count is updated.
#### Main Flow
1. User views a member's details.
2. User clicks the review button.
3. System displays a review form.
4. User enters their review and rating.
5. System validates the review input.
6. System saves the review and associates it with the member.
7. System updates the member's review count.

### Use Case: Edit Member Review
#### Description
A user can edit their previously submitted review for a member. The system will update the review with the new content.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to edit their review.
- The member exists in the system.
- The user has previously submitted a review for the member.
#### Postconditions
- The member's review is updated with the new content.
#### Main Flow
1. User views their previously submitted review for a member.
2. User clicks the edit button on their review.
3. System displays the review form with the existing content.
4. User modifies the review content and rating.
5. System validates the updated review input.
6. System updates the review in the database.
7. System displays a confirmation message that the review has been updated.

### Use Case: Delete Member Review
#### Description
A user can delete their previously submitted review for a member. The system will remove the review from the database.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to delete their review.
- The member exists in the system.
#### Postconditions
- The member's review is removed from the database.
#### Main Flow
1. User views their previously submitted review for a member.
2. User clicks the delete button on their review.
3. System prompts the user for confirmation to delete the review.
4. User confirms the deletion.
5. System removes the review from the database.
6. System displays a confirmation message that the review has been deleted.
