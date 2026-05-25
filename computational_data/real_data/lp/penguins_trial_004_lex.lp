Maximize
 obj: 0.985075 r_0 +0.985075 r_1 +0.970149 r_2 +0.970149 r_3 +0.970149 r_4 +0.970149 r_5
  +0.970149 r_6 +0.955224 r_7 +0.955224 r_8 +0.910448 r_9 +0.865672 r_10 +0.865672 r_11
  +0.835821 r_12 +0.820896 r_13 +0.805970 r_14 +0.791045 r_15 +0.985075 b_0 +0.985075 b_1
  +0.970149 b_2 +0.970149 b_3 +0.970149 b_4 +0.970149 b_5 +0.970149 b_6 +0.955224 b_7
  +0.955224 b_8 +0.910448 b_9 +0.865672 b_10 +0.865672 b_11 +0.835821 b_12 +0.820896 b_13
  +0.805970 b_14 +0.791045 b_15
Subject To
 red_nonempty: r_0 +r_1 +r_2 +r_3 +r_4 +r_5 +r_6 +r_7 +r_8 +r_9 +r_10 +r_11 +r_12 +r_13
  +r_14 +r_15 >= 1
 blue_nonempty: b_0 +b_1 +b_2 +b_3 +b_4 +b_5 +b_6 +b_7 +b_8 +b_9 +b_10 +b_11 +b_12 +b_13
  +b_14 +b_15 >= 1
 size_ge: r_0 +r_1 +r_2 +r_3 +r_4 +r_5 +r_6 +r_7 +r_8 +r_9 +r_10 +r_11 +r_12 +r_13 +r_14
  +r_15 +b_0 +b_1 +b_2 +b_3 +b_4 +b_5 +b_6 +b_7 +b_8 +b_9 +b_10 +b_11 +b_12 +b_13 +b_14
  +b_15 >= 9
 size_le: r_0 +r_1 +r_2 +r_3 +r_4 +r_5 +r_6 +r_7 +r_8 +r_9 +r_10 +r_11 +r_12 +r_13 +r_14
  +r_15 +b_0 +b_1 +b_2 +b_3 +b_4 +b_5 +b_6 +b_7 +b_8 +b_9 +b_10 +b_11 +b_12 +b_13 +b_14
  +b_15 <= 9
 disjoint_0: r_0 + b_0 <= 1
 disjoint_1: r_1 + b_1 <= 1
 disjoint_2: r_2 + b_2 <= 1
 disjoint_3: r_3 + b_3 <= 1
 disjoint_4: r_4 + b_4 <= 1
 disjoint_5: r_5 + b_5 <= 1
 disjoint_6: r_6 + b_6 <= 1
 disjoint_7: r_7 + b_7 <= 1
 disjoint_8: r_8 + b_8 <= 1
 disjoint_9: r_9 + b_9 <= 1
 disjoint_10: r_10 + b_10 <= 1
 disjoint_11: r_11 + b_11 <= 1
 disjoint_12: r_12 + b_12 <= 1
 disjoint_13: r_13 + b_13 <= 1
 disjoint_14: r_14 + b_14 <= 1
 disjoint_15: r_15 + b_15 <= 1
 red_ind_0: r_0 + r_1 <= 1
 blue_ind_0: b_0 + b_1 <= 1
 red_ind_1: r_0 + r_2 <= 1
 blue_ind_1: b_0 + b_2 <= 1
 red_ind_2: r_0 + r_3 <= 1
 blue_ind_2: b_0 + b_3 <= 1
 red_ind_3: r_0 + r_4 <= 1
 blue_ind_3: b_0 + b_4 <= 1
 red_ind_4: r_0 + r_5 <= 1
 blue_ind_4: b_0 + b_5 <= 1
 red_ind_5: r_0 + r_6 <= 1
 blue_ind_5: b_0 + b_6 <= 1
 red_ind_6: r_0 + r_7 <= 1
 blue_ind_6: b_0 + b_7 <= 1
 red_ind_7: r_0 + r_8 <= 1
 blue_ind_7: b_0 + b_8 <= 1
 red_ind_8: r_1 + r_2 <= 1
 blue_ind_8: b_1 + b_2 <= 1
 red_ind_9: r_1 + r_3 <= 1
 blue_ind_9: b_1 + b_3 <= 1
 red_ind_10: r_1 + r_4 <= 1
 blue_ind_10: b_1 + b_4 <= 1
 red_ind_11: r_1 + r_5 <= 1
 blue_ind_11: b_1 + b_5 <= 1
 red_ind_12: r_1 + r_6 <= 1
 blue_ind_12: b_1 + b_6 <= 1
 red_ind_13: r_1 + r_7 <= 1
 blue_ind_13: b_1 + b_7 <= 1
 red_ind_14: r_1 + r_8 <= 1
 blue_ind_14: b_1 + b_8 <= 1
 red_ind_15: r_2 + r_3 <= 1
 blue_ind_15: b_2 + b_3 <= 1
 red_ind_16: r_2 + r_4 <= 1
 blue_ind_16: b_2 + b_4 <= 1
 red_ind_17: r_2 + r_5 <= 1
 blue_ind_17: b_2 + b_5 <= 1
 red_ind_18: r_2 + r_6 <= 1
 blue_ind_18: b_2 + b_6 <= 1
 red_ind_19: r_2 + r_8 <= 1
 blue_ind_19: b_2 + b_8 <= 1
 red_ind_20: r_2 + r_9 <= 1
 blue_ind_20: b_2 + b_9 <= 1
 red_ind_21: r_3 + r_4 <= 1
 blue_ind_21: b_3 + b_4 <= 1
 red_ind_22: r_3 + r_5 <= 1
 blue_ind_22: b_3 + b_5 <= 1
 red_ind_23: r_3 + r_6 <= 1
 blue_ind_23: b_3 + b_6 <= 1
 red_ind_24: r_3 + r_8 <= 1
 blue_ind_24: b_3 + b_8 <= 1
 red_ind_25: r_3 + r_9 <= 1
 blue_ind_25: b_3 + b_9 <= 1
 red_ind_26: r_4 + r_5 <= 1
 blue_ind_26: b_4 + b_5 <= 1
 red_ind_27: r_4 + r_6 <= 1
 blue_ind_27: b_4 + b_6 <= 1
 red_ind_28: r_4 + r_8 <= 1
 blue_ind_28: b_4 + b_8 <= 1
 red_ind_29: r_4 + r_9 <= 1
 blue_ind_29: b_4 + b_9 <= 1
 red_ind_30: r_5 + r_6 <= 1
 blue_ind_30: b_5 + b_6 <= 1
 red_ind_31: r_5 + r_8 <= 1
 blue_ind_31: b_5 + b_8 <= 1
 red_ind_32: r_5 + r_9 <= 1
 blue_ind_32: b_5 + b_9 <= 1
 red_ind_33: r_6 + r_8 <= 1
 blue_ind_33: b_6 + b_8 <= 1
 red_ind_34: r_7 + r_8 <= 1
 blue_ind_34: b_7 + b_8 <= 1
 red_ind_35: r_11 + r_13 <= 1
 blue_ind_35: b_11 + b_13 <= 1
 red_ind_36: r_14 + r_15 <= 1
 blue_ind_36: b_14 + b_15 <= 1
 red_dom_0: r_1 +r_2 +r_3 +r_4 +r_5 +r_6 +r_7 +r_8 +r_0 +b_0 >= 1
 blue_dom_0: b_1 +b_2 +b_3 +b_4 +b_5 +b_6 +b_7 +b_8 +r_0 +b_0 >= 1
 red_dom_1: r_0 +r_2 +r_3 +r_4 +r_5 +r_6 +r_7 +r_8 +r_1 +b_1 >= 1
 blue_dom_1: b_0 +b_2 +b_3 +b_4 +b_5 +b_6 +b_7 +b_8 +r_1 +b_1 >= 1
 red_dom_2: r_0 +r_1 +r_3 +r_4 +r_5 +r_6 +r_8 +r_9 +r_2 +b_2 >= 1
 blue_dom_2: b_0 +b_1 +b_3 +b_4 +b_5 +b_6 +b_8 +b_9 +r_2 +b_2 >= 1
 red_dom_3: r_0 +r_1 +r_2 +r_4 +r_5 +r_6 +r_8 +r_9 +r_3 +b_3 >= 1
 blue_dom_3: b_0 +b_1 +b_2 +b_4 +b_5 +b_6 +b_8 +b_9 +r_3 +b_3 >= 1
 red_dom_4: r_0 +r_1 +r_2 +r_3 +r_5 +r_6 +r_8 +r_9 +r_4 +b_4 >= 1
 blue_dom_4: b_0 +b_1 +b_2 +b_3 +b_5 +b_6 +b_8 +b_9 +r_4 +b_4 >= 1
 red_dom_5: r_0 +r_1 +r_2 +r_3 +r_4 +r_6 +r_8 +r_9 +r_5 +b_5 >= 1
 blue_dom_5: b_0 +b_1 +b_2 +b_3 +b_4 +b_6 +b_8 +b_9 +r_5 +b_5 >= 1
 red_dom_6: r_0 +r_1 +r_2 +r_3 +r_4 +r_5 +r_8 +r_6 +b_6 >= 1
 blue_dom_6: b_0 +b_1 +b_2 +b_3 +b_4 +b_5 +b_8 +r_6 +b_6 >= 1
 red_dom_7: r_0 +r_1 +r_8 +r_7 +b_7 >= 1
 blue_dom_7: b_0 +b_1 +b_8 +r_7 +b_7 >= 1
 red_dom_8: r_0 +r_1 +r_2 +r_3 +r_4 +r_5 +r_6 +r_7 +r_8 +b_8 >= 1
 blue_dom_8: b_0 +b_1 +b_2 +b_3 +b_4 +b_5 +b_6 +b_7 +r_8 +b_8 >= 1
 red_dom_9: r_2 +r_3 +r_4 +r_5 +r_9 +b_9 >= 1
 blue_dom_9: b_2 +b_3 +b_4 +b_5 +r_9 +b_9 >= 1
 red_dom_10: r_10 +b_10 >= 1
 blue_dom_10: r_10 +b_10 >= 1
 red_dom_11: r_13 +r_11 +b_11 >= 1
 blue_dom_11: b_13 +r_11 +b_11 >= 1
 red_dom_12: r_12 +b_12 >= 1
 blue_dom_12: r_12 +b_12 >= 1
 red_dom_13: r_11 +r_13 +b_13 >= 1
 blue_dom_13: b_11 +r_13 +b_13 >= 1
 red_dom_14: r_15 +r_14 +b_14 >= 1
 blue_dom_14: b_15 +r_14 +b_14 >= 1
 red_dom_15: r_14 +r_15 +b_15 >= 1
 blue_dom_15: b_14 +r_15 +b_15 >= 1
Binary
 r_0
 r_1
 r_2
 r_3
 r_4
 r_5
 r_6
 r_7
 r_8
 r_9
 r_10
 r_11
 r_12
 r_13
 r_14
 r_15
 b_0
 b_1
 b_2
 b_3
 b_4
 b_5
 b_6
 b_7
 b_8
 b_9
 b_10
 b_11
 b_12
 b_13
 b_14
 b_15
End
