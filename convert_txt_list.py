def convert_txt_to_python_list(input_file, output_file):
    # Step 1: Read the content from the input .txt file
    with open(input_file, 'r') as file:
        # Read lines and strip any extra spaces or newline characters
        lines = [line.strip() for line in file.readlines()]

    # Step 2: Convert list of lines into a Python list representation
    python_list = str(lines)

    # Step 3: Write the Python list to the output file
    with open(output_file, 'w') as file:
        file.write(f"{python_list}\n")

    print(f"Python list saved to {output_file}")

# Example usage
input_file = 'input_list.txt'  # Input file with your list
output_file = 'output_list.txt'  # Output file to save the Python list
convert_txt_to_python_list(input_file, output_file)
