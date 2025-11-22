import os

class Dataloader:
    """ a memory efficient image loader that yields file paths one by one
    designed to handle massive datasets without loading file lists into RAM"""

    def __init__(self, folder_paths):
        """initialize the loader with a list of folder paths"""

        # we check if a list was given or a string

        if isinstance(folder_paths, str):
            self.folders = [folder_paths]
        else:
            self.folders = folder_paths

        self.VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}

        pass

    def scan(self):
        """generator that yields image paths one by one"""

        for folder in self.folders:
            if not os.path.exists(folder):
                print(f"warning: folder not found {folder}")
                continue
            
            try:
                with os.scandir(folder) as entities:
                    for entry in entities:
                        if entry.is_file():
                            _, ext = os.path.splitext(entry.name)

                            if ext.lower() in self.VALID_EXTENSIONS:
                                yield entry.path
            except PermissionError:
                print(f"permission denied for {folder}")
                continue


# # --- Usage Example (Debug Block) ---
# if __name__ == "__main__":
#     # Create some dummy folders/files for testing if they don't exist
#     test_dir = "test_input_loader"
#     os.makedirs(test_dir, exist_ok=True)
#     with open(os.path.join(test_dir, "test1.jpg"), "w") as f: f.write("dummy")
#     with open(os.path.join(test_dir, "test2.png"), "w") as f: f.write("dummy")
#     with open(os.path.join(test_dir, "ignore.txt"), "w") as f: f.write("dummy")

#     # Initialize
#     loader = DataLoader([test_dir])
    
#     print("Scanning...")
#     # The loop pulls one file at a time from the generator
#     count = 0
#     for image_path in loader.scan():
#         print(f"Found: {image_path}")
#         count += 1
    
#     print(f"Total images found: {count}")
    
#     # Cleanup
#     import shutil
#     shutil.rmtree(test_dir)
