
import csv
import pandas as pd

def json_to_dict(data):
    if isinstance(data, list):
        return [json_to_dict(item) for item in data]
    elif isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = json_to_dict(value)
        return result
    else:
        return data

def generate_csv_from_dict(list, output_file):
  """Generates a CSV file from a dict.

  Args:
    dict: A dict containing the data to be exported to the CSV file.
    output_file: The path to the output CSV file.
  """

  dict = {}
 
  dict = json_to_dict(list)
  # Convert the flat dictionary to a DataFrame (using pandas)
  df = pd.DataFrame.from_dict(dict)

  # Export DataFrame to a CSV file
  df.to_csv("output.csv", index=False)
#   with open(output_file, "w", newline="") as f:
#     # Write the header row.
#     f.write(",".join(dict.keys()) + "\n")
# 
#     # Iterate over the dict and write each row to the file.
#     for row in dict.values():
#       f.write(",".join(row) + "\n")

# if __name__ == "__main__":
#   # Create a dict containing the data to be exported to the CSV file.
#   dict = {
#     "name": ["Alice", "Bob", "Carol"],
#     "age": [25, 30, 35]
#   }
# 
#   # Generate the CSV file.
#   generate_csv_from_dict(dict, "financeiro.csv")
