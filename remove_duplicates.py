from core.Bots.blockeds.shit_isps import bot_keywords_SHIT_ISPS



def remove_duplicates_and_save_to_file(input_list, output_file):
    # Remove duplicates by converting the list to a set and back to a list
    unique_items = list(set(input_list))
    
    # Sort the list if you want the output to be sorted (optional)
    unique_items.sort()
    
    # Save the Python list format to the text file
    with open(output_file, 'w',  encoding='utf-8') as file:
        file.write(f"{unique_items}\n")  # Write the list in Python list format
    
    print(f"Unique items have been saved to {output_file}")
    print(f"#####  After Count: {len(unique_items)}")


if __name__ == "__main__":

    # Print before count
    print(f"#####  Before Count: {len(bot_keywords_SHIT_ISPS)}")
  
    # Output file name
    output_file = "unique_items.txt"
    
    # Call the function to remove duplicates and save to the file
    remove_duplicates_and_save_to_file(bot_keywords_SHIT_ISPS, output_file)
