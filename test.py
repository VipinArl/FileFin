import os

def replicate_structure_with_dummy_files(source_path, destination_path):
    """
    Replicates the folder structure of source_path in destination_path, creating dummy files with matching names.
    
    Args:
        source_path (str): The source directory to replicate.
        destination_path (str): The destination directory where the structure will be replicated.
    """
    if not os.path.exists(source_path):
        print(f"Source path '{source_path}' does not exist.")
        return
    
    for root, dirs, files in os.walk(source_path):
        relative_path = os.path.relpath(root, source_path)
        destination_dir = os.path.join(destination_path, relative_path)
        os.makedirs(destination_dir, exist_ok=True)
        
        for file in files:
            dummy_file_path = os.path.join(destination_dir, file)
            open(dummy_file_path, 'w').close()  # Create an empty file
            print(f"Created: {dummy_file_path}")
            
    print("Replication complete.")

# Example usage
source = r"E:\\Movies"
destination = r".\\Sample"
replicate_structure_with_dummy_files(source, destination)
