# tests/integration/features/auth.feature
Feature: User Authentication
  As a registered user
  I want to log in to the system
  So that I can access protected resources

  Background:
    Given the system has a registered user with CPF "12345678901" and password "valid_password"

  Scenario: Successful login
    When the user attempts to log in with CPF "12345678901" and password "valid_password"
    Then the login should be successful
    And the user should receive a valid token
    And the token should have an expiration time

  Scenario: Failed login with incorrect password
    When the user attempts to log in with CPF "12345678901" and password "wrong_password"
    Then the login should fail
    And the auth error message should contain "Incorrect credentials"

  Scenario: Failed login with non-existent user
    When the user attempts to log in with CPF "99999999999" and password "any_password"
    Then the login should fail
    And the auth error message should contain "User not found"