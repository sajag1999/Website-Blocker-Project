'''
This Python script blocks the websites written in the website_list.txt files during the given working hours.
'''

# Import the necessary libraries
import time # For sleep() function
from datetime import datetime as dt 
import platform, os # To check OS type
import ctypes, sys # To run script with admin rights

redirect_url = "127.0.0.1" # Website URL where all the blocked websites would be redirected to.

#Read all websites to be blocked in website_list
web_list_file = open("website_list.txt","r")
website_list = web_list_file.readlines()
web_list_file.close()

# Hours when the websites will be blocked (24 hours format)
STARTING_HOUR = 9
END_HOUR = 20

#Function to check if user is admin or not
def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

# Returns the hosts path depending on operating system
def hosts_path():
	if platform.system() == "Windows":
		hosts = r"C:\Windows\System32\drivers\etc\hosts"
	elif platform.system() == "Darwin" or platform.system() == "Linux": #Darwin represents MacOS
		hosts = r"/etc/hosts"
	else:
		print("Unsupported OS detected. Exiting the program.")
		exit(0)

	return hosts # Returns a string of the location of hosts file

# Actual function which blocks the websites
def web_blocker():
	while True: # Loop runs indefinitely to make sure it blocks and unblocks the websites at correct time

		# Check if current time is between the required hours
		if dt(dt.now().year, dt.now().month, dt.now().day, STARTING_HOUR) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, END_HOUR): 
			print("Working Hours!! Your given websites have been blocked!")
			file = open(hosts_path(), "r+")
			content = file.read()
			for website in website_list:
				if not website in content:
					file.write(redirect_url+" "+website+"\n")
				else:
					pass
			file.close()
		else:
			print("Non Working Hours!! No website has been blocked!")
			with open(hosts_path(),"r+") as file:
				content = file.readlines()
				file.seek(0)
				for line in content:
					if not any(website in line for website in website_list):
						file.write(line)
					file.truncate()
		time.sleep(5) # Executes loop after each 5 seconds

# Main function
def main():
	if platform.system() == "Windows":
		if is_admin():
			# If user is admin, execute the script
			web_blocker()
		else:
			# If user is not admin, open a UAC prompt to execute the script
				ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

	elif platform.system() == "Linux":
		if os.geteuid() != 0: # If user is not root execute the program as root
			os.execvp("sudo", ["sudo"] + sys.argv)
	else:
		print("Incompatible OS. Exiting Program.")
		exit(0)

if __name__ == "__main__":
	main()
