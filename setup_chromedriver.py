import requests
import zipfile
import os
import json

def download_chromedriver():
    """Download ChromeDriver for Windows"""
    try:
        # Try the very latest ChromeDriver versions that might support Chrome 139
        versions_to_try = [
            "132.0.6834.83",  # Very latest
            "132.0.6834.15",  # Latest beta
            "131.0.6778.108", # Latest stable
            "131.0.6778.85",  # Previous stable
            "130.0.6723.116", # Older stable
        ]
        
        for version in versions_to_try:
            try:
                print(f"Trying ChromeDriver version {version}...")
                # Try new ChromeDriver URL format first
                download_url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/win32/chromedriver-win32.zip"
                
                response = requests.get(download_url)
                if response.status_code == 200:
                    print(f"Downloading ChromeDriver {version}...")
                    
                    # Save the zip file
                    with open("chromedriver.zip", "wb") as f:
                        f.write(response.content)
                    print("ChromeDriver downloaded successfully!")
                    
                    # Extract the zip file
                    with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
                        zip_ref.extractall(".")
                    
                    # Move chromedriver.exe from subfolder if needed
                    if os.path.exists("chromedriver-win32/chromedriver.exe"):
                        import shutil
                        shutil.move("chromedriver-win32/chromedriver.exe", "chromedriver.exe")
                        shutil.rmtree("chromedriver-win32")
                    
                    # Clean up
                    os.remove("chromedriver.zip")
                    print(f"ChromeDriver {version} extracted and ready to use!")
                    
                    return True
                else:
                    # Try old URL format
                    old_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
                    response = requests.get(old_url)
                    if response.status_code == 200:
                        with open("chromedriver.zip", "wb") as f:
                            f.write(response.content)
                        
                        with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
                            zip_ref.extractall(".")
                        
                        os.remove("chromedriver.zip")
                        print(f"ChromeDriver {version} downloaded successfully!")
                        return True
                    
            except Exception as e:
                print(f"Failed to download version {version}: {e}")
                continue
        
        print("All ChromeDriver versions failed. Trying fallback...")
        return False
            
    except Exception as e:
        print(f"Error downloading ChromeDriver: {e}")
        return False

if __name__ == "__main__":
    success = download_chromedriver()
    if success:
        print("\nChrome driver setup complete!")
        print("You can now run: python payment_automation.py")
    else:
        print("\nFailed to download ChromeDriver automatically.")
        print("Please download ChromeDriver manually from:")
        print("https://chromedriver.chromium.org/downloads")
        print("Extract chromedriver.exe to this folder.")
