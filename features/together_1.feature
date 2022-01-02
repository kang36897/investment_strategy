Feature: best permutation problem
  pick up a few items from a bunch of things and put them into a knapsack with fixed capacity,
  and try to keep the sum of the value of all selected items largest or lowest. Be aware of that some of the items
  might be formed by some individual items.

  Scenario Outline: you have a knapsack with a fixed capacity , and  a bunch of items with different weight
    Given signals come from <signal_file>, the capacity of the knapsack is <target_capacity>
    When try to pick up the items in order to keep the sum of their growth value largest, but the selected signals should be unique in the permutation
    Then the total value would be larger than or equal with <expected_total_value>, and maybe <expected_items> have been put in the knapsack

    Examples:
      | signal_file      | target_capacity | expected_items                                                    | expected_total_value |
#      | signal_16.xlsx   | 6               | (z1001,z1012),(z1007,z1013),(z1015),(z1016)                       | 155077.45            |
      | signal_10_9.xlsx | 9               | (z1001, z1005),(z1003,z1004),(z1006,z1007),(z1008, z1009),(z1010) | 120664.16            |
      | signal_10_8.xlsx | 8               | (z1001,z1005),(z1003,z1004),(z1007,z1008),(z1009,z1010)           | 110999.59            |
      | signal_10_7.xlsx | 7               | (z1001,z1005),(z1003,z1004),(z1007,z1008),(z1009)                 | 99842.45             |

