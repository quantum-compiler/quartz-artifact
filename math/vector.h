#pragma once

#include "matrix.h"

// An std::vector<ComplexType> to store the distributions.
class Vector {
 public:
  Vector() {}
  Vector(const std::vector<ComplexType> &data) : data_(data) {}
  Vector(std::vector<ComplexType> &&data) : data_(data) {}
  ComplexType &operator[](int x) { return data_[x]; }
  const ComplexType &operator[](int x) const { return data_[x]; }
  bool apply_matrix(MatrixBase *mat, const std::vector<int> &qubit_indices);
 private:
  std::vector<ComplexType> data_;
};
