Minimize
 obj: r_0 +r_1 +r_2 +r_3 +r_4 +r_5 +r_6 +r_7 +r_8 +r_9 +r_10 +r_11 +r_12 +r_13 +r_14 +r_15
  +r_16 +r_17 +b_0 +b_1 +b_2 +b_3 +b_4 +b_5 +b_6 +b_7 +b_8 +b_9 +b_10 +b_11 +b_12 +b_13
  +b_14 +b_15 +b_16 +b_17
Subject To
 red_nonempty: r_0 +r_1 +r_2 +r_3 +r_4 +r_5 +r_6 +r_7 +r_8 +r_9 +r_10 +r_11 +r_12 +r_13
  +r_14 +r_15 +r_16 +r_17 >= 1
 blue_nonempty: b_0 +b_1 +b_2 +b_3 +b_4 +b_5 +b_6 +b_7 +b_8 +b_9 +b_10 +b_11 +b_12 +b_13
  +b_14 +b_15 +b_16 +b_17 >= 1
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
 disjoint_17: r_17 + b_17 <= 1
 red_ind_0: r_0 + r_1 <= 1
 blue_ind_0: b_0 + b_1 <= 1
 red_ind_1: r_0 + r_5 <= 1
 blue_ind_1: b_0 + b_5 <= 1
 red_ind_2: r_0 + r_6 <= 1
 blue_ind_2: b_0 + b_6 <= 1
 red_ind_3: r_0 + r_7 <= 1
 blue_ind_3: b_0 + b_7 <= 1
 red_ind_4: r_0 + r_9 <= 1
 blue_ind_4: b_0 + b_9 <= 1
 red_ind_5: r_0 + r_10 <= 1
 blue_ind_5: b_0 + b_10 <= 1
 red_ind_6: r_0 + r_11 <= 1
 blue_ind_6: b_0 + b_11 <= 1
 red_ind_7: r_0 + r_12 <= 1
 blue_ind_7: b_0 + b_12 <= 1
 red_ind_8: r_0 + r_13 <= 1
 blue_ind_8: b_0 + b_13 <= 1
 red_ind_9: r_0 + r_14 <= 1
 blue_ind_9: b_0 + b_14 <= 1
 red_ind_10: r_0 + r_15 <= 1
 blue_ind_10: b_0 + b_15 <= 1
 red_ind_11: r_0 + r_16 <= 1
 blue_ind_11: b_0 + b_16 <= 1
 red_ind_12: r_0 + r_17 <= 1
 blue_ind_12: b_0 + b_17 <= 1
 red_ind_13: r_1 + r_5 <= 1
 blue_ind_13: b_1 + b_5 <= 1
 red_ind_14: r_1 + r_6 <= 1
 blue_ind_14: b_1 + b_6 <= 1
 red_ind_15: r_1 + r_7 <= 1
 blue_ind_15: b_1 + b_7 <= 1
 red_ind_16: r_1 + r_9 <= 1
 blue_ind_16: b_1 + b_9 <= 1
 red_ind_17: r_1 + r_10 <= 1
 blue_ind_17: b_1 + b_10 <= 1
 red_ind_18: r_1 + r_11 <= 1
 blue_ind_18: b_1 + b_11 <= 1
 red_ind_19: r_1 + r_12 <= 1
 blue_ind_19: b_1 + b_12 <= 1
 red_ind_20: r_1 + r_13 <= 1
 blue_ind_20: b_1 + b_13 <= 1
 red_ind_21: r_1 + r_14 <= 1
 blue_ind_21: b_1 + b_14 <= 1
 red_ind_22: r_1 + r_15 <= 1
 blue_ind_22: b_1 + b_15 <= 1
 red_ind_23: r_1 + r_16 <= 1
 blue_ind_23: b_1 + b_16 <= 1
 red_ind_24: r_1 + r_17 <= 1
 blue_ind_24: b_1 + b_17 <= 1
 red_ind_25: r_2 + r_8 <= 1
 blue_ind_25: b_2 + b_8 <= 1
 red_ind_26: r_3 + r_4 <= 1
 blue_ind_26: b_3 + b_4 <= 1
 red_ind_27: r_5 + r_6 <= 1
 blue_ind_27: b_5 + b_6 <= 1
 red_ind_28: r_5 + r_7 <= 1
 blue_ind_28: b_5 + b_7 <= 1
 red_ind_29: r_5 + r_9 <= 1
 blue_ind_29: b_5 + b_9 <= 1
 red_ind_30: r_5 + r_10 <= 1
 blue_ind_30: b_5 + b_10 <= 1
 red_ind_31: r_5 + r_11 <= 1
 blue_ind_31: b_5 + b_11 <= 1
 red_ind_32: r_5 + r_12 <= 1
 blue_ind_32: b_5 + b_12 <= 1
 red_ind_33: r_5 + r_13 <= 1
 blue_ind_33: b_5 + b_13 <= 1
 red_ind_34: r_5 + r_14 <= 1
 blue_ind_34: b_5 + b_14 <= 1
 red_ind_35: r_5 + r_15 <= 1
 blue_ind_35: b_5 + b_15 <= 1
 red_ind_36: r_5 + r_16 <= 1
 blue_ind_36: b_5 + b_16 <= 1
 red_ind_37: r_5 + r_17 <= 1
 blue_ind_37: b_5 + b_17 <= 1
 red_ind_38: r_6 + r_7 <= 1
 blue_ind_38: b_6 + b_7 <= 1
 red_ind_39: r_6 + r_9 <= 1
 blue_ind_39: b_6 + b_9 <= 1
 red_ind_40: r_6 + r_10 <= 1
 blue_ind_40: b_6 + b_10 <= 1
 red_ind_41: r_6 + r_11 <= 1
 blue_ind_41: b_6 + b_11 <= 1
 red_ind_42: r_6 + r_12 <= 1
 blue_ind_42: b_6 + b_12 <= 1
 red_ind_43: r_6 + r_13 <= 1
 blue_ind_43: b_6 + b_13 <= 1
 red_ind_44: r_6 + r_14 <= 1
 blue_ind_44: b_6 + b_14 <= 1
 red_ind_45: r_6 + r_15 <= 1
 blue_ind_45: b_6 + b_15 <= 1
 red_ind_46: r_6 + r_16 <= 1
 blue_ind_46: b_6 + b_16 <= 1
 red_ind_47: r_6 + r_17 <= 1
 blue_ind_47: b_6 + b_17 <= 1
 red_ind_48: r_7 + r_9 <= 1
 blue_ind_48: b_7 + b_9 <= 1
 red_ind_49: r_7 + r_10 <= 1
 blue_ind_49: b_7 + b_10 <= 1
 red_ind_50: r_7 + r_11 <= 1
 blue_ind_50: b_7 + b_11 <= 1
 red_ind_51: r_7 + r_12 <= 1
 blue_ind_51: b_7 + b_12 <= 1
 red_ind_52: r_7 + r_13 <= 1
 blue_ind_52: b_7 + b_13 <= 1
 red_ind_53: r_7 + r_14 <= 1
 blue_ind_53: b_7 + b_14 <= 1
 red_ind_54: r_7 + r_15 <= 1
 blue_ind_54: b_7 + b_15 <= 1
 red_ind_55: r_7 + r_16 <= 1
 blue_ind_55: b_7 + b_16 <= 1
 red_ind_56: r_7 + r_17 <= 1
 blue_ind_56: b_7 + b_17 <= 1
 red_ind_57: r_9 + r_10 <= 1
 blue_ind_57: b_9 + b_10 <= 1
 red_ind_58: r_9 + r_11 <= 1
 blue_ind_58: b_9 + b_11 <= 1
 red_ind_59: r_9 + r_12 <= 1
 blue_ind_59: b_9 + b_12 <= 1
 red_ind_60: r_9 + r_13 <= 1
 blue_ind_60: b_9 + b_13 <= 1
 red_ind_61: r_9 + r_14 <= 1
 blue_ind_61: b_9 + b_14 <= 1
 red_ind_62: r_9 + r_15 <= 1
 blue_ind_62: b_9 + b_15 <= 1
 red_ind_63: r_9 + r_16 <= 1
 blue_ind_63: b_9 + b_16 <= 1
 red_ind_64: r_9 + r_17 <= 1
 blue_ind_64: b_9 + b_17 <= 1
 red_ind_65: r_10 + r_11 <= 1
 blue_ind_65: b_10 + b_11 <= 1
 red_ind_66: r_10 + r_12 <= 1
 blue_ind_66: b_10 + b_12 <= 1
 red_ind_67: r_10 + r_13 <= 1
 blue_ind_67: b_10 + b_13 <= 1
 red_ind_68: r_10 + r_14 <= 1
 blue_ind_68: b_10 + b_14 <= 1
 red_ind_69: r_10 + r_15 <= 1
 blue_ind_69: b_10 + b_15 <= 1
 red_ind_70: r_10 + r_16 <= 1
 blue_ind_70: b_10 + b_16 <= 1
 red_ind_71: r_10 + r_17 <= 1
 blue_ind_71: b_10 + b_17 <= 1
 red_ind_72: r_11 + r_12 <= 1
 blue_ind_72: b_11 + b_12 <= 1
 red_ind_73: r_11 + r_13 <= 1
 blue_ind_73: b_11 + b_13 <= 1
 red_ind_74: r_11 + r_14 <= 1
 blue_ind_74: b_11 + b_14 <= 1
 red_ind_75: r_11 + r_15 <= 1
 blue_ind_75: b_11 + b_15 <= 1
 red_ind_76: r_11 + r_16 <= 1
 blue_ind_76: b_11 + b_16 <= 1
 red_ind_77: r_11 + r_17 <= 1
 blue_ind_77: b_11 + b_17 <= 1
 red_ind_78: r_12 + r_13 <= 1
 blue_ind_78: b_12 + b_13 <= 1
 red_ind_79: r_12 + r_14 <= 1
 blue_ind_79: b_12 + b_14 <= 1
 red_ind_80: r_12 + r_15 <= 1
 blue_ind_80: b_12 + b_15 <= 1
 red_ind_81: r_12 + r_16 <= 1
 blue_ind_81: b_12 + b_16 <= 1
 red_ind_82: r_12 + r_17 <= 1
 blue_ind_82: b_12 + b_17 <= 1
 red_ind_83: r_13 + r_14 <= 1
 blue_ind_83: b_13 + b_14 <= 1
 red_ind_84: r_13 + r_15 <= 1
 blue_ind_84: b_13 + b_15 <= 1
 red_ind_85: r_13 + r_16 <= 1
 blue_ind_85: b_13 + b_16 <= 1
 red_ind_86: r_13 + r_17 <= 1
 blue_ind_86: b_13 + b_17 <= 1
 red_ind_87: r_14 + r_15 <= 1
 blue_ind_87: b_14 + b_15 <= 1
 red_ind_88: r_14 + r_16 <= 1
 blue_ind_88: b_14 + b_16 <= 1
 red_ind_89: r_14 + r_17 <= 1
 blue_ind_89: b_14 + b_17 <= 1
 red_ind_90: r_15 + r_16 <= 1
 blue_ind_90: b_15 + b_16 <= 1
 red_ind_91: r_15 + r_17 <= 1
 blue_ind_91: b_15 + b_17 <= 1
 red_ind_92: r_16 + r_17 <= 1
 blue_ind_92: b_16 + b_17 <= 1
 red_dom_0: r_1 +r_5 +r_6 +r_7 +r_9 +r_10 +r_11 +r_12 +r_13 +r_14 +r_15 +r_16 +r_17 +r_0
  +b_0 >= 1
 blue_dom_0: b_1 +b_5 +b_6 +b_7 +b_9 +b_10 +b_11 +b_12 +b_13 +b_14 +b_15 +b_16 +b_17 +r_0
  +b_0 >= 1
 red_dom_1: r_0 +r_5 +r_6 +r_7 +r_9 +r_10 +r_11 +r_12 +r_13 +r_14 +r_15 +r_16 +r_17 +r_1
  +b_1 >= 1
 blue_dom_1: b_0 +b_5 +b_6 +b_7 +b_9 +b_10 +b_11 +b_12 +b_13 +b_14 +b_15 +b_16 +b_17 +r_1
  +b_1 >= 1
 red_dom_2: r_8 +r_2 +b_2 >= 1
 blue_dom_2: b_8 +r_2 +b_2 >= 1
 red_dom_3: r_4 +r_3 +b_3 >= 1
 blue_dom_3: b_4 +r_3 +b_3 >= 1
 red_dom_4: r_3 +r_4 +b_4 >= 1
 blue_dom_4: b_3 +r_4 +b_4 >= 1
 red_dom_5: r_0 +r_1 +r_6 +r_7 +r_9 +r_10 +r_11 +r_12 +r_13 +r_14 +r_15 +r_16 +r_17 +r_5
  +b_5 >= 1
 blue_dom_5: b_0 +b_1 +b_6 +b_7 +b_9 +b_10 +b_11 +b_12 +b_13 +b_14 +b_15 +b_16 +b_17 +r_5
  +b_5 >= 1
 red_dom_6: r_0 +r_1 +r_5 +r_7 +r_9 +r_10 +r_11 +r_12 +r_13 +r_14 +r_15 +r_16 +r_17 +r_6
  +b_6 >= 1
 blue_dom_6: b_0 +b_1 +b_5 +b_7 +b_9 +b_10 +b_11 +b_12 +b_13 +b_14 +b_15 +b_16 +b_17 +r_6
  +b_6 >= 1
 red_dom_7: r_0 +r_1 +r_5 +r_6 +r_9 +r_10 +r_11 +r_12 +r_13 +r_14 +r_15 +r_16 +r_17 +r_7
  +b_7 >= 1
 blue_dom_7: b_0 +b_1 +b_5 +b_6 +b_9 +b_10 +b_11 +b_12 +b_13 +b_14 +b_15 +b_16 +b_17 +r_7
  +b_7 >= 1
 red_dom_8: r_2 +r_8 +b_8 >= 1
 blue_dom_8: b_2 +r_8 +b_8 >= 1
 red_dom_9: r_0 +r_1 +r_5 +r_6 +r_7 +r_10 +r_11 +r_12 +r_13 +r_14 +r_15 +r_16 +r_17 +r_9
  +b_9 >= 1
 blue_dom_9: b_0 +b_1 +b_5 +b_6 +b_7 +b_10 +b_11 +b_12 +b_13 +b_14 +b_15 +b_16 +b_17 +r_9
  +b_9 >= 1
 red_dom_10: r_0 +r_1 +r_5 +r_6 +r_7 +r_9 +r_11 +r_12 +r_13 +r_14 +r_15 +r_16 +r_17 +r_10
  +b_10 >= 1
 blue_dom_10: b_0 +b_1 +b_5 +b_6 +b_7 +b_9 +b_11 +b_12 +b_13 +b_14 +b_15 +b_16 +b_17 +r_10
  +b_10 >= 1
 red_dom_11: r_0 +r_1 +r_5 +r_6 +r_7 +r_9 +r_10 +r_12 +r_13 +r_14 +r_15 +r_16 +r_17 +r_11
  +b_11 >= 1
 blue_dom_11: b_0 +b_1 +b_5 +b_6 +b_7 +b_9 +b_10 +b_12 +b_13 +b_14 +b_15 +b_16 +b_17 +r_11
  +b_11 >= 1
 red_dom_12: r_0 +r_1 +r_5 +r_6 +r_7 +r_9 +r_10 +r_11 +r_13 +r_14 +r_15 +r_16 +r_17 +r_12
  +b_12 >= 1
 blue_dom_12: b_0 +b_1 +b_5 +b_6 +b_7 +b_9 +b_10 +b_11 +b_13 +b_14 +b_15 +b_16 +b_17 +r_12
  +b_12 >= 1
 red_dom_13: r_0 +r_1 +r_5 +r_6 +r_7 +r_9 +r_10 +r_11 +r_12 +r_14 +r_15 +r_16 +r_17 +r_13
  +b_13 >= 1
 blue_dom_13: b_0 +b_1 +b_5 +b_6 +b_7 +b_9 +b_10 +b_11 +b_12 +b_14 +b_15 +b_16 +b_17 +r_13
  +b_13 >= 1
 red_dom_14: r_0 +r_1 +r_5 +r_6 +r_7 +r_9 +r_10 +r_11 +r_12 +r_13 +r_15 +r_16 +r_17 +r_14
  +b_14 >= 1
 blue_dom_14: b_0 +b_1 +b_5 +b_6 +b_7 +b_9 +b_10 +b_11 +b_12 +b_13 +b_15 +b_16 +b_17 +r_14
  +b_14 >= 1
 red_dom_15: r_0 +r_1 +r_5 +r_6 +r_7 +r_9 +r_10 +r_11 +r_12 +r_13 +r_14 +r_16 +r_17 +r_15
  +b_15 >= 1
 blue_dom_15: b_0 +b_1 +b_5 +b_6 +b_7 +b_9 +b_10 +b_11 +b_12 +b_13 +b_14 +b_16 +b_17 +r_15
  +b_15 >= 1
 red_dom_16: r_0 +r_1 +r_5 +r_6 +r_7 +r_9 +r_10 +r_11 +r_12 +r_13 +r_14 +r_15 +r_17 +r_16
  +b_16 >= 1
 blue_dom_16: b_0 +b_1 +b_5 +b_6 +b_7 +b_9 +b_10 +b_11 +b_12 +b_13 +b_14 +b_15 +b_17 +r_16
  +b_16 >= 1
 red_dom_17: r_0 +r_1 +r_5 +r_6 +r_7 +r_9 +r_10 +r_11 +r_12 +r_13 +r_14 +r_15 +r_16 +r_17
  +b_17 >= 1
 blue_dom_17: b_0 +b_1 +b_5 +b_6 +b_7 +b_9 +b_10 +b_11 +b_12 +b_13 +b_14 +b_15 +b_16 +r_17
  +b_17 >= 1
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
 r_17
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
 b_17
End
