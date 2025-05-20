# tests/integration/features/users.feature
Feature: User Management
  As a system administrator
  I want to manage user accounts
  So that I can control who has access to the system

  Background:
    Given the system has these existing users:
      | id | username | email               | cpf         |
      | 1  | user1    | user1@example.com   | 12345678901 |
      | 2  | user2    | user2@example.com   | 98765432101 |

  Scenario: Creating a new user successfully
    When I create a user with the following information:
      | username | email               | password   | cpf         |
      | newuser  | newuser@example.com | Password1! | 11122233344 |
    Then the user creation should be successful
    And the response should include the user details
    And the password should not be included in the response

  Scenario: Attempting to create a user with an existing CPF
    When I create a user with the following information:
      | username | email            | password   | cpf         |
      | copycat  | copy@example.com | Password1! | 12345678901 |
    Then the user creation should fail
    And the user error message should contain "User already exists"

  Scenario: Retrieving a user by ID
    When I request the user with ID 1
    Then the request should be successful
    And the response should include user details for "user1"

  Scenario: Retrieving a user by CPF
    When I request the user with CPF "98765432101"
    Then the request should be successful
    And the response should include user details for "user2"

  Scenario: Retrieving a non-existent user
    When I request the user with ID 999
    Then the request should fail
    And the user error message should contain "User not found"

  Scenario: Updating a user's information
    When I update user with ID 1 with the following information:
      | username | email                 | password      | cpf         |
      | updated1 | updated1@example.com  | NewPassword1! | 12345678901 |
    Then the user update should be successful
    And the response should include the updated user details

  Scenario: Deleting a user
    When I delete the user with ID 2
    Then the user deletion should be successful
    And a confirmation message should be returned