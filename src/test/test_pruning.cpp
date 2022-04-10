#include "test_pruning.h"

int main() {
  test_pruning({GateType::rx, GateType::rz, GateType::cz,
                GateType::add}, "Rigetti_2_", 3, 2, 2, false, 1, true, false, false, false, true);
  test_pruning({GateType::rx, GateType::rz, GateType::cz,
                GateType::add}, "Rigetti_3_", 3, 2, 3, false, 1, true, false, false, false, true);
  return 0;
  test_pruning({GateType::rz, GateType::h, GateType::cx, GateType::x,
                GateType::add}, "Nam_2_", 3, 2, 2, false, 1, true, false, false, false, true);
  test_pruning({GateType::rx1, GateType::x, GateType::rx3, GateType::rz, GateType::cz,
                GateType::add}, "Rigetti_const_2_", 3, 2, 2, false, 1, true, false, false, false, true);
  return 0;
  test_pruning({GateType::rx1, GateType::x, GateType::rx3, GateType::rz, GateType::cz,
                GateType::add}, "Rigetti_const_3_", 3, 2, 3, false, 1, true, true, false, true, true);
  test_pruning({GateType::rx1, GateType::x, GateType::rx3, GateType::rz, GateType::cz,
                GateType::add}, "Rigetti_const_4_", 3, 2, 4, false, 1, true, true, false, true, true);
  test_pruning({GateType::rx1, GateType::x, GateType::rx3, GateType::rz, GateType::cz,
                GateType::add}, "Rigetti_const_5_", 3, 2, 5, false, 1, true, true, true, false, true);
  test_pruning({GateType::rx1, GateType::x, GateType::rx3, GateType::rz, GateType::cz,
                GateType::add}, "Rigetti_const_6_", 3, 2, 6, false, 1, true, true, true, false, true);
  test_pruning({GateType::rz, GateType::h, GateType::cx, GateType::x,
                GateType::add}, "Nam_3_", 3, 2, 3, false, 1, true, true, false, true, true);
  test_pruning({GateType::rz, GateType::h, GateType::cx, GateType::x,
                GateType::add}, "Nam_4_", 3, 2, 4, false, 1, true, true, false, true, true);
  test_pruning({GateType::u1, GateType::u2, GateType::u3, GateType::cx,
                GateType::add}, "IBM_2_", 3, 4, 2, false, 1, true, true, false, true, true);
  test_pruning({GateType::u1, GateType::u2, GateType::u3, GateType::cx,
                GateType::add}, "IBM_3_", 3, 4, 3, false, 1, true, true, false, true, true);
  test_pruning({GateType::rx, GateType::rz, GateType::cz,
                GateType::add}, "Rigetti_3_", 3, 2, 3, false, 1, true, true, false, true, true);
  test_pruning({GateType::rx, GateType::rz, GateType::cz,
                GateType::add}, "Rigetti_4_", 3, 2, 4, false, 1, true, true, false, true, true);
  test_pruning({GateType::rx, GateType::rz, GateType::cz,
                GateType::add}, "Rigetti_5_", 3, 2, 5, false, 1, true, true, false, true, true);
  test_pruning({GateType::rz, GateType::h, GateType::cx, GateType::x,
                GateType::add}, "Nam_5_", 3, 2, 5, false, 1, true, true, true, false, true);
  test_pruning({GateType::u1, GateType::u2, GateType::u3, GateType::cx,
                GateType::add}, "IBM_4_", 3, 4, 4, false, 1, true, true, true, false, true);
  test_pruning({GateType::rx, GateType::rz, GateType::cz,
                GateType::add}, "Rigetti_6_", 3, 2, 6, false, 1, true, true, true, false, true);
  test_pruning({GateType::rz, GateType::h, GateType::cx, GateType::x,
                GateType::add}, "Nam_6_", 3, 2, 6, false, 1, true, true, true, false, true);
  test_pruning({GateType::rx, GateType::rz, GateType::cz,
                GateType::add}, "Rigetti_7_", 3, 2, 7, false, 1, true, false, true, false, true);
  test_pruning({GateType::rz, GateType::h, GateType::cx, GateType::x,
                GateType::add}, "Nam_7_", 3, 2, 7, false, 1, true, false, true, false, true);
  test_pruning({GateType::u1, GateType::u2, GateType::u3, GateType::cx,
                GateType::add}, "IBM_5_", 3, 4, 5, false, 1, true, false, true, false, true);
//  test_pruning({GateType::rx, GateType::rz, GateType::cz,
//                GateType::add}, "Rigetti_8_", 3, 2, 8, false, 1, true, false, true, false, true);
//  test_pruning({GateType::rz, GateType::h, GateType::cx, GateType::x,
//                GateType::add}, "Nam_8_", 3, 2, 8, false, 1, true, false, true, false, true);
  return 0;
}
