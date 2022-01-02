Feature: knapsack problem
  pick up a few items from a bunch of things and put them into a knapsack with fixed capacity,
  and try to keep the sum of the value of all selected items largest

  Scenario Outline: you have a knapsack with a fixed capacity , and  a bunch of items with a weight of 1
    Given signals in <signal_file>, the capacity of the knapsack is <target_capacity>
    When try to pick up the items in order to keep the sum of their growth value largest
    Then <expected_items> should be in the knapsack

    Examples:
      | signal_file    | target_capacity | expected_items                                                      |
      | signal_6.xlsx  | 4               | (ex4022b),(ex5320b),(ex6393a),(ex6393b)                             |
      | signal_10.xlsx | 7               | (ex5320b),(ex6393a),(ex8000a),(ex3690a,ex8001a),(xm8670a),(xm8670b) |


  Scenario Outline: you have a knapsack with a fixed capacity , and  a bunch of items with a weight of 1
    Given signals in <signal_file>, the capacity of the knapsack is <target_capacity>
    When try to pick up the items in order to keep the sum of their drawback value lowest
    Then <expected_items> should be in the knapsack

    Examples:
      | signal_file    | target_capacity | expected_items                                                      |
      | signal_6.xlsx  | 4               | (ex3690a),(ex4022b),(ex5320b),(ex6393a)                             |
      | signal_10.xlsx | 7               | (ex5320b),(ex6393a),(ex8000a),(ex4022b,ex6393b),(xm8670a),(xm8670b) |


