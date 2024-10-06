class SparseMatrix:
    def __init__(self, matrix_file_path=None, num_rows=None, num_cols=None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.data = {}

        if matrix_file_path:
            self.load_from_file(matrix_file_path)
    
    def load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()

                self.num_rows = int(lines[0].split('=')[1].strip())
                self.num_cols = int(lines[1].split('=')[1].strip())

                for line in lines[2:]:
                    line = line.strip()
                    if line:  
                        if not self.is_valid_entry(line):
                            raise ValueError("Input file has wrong format")
                        
                        row, col, value = self.parse_entry(line)
                        self.set_element(row, col, value)

        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(e)

    def is_valid_entry(self, line):
        return line.startswith('(') and line.endswith(')')

    def parse_entry(self, line):
        line = line[1:-1].strip()
        parts = line.split(',')
        return int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip())

    def get_element(self, curr_row, curr_col):
        return self.data.get((curr_row, curr_col), 0)

    def set_element(self, curr_row, curr_col, value):
        if value != 0:
            self.data[(curr_row, curr_col)] = value
        elif (curr_row, curr_col) in self.data:
            del self.data[(curr_row, curr_col)]

    def add(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions do not match for addition")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)

        for (row, col), value in self.data.items():
            result.set_element(row, col, value + other.get_element(row, col))
        
        return result

    def subtract(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions do not match for subtraction")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)

        for (row, col), value in self.data.items():
            result.set_element(row, col, value - other.get_element(row, col))
        
        return result

    def multiply(self, other):
        if self.num_cols != other.num_rows:
            raise ValueError("Matrix dimensions do not allow multiplication")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)

        for (row, col), value in self.data.items():
            for k in range(other.num_cols):
                result_value = value * other.get_element(col, k)
                if result_value != 0:
                    result.set_element(row, k, result.get_element(row, k) + result_value)
        
        return result

    def __str__(self):
        output = []
        output.append(f"rows={self.num_rows}")
        output.append(f"cols={self.num_cols}")
        for (row, col), value in self.data.items():
            output.append(f"({row}, {col}, {value})")
        return '\n'.join(output)

def main():
    matrix1_direction = input("Enter the path for the first matrix: ")
    matrix2_direction = input("Enter the path for the second matrix: ")

    matrix1 = SparseMatrix(matrix_file_path=matrix1_direction)
    matrix2 = SparseMatrix(matrix_file_path=matrix2_direction)

    operation = input("Select operation (add/subtract/multiply): ").strip().lower()

    if operation == "add":
        result = matrix1.add(matrix2)
    elif operation == "subtract":
        result = matrix1.subtract(matrix2)
    elif operation == "multiply":
        result = matrix1.multiply(matrix2)
    else:
        print("Invalid operation selected.")
        return
    
    print("Resulting Sparse Matrix:")
    print(result)

if __name__ == "__main__":
    main()
