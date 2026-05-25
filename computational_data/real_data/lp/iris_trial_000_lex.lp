Maximize
 obj: 1.000000 r_0 +0.966667 r_1 +0.966667 r_2 +0.966667 r_3 +0.966667 r_4 +0.966667 r_5
  +0.966667 r_6 +0.966667 r_7 +1.000000 r_8 +1.000000 r_9 +0.966667 r_10 +1.000000 r_11
  +1.000000 r_12 +1.000000 r_13 +1.000000 r_14 +1.000000 r_15 +1.000000 r_16 +1.000000 b_0
  +0.966667 b_1 +0.966667 b_2 +0.966667 b_3 +0.966667 b_4 +0.966667 b_5 +0.966667 b_6
  +0.966667 b_7 +1.000000 b_8 +1.000000 b_9 +0.966667 b_10 +1.000000 b_11 +1.000000 b_12
  +1.000000 b_13 +1.000000 b_14 +1.000000 b_15 +1.000000 b_16
Subject To
 red_nonempty: r_0 +r_1 +r_2 +r_3 +r_4 +r_5 +r_6 +r_7 +r_8 +r_9 +r_10 +r_11 +r_12 +r_13
  +r_14 +r_15 +r_16 >= 1
 blue_nonempty: b_0 +b_1 +b_2 +b_3 +b_4 +b_5 +b_6 +b_7 +b_8 +b_9 +b_10 +b_11 +b_12 +b_13
  +b_14 +b_15 +b_16 >= 1
 size_ge: r_0 +r_1 +r_2 +r_3 +r_4 +r_5 +r_6 +r_7 +r_8 +r_9 +r_10 +r_11 +r_12 +r_13 +r_14
  +r_15 +r_16 +b_0 +b_1 +b_2 +b_3 +b_4 +b_5 +b_6 +b_7 +b_8 +b_9 +b_10 +b_11 +b_12 +b_13
  +b_14 +b_15 +b_16 >= 4
 size_le: r_0 +r_1 +r_2 +r_3 +r_4 +r_5 +r_6 +r_7 +r_8 +r_9 +r_10 +r_11 +r_12 +r_13 +r_14
  +r_15 +r_16 +b_0 +b_1 +b_2 +b_3 +b_4 +b_5 +b_6 +b_7 +b_8 +b_9 +b_10 +b_11 +b_12 +b_13
  +b_14 +b_15 +b_16 <= 4
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
 disjoint_16: r_16 + b_16 <= 1
 red_ind_0: r_0 + r_8 <= 1
 blue_ind_0: b_0 + b_8 <= 1
 red_ind_1: r_0 + r_9 <= 1
 blue_ind_1: b_0 + b_9 <= 1
 red_ind_2: r_0 + r_11 <= 1
 blue_ind_2: b_0 + b_11 <= 1
 red_ind_3: r_0 + r_12 <= 1
 blue_ind_3: b_0 + b_12 <= 1
 red_ind_4: r_0 + r_13 <= 1
 blue_ind_4: b_0 + b_13 <= 1
 red_ind_5: r_0 + r_14 <= 1
 blue_ind_5: b_0 + b_14 <= 1
 red_ind_6: r_0 + r_15 <= 1
 blue_ind_6: b_0 + b_15 <= 1
 red_ind_7: r_0 + r_16 <= 1
 blue_ind_7: b_0 + b_16 <= 1
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
 red_ind_14: r_1 + r_10 <= 1
 blue_ind_14: b_1 + b_10 <= 1
 red_ind_15: r_2 + r_3 <= 1
 blue_ind_15: b_2 + b_3 <= 1
 red_ind_16: r_2 + r_4 <= 1
 blue_ind_16: b_2 + b_4 <= 1
 red_ind_17: r_2 + r_5 <= 1
 blue_ind_17: b_2 + b_5 <= 1
 red_ind_18: r_2 + r_6 <= 1
 blue_ind_18: b_2 + b_6 <= 1
 red_ind_19: r_2 + r_7 <= 1
 blue_ind_19: b_2 + b_7 <= 1
 red_ind_20: r_2 + r_10 <= 1
 blue_ind_20: b_2 + b_10 <= 1
 red_ind_21: r_3 + r_4 <= 1
 blue_ind_21: b_3 + b_4 <= 1
 red_ind_22: r_3 + r_5 <= 1
 blue_ind_22: b_3 + b_5 <= 1
 red_ind_23: r_3 + r_6 <= 1
 blue_ind_23: b_3 + b_6 <= 1
 red_ind_24: r_3 + r_7 <= 1
 blue_ind_24: b_3 + b_7 <= 1
 red_ind_25: r_3 + r_10 <= 1
 blue_ind_25: b_3 + b_10 <= 1
 red_ind_26: r_4 + r_5 <= 1
 blue_ind_26: b_4 + b_5 <= 1
 red_ind_27: r_4 + r_6 <= 1
 blue_ind_27: b_4 + b_6 <= 1
 red_ind_28: r_4 + r_7 <= 1
 blue_ind_28: b_4 + b_7 <= 1
 red_ind_29: r_4 + r_10 <= 1
 blue_ind_29: b_4 + b_10 <= 1
 red_ind_30: r_5 + r_6 <= 1
 blue_ind_30: b_5 + b_6 <= 1
 red_ind_31: r_5 + r_7 <= 1
 blue_ind_31: b_5 + b_7 <= 1
 red_ind_32: r_5 + r_10 <= 1
 blue_ind_32: b_5 + b_10 <= 1
 red_ind_33: r_6 + r_7 <= 1
 blue_ind_33: b_6 + b_7 <= 1
 red_ind_34: r_6 + r_10 <= 1
 blue_ind_34: b_6 + b_10 <= 1
 red_ind_35: r_7 + r_10 <= 1
 blue_ind_35: b_7 + b_10 <= 1
 red_ind_36: r_8 + r_9 <= 1
 blue_ind_36: b_8 + b_9 <= 1
 red_ind_37: r_8 + r_11 <= 1
 blue_ind_37: b_8 + b_11 <= 1
 red_ind_38: r_8 + r_12 <= 1
 blue_ind_38: b_8 + b_12 <= 1
 red_ind_39: r_8 + r_13 <= 1
 blue_ind_39: b_8 + b_13 <= 1
 red_ind_40: r_8 + r_14 <= 1
 blue_ind_40: b_8 + b_14 <= 1
 red_ind_41: r_8 + r_15 <= 1
 blue_ind_41: b_8 + b_15 <= 1
 red_ind_42: r_8 + r_16 <= 1
 blue_ind_42: b_8 + b_16 <= 1
 red_ind_43: r_9 + r_11 <= 1
 blue_ind_43: b_9 + b_11 <= 1
 red_ind_44: r_9 + r_12 <= 1
 blue_ind_44: b_9 + b_12 <= 1
 red_ind_45: r_9 + r_13 <= 1
 blue_ind_45: b_9 + b_13 <= 1
 red_ind_46: r_9 + r_14 <= 1
 blue_ind_46: b_9 + b_14 <= 1
 red_ind_47: r_9 + r_15 <= 1
 blue_ind_47: b_9 + b_15 <= 1
 red_ind_48: r_9 + r_16 <= 1
 blue_ind_48: b_9 + b_16 <= 1
 red_ind_49: r_11 + r_12 <= 1
 blue_ind_49: b_11 + b_12 <= 1
 red_ind_50: r_11 + r_13 <= 1
 blue_ind_50: b_11 + b_13 <= 1
 red_ind_51: r_11 + r_14 <= 1
 blue_ind_51: b_11 + b_14 <= 1
 red_ind_52: r_11 + r_15 <= 1
 blue_ind_52: b_11 + b_15 <= 1
 red_ind_53: r_11 + r_16 <= 1
 blue_ind_53: b_11 + b_16 <= 1
 red_ind_54: r_12 + r_13 <= 1
 blue_ind_54: b_12 + b_13 <= 1
 red_ind_55: r_12 + r_14 <= 1
 blue_ind_55: b_12 + b_14 <= 1
 red_ind_56: r_12 + r_15 <= 1
 blue_ind_56: b_12 + b_15 <= 1
 red_ind_57: r_12 + r_16 <= 1
 blue_ind_57: b_12 + b_16 <= 1
 red_ind_58: r_13 + r_14 <= 1
 blue_ind_58: b_13 + b_14 <= 1
 red_ind_59: r_13 + r_15 <= 1
 blue_ind_59: b_13 + b_15 <= 1
 red_ind_60: r_13 + r_16 <= 1
 blue_ind_60: b_13 + b_16 <= 1
 red_ind_61: r_14 + r_15 <= 1
 blue_ind_61: b_14 + b_15 <= 1
 red_ind_62: r_14 + r_16 <= 1
 blue_ind_62: b_14 + b_16 <= 1
 red_ind_63: r_15 + r_16 <= 1
 blue_ind_63: b_15 + b_16 <= 1
 red_dom_0: r_8 +r_9 +r_11 +r_12 +r_13 +r_14 +r_15 +r_16 +r_0 +b_0 >= 1
 blue_dom_0: b_8 +b_9 +b_11 +b_12 +b_13 +b_14 +b_15 +b_16 +r_0 +b_0 >= 1
 red_dom_1: r_2 +r_3 +r_4 +r_5 +r_6 +r_7 +r_10 +r_1 +b_1 >= 1
 blue_dom_1: b_2 +b_3 +b_4 +b_5 +b_6 +b_7 +b_10 +r_1 +b_1 >= 1
 red_dom_2: r_1 +r_3 +r_4 +r_5 +r_6 +r_7 +r_10 +r_2 +b_2 >= 1
 blue_dom_2: b_1 +b_3 +b_4 +b_5 +b_6 +b_7 +b_10 +r_2 +b_2 >= 1
 red_dom_3: r_1 +r_2 +r_4 +r_5 +r_6 +r_7 +r_10 +r_3 +b_3 >= 1
 blue_dom_3: b_1 +b_2 +b_4 +b_5 +b_6 +b_7 +b_10 +r_3 +b_3 >= 1
 red_dom_4: r_1 +r_2 +r_3 +r_5 +r_6 +r_7 +r_10 +r_4 +b_4 >= 1
 blue_dom_4: b_1 +b_2 +b_3 +b_5 +b_6 +b_7 +b_10 +r_4 +b_4 >= 1
 red_dom_5: r_1 +r_2 +r_3 +r_4 +r_6 +r_7 +r_10 +r_5 +b_5 >= 1
 blue_dom_5: b_1 +b_2 +b_3 +b_4 +b_6 +b_7 +b_10 +r_5 +b_5 >= 1
 red_dom_6: r_1 +r_2 +r_3 +r_4 +r_5 +r_7 +r_10 +r_6 +b_6 >= 1
 blue_dom_6: b_1 +b_2 +b_3 +b_4 +b_5 +b_7 +b_10 +r_6 +b_6 >= 1
 red_dom_7: r_1 +r_2 +r_3 +r_4 +r_5 +r_6 +r_10 +r_7 +b_7 >= 1
 blue_dom_7: b_1 +b_2 +b_3 +b_4 +b_5 +b_6 +b_10 +r_7 +b_7 >= 1
 red_dom_8: r_0 +r_9 +r_11 +r_12 +r_13 +r_14 +r_15 +r_16 +r_8 +b_8 >= 1
 blue_dom_8: b_0 +b_9 +b_11 +b_12 +b_13 +b_14 +b_15 +b_16 +r_8 +b_8 >= 1
 red_dom_9: r_0 +r_8 +r_11 +r_12 +r_13 +r_14 +r_15 +r_16 +r_9 +b_9 >= 1
 blue_dom_9: b_0 +b_8 +b_11 +b_12 +b_13 +b_14 +b_15 +b_16 +r_9 +b_9 >= 1
 red_dom_10: r_1 +r_2 +r_3 +r_4 +r_5 +r_6 +r_7 +r_10 +b_10 >= 1
 blue_dom_10: b_1 +b_2 +b_3 +b_4 +b_5 +b_6 +b_7 +r_10 +b_10 >= 1
 red_dom_11: r_0 +r_8 +r_9 +r_12 +r_13 +r_14 +r_15 +r_16 +r_11 +b_11 >= 1
 blue_dom_11: b_0 +b_8 +b_9 +b_12 +b_13 +b_14 +b_15 +b_16 +r_11 +b_11 >= 1
 red_dom_12: r_0 +r_8 +r_9 +r_11 +r_13 +r_14 +r_15 +r_16 +r_12 +b_12 >= 1
 blue_dom_12: b_0 +b_8 +b_9 +b_11 +b_13 +b_14 +b_15 +b_16 +r_12 +b_12 >= 1
 red_dom_13: r_0 +r_8 +r_9 +r_11 +r_12 +r_14 +r_15 +r_16 +r_13 +b_13 >= 1
 blue_dom_13: b_0 +b_8 +b_9 +b_11 +b_12 +b_14 +b_15 +b_16 +r_13 +b_13 >= 1
 red_dom_14: r_0 +r_8 +r_9 +r_11 +r_12 +r_13 +r_15 +r_16 +r_14 +b_14 >= 1
 blue_dom_14: b_0 +b_8 +b_9 +b_11 +b_12 +b_13 +b_15 +b_16 +r_14 +b_14 >= 1
 red_dom_15: r_0 +r_8 +r_9 +r_11 +r_12 +r_13 +r_14 +r_16 +r_15 +b_15 >= 1
 blue_dom_15: b_0 +b_8 +b_9 +b_11 +b_12 +b_13 +b_14 +b_16 +r_15 +b_15 >= 1
 red_dom_16: r_0 +r_8 +r_9 +r_11 +r_12 +r_13 +r_14 +r_15 +r_16 +b_16 >= 1
 blue_dom_16: b_0 +b_8 +b_9 +b_11 +b_12 +b_13 +b_14 +b_15 +r_16 +b_16 >= 1
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
 r_16
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
 b_16
End
