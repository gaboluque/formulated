## Races

### Use Case: List Races
#### Description
A user can view a list of all races in the system. The system will display race details such as name, date, circuit, description, and status.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to view races.
- There are races available in the system.
#### Postconditions
- The user can view the list of races.
#### Main Flow
1. User navigates to the races page.
2. System retrieves the list of races from the database.
3. System displays the list of races with their details (name, date, circuit, description, status).
4. User can filter or search for specific races (by name, date, or circuit).
5. User can click on a race to view more details.

### Use Case: View Race Details
#### Description
A user can view detailed information about a specific race. The system will display the race's name, date, circuit information, description, positions, points, and other relevant details.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to view race details.
- The race exists in the system.
#### Postconditions
- The user can view the race's details.
#### Main Flow
1. User clicks on a race from the list of races.
2. System retrieves the race's details from the database.
3. System displays the race's name, date, circuit information, description, results/positions, and other relevant details.

### Use Case: Like a Race
#### Description
A user can like a race to show their support or interest. The system will update the race's like count.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to like races.
- The race exists in the system.
#### Postconditions
- The race's like count is updated.
#### Main Flow
1. User views a race's details.
2. User clicks the like button.
3. System checks if the user has already liked the race.
4. If not, system increments the race's like count.
5. System updates the race's like count in the database.

### Use Case: Un-like a Race
#### Description
A user can un-like a race to remove their support or interest. The system will update the race's like count.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to like races.
- The race exists in the system.
- The user has previously liked the race.
#### Postconditions
- The race's like count is updated.
#### Main Flow
1. User views a race's details.
2. User clicks the unlike button.
3. System checks if the user has liked the race.
4. If yes, system decrements the race's like count.
5. System updates the race's like count in the database.

### Use Case: Review a Race
#### Description
A user can leave a review for a race to provide feedback or commentary. The system will store the review and associate it with the race.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to review races.
- The race exists in the system.
- The race has finished (i.e., start_at date is in the past).
#### Postconditions
- The race's review count is updated.
#### Main Flow
1. User views a race's details.
2. User clicks the review button.
3. System displays a review form.
4. User enters their review and rating.
5. System validates the review input.
6. System saves the review and associates it with the race.
7. System updates the race's review count.

### Use Case: Edit Race Review
#### Description
A user can edit their previously submitted review for a race. The system will update the review with the new content.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to edit their review.
- The race exists in the system.
- The user has previously submitted a review for the race.
#### Postconditions
- The race's review is updated with the new content.
#### Main Flow
1. User views their previously submitted review for a race.
2. User clicks the edit button on their review.
3. System displays the review form with the existing content.
4. User modifies the review content and rating.
5. System validates the updated review input.
6. System updates the review in the database.
7. System displays a confirmation message that the review has been updated.

### Use Case: Delete Race Review
#### Description
A user can delete their previously submitted review for a race. The system will remove the review from the database.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to delete their review.
- The race exists in the system.
- The user has previously submitted a review for the race.
#### Postconditions
- The race's review is removed from the database.
#### Main Flow
1. User views their previously submitted review for a race.
2. User clicks the delete button on their review.
3. System prompts the user for confirmation to delete the review.
4. User confirms the deletion.
5. System removes the review from the database.
6. System displays a confirmation message that the review has been deleted. 