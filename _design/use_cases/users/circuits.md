## Circuits

### Use Case: List Circuits
#### Description
A user can view a list of all circuits in the system. The system will display circuit details such as name, location, country, length, description, and circuit characteristics.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to view circuits.
- There are circuits available in the system.
#### Postconditions
- The user can view the list of circuits.
#### Main Flow
1. User navigates to the circuits page.
2. System retrieves the list of circuits from the database.
3. System displays the list of circuits with their details (name, location, country, length, description).
4. User can filter or search for specific circuits (by name, location, or country).
5. User can click on a circuit to view more details.

### Use Case: View Circuit Details
#### Description
A user can view detailed information about a specific circuit. The system will display the circuit's name, location, country, length, lap record, circuit characteristics, description, and track layout information.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to view circuit details.
- The circuit exists in the system.
#### Postconditions
- The user can view the circuit's details.
#### Main Flow
1. User clicks on a circuit from the list of circuits.
2. System retrieves the circuit's details from the database.
3. System displays the circuit's name, location, country, length, lap record, circuit characteristics, track layout, and other relevant details.
4. System shows upcoming and past races held at this circuit.

### Use Case: Like a Circuit
#### Description
A user can like a circuit to show their support or favorite track preference. The system will update the circuit's like count.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to like circuits.
- The circuit exists in the system.
#### Postconditions
- The circuit's like count is updated.
#### Main Flow
1. User views a circuit's details.
2. User clicks the like button.
3. System checks if the user has already liked the circuit.
4. If not, system increments the circuit's like count.
5. System updates the circuit's like count in the database.

### Use Case: Un-like a Circuit
#### Description
A user can un-like a circuit to remove their support or preference. The system will update the circuit's like count.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to like circuits.
- The circuit exists in the system.
- The user has previously liked the circuit.
#### Postconditions
- The circuit's like count is updated.
#### Main Flow
1. User views a circuit's details.
2. User clicks the unlike button.
3. System checks if the user has liked the circuit.
4. If yes, system decrements the circuit's like count.
5. System updates the circuit's like count in the database.

### Use Case: Review a Circuit
#### Description
A user can leave a review for a circuit to provide feedback, commentary, or their experience with the track. The system will store the review and associate it with the circuit.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to review circuits.
- The circuit exists in the system.
#### Postconditions
- The circuit's review count is updated.
#### Main Flow
1. User views a circuit's details.
2. User clicks the review button.
3. System displays a review form.
4. User enters their review and rating.
5. System validates the review input.
6. System saves the review and associates it with the circuit.
7. System updates the circuit's review count.

### Use Case: Edit Circuit Review
#### Description
A user can edit their previously submitted review for a circuit. The system will update the review with the new content.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to edit their review.
- The circuit exists in the system.
- The user has previously submitted a review for the circuit.
#### Postconditions
- The circuit's review is updated with the new content.
#### Main Flow
1. User views their previously submitted review for a circuit.
2. User clicks the edit button on their review.
3. System displays the review form with the existing content.
4. User modifies the review content and rating.
5. System validates the updated review input.
6. System updates the review in the database.
7. System displays a confirmation message that the review has been updated.

### Use Case: Delete Circuit Review
#### Description
A user can delete their previously submitted review for a circuit. The system will remove the review from the database.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to delete their review.
- The circuit exists in the system.
- The user has previously submitted a review for the circuit.
#### Postconditions
- The circuit's review is removed from the database.
#### Main Flow
1. User views their previously submitted review for a circuit.
2. User clicks the delete button on their review.
3. System prompts the user for confirmation to delete the review.
4. User confirms the deletion.
5. System removes the review from the database.
6. System displays a confirmation message that the review has been deleted.

### Use Case: View Circuit Race History
#### Description
A user can view the history of races held at a specific circuit. The system will display past and upcoming races at the circuit.
#### Actors
- User
#### Preconditions
- The user is logged in.
- The user has permission to view circuit details.
- The circuit exists in the system.
#### Postconditions
- The user can view the circuit's race history.
#### Main Flow
1. User views a circuit's details page.
2. System retrieves all races associated with the circuit.
3. System displays the race history, including past race results and upcoming scheduled races.
4. User can click on individual races to view their details. 