Feature: permutation problem
  You are given a bunch of items. These objects might be individual objects or combination of them.
  try to pick up a fixed quantity of items and keep a specific item unique in them.

  Scenario: a fixed quantity of items are provided
    Given signals in "signal_3.xlsx", the quantity allowed is "3"
    When try to pick up the right items
    Then the following permutations are chosen
      | permutation                   |
      | (ex3690a),(ex4022b),(ex5320a) |
      | (ex3690a,ex4022b),(ex5320a)   |
      | (ex3690a),(ex4022b,ex5320a)   |
      | (ex3690a,ex5320a),(ex4022b)   |


  Scenario: a fixed quantity of items are provided
    Given signals in "signal_4.xlsx", the quantity allowed is "4"
    When try to pick up the right items
    Then the following permutations are chosen
      | permutation                             |
      | (ex3690a),(ex4022b),(ex5320a),(ex5320b) |
      | (ex3690a,ex4022b),(ex5320a),(ex5320b)   |
      | (ex3690a,ex5320a),(ex4022b),(ex5320b)   |
      | (ex3690a),(ex4022b,ex5320a),(ex5320b)   |
      | (ex3690a,ex5320b),(ex4022b),(ex5320a)   |
      | (ex3690a),(ex4022b,ex5320b),(ex5320a)   |
      | (ex3690a),(ex4022b),(ex5320a,ex5320b)   |
      | (ex3690a,ex4022b),(ex5320a,ex5320b)     |
      | (ex3690a,ex5320a),(ex4022b,ex5320b)     |
      | (ex3690a,ex5320b),(ex4022b,ex5320a)     |


  Scenario: a fixed quantity of items are provided
    Given signals in "signal_5.xlsx", the quantity allowed is "5"
    When try to pick up the right items
    Then the following permutations are chosen
      | permutation                                       |
      | (ex3690a),(ex4022b),(ex5320a),(ex5320b),(ex6393a) |
      | (ex3690a,ex4022b),(ex5320a),(ex5320b),(ex6393a)   |
      | (ex3690a,ex5320a),(ex4022b),(ex5320b),(ex6393a)   |
      | (ex3690a),(ex4022b,ex5320a),(ex5320b),(ex6393a)   |
      | (ex3690a,ex5320b),(ex4022b),(ex5320a),(ex6393a)   |
      | (ex3690a),(ex4022b,ex5320b),(ex5320a),(ex6393a)   |
      | (ex3690a),(ex4022b),(ex5320a,ex5320b),(ex6393a)   |
      | (ex3690a,ex4022b),(ex5320a,ex5320b),(ex6393a)     |
      | (ex3690a,ex5320a),(ex4022b,ex5320b),(ex6393a)     |
      | (ex3690a,ex5320b),(ex4022b,ex5320a),(ex6393a)     |
      | (ex3690a,ex6393a),(ex4022b),(ex5320a),(ex5320b)   |
      | (ex3690a),(ex4022b,ex6393a),(ex5320a),(ex5320b)   |
      | (ex3690a),(ex4022b),(ex5320a,ex6393a),(ex5320b)   |
      | (ex3690a),(ex4022b),(ex5320a),(ex5320b,ex6393a)   |
      | (ex3690a,ex4022b),(ex5320a,ex6393a),(ex5320b)     |
      | (ex3690a,ex4022b),(ex5320a),(ex5320b,ex6393a)     |
      | (ex3690a,ex5320a),(ex4022b,ex6393a),(ex5320b)     |
      | (ex3690a,ex5320a),(ex4022b),(ex5320b,ex6393a)     |
      | (ex3690a,ex6393a),(ex4022b,ex5320a),(ex5320b)     |
      | (ex3690a),(ex4022b,ex5320a),(ex5320b,ex6393a)     |
      | (ex3690a,ex5320b),(ex4022b,ex6393a),(ex5320a)     |
      | (ex3690a,ex5320b),(ex4022b),(ex5320a,ex6393a)     |
      | (ex3690a,ex6393a),(ex4022b,ex5320b),(ex5320a)     |
      | (ex3690a),(ex4022b,ex5320b),(ex5320a,ex6393a)     |
      | (ex3690a,ex6393a),(ex4022b),(ex5320a,ex5320b)     |
      | (ex3690a),(ex4022b,ex6393a),(ex5320a,ex5320b)     |

