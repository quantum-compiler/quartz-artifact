#pragma once

#include "matrix.h"

#include <vector>

// An std::vector<ComplexType> to store the distributions.
class Vector {
 public:
  Vector() {}
  Vector(const std::vector<ComplexType> &data) : data_(data) {}
  Vector(std::vector<ComplexType> &&data) : data_(data) {}
  ComplexType &operator[](int x) { return data_[x]; }
  const ComplexType &operator[](int x) const { return data_[x]; }
  [[nodiscard]] int size() const { return (int) data_.size(); }
  bool apply_matrix(MatrixBase *mat, const std::vector<int> &qubit_indices);
 private:
  std::vector<ComplexType> data_;
};
