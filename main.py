import json
import re
import os
from colorist import Color
from InquirerPy import prompt
from prettytable import PrettyTable


# Best practices
best_practices_verified = []


# Banner
def banner():
    print(f"""{Color.BLUE}
                            _             _____             __ _          _____                 
     /\                    | |           / ____|           / _(_)        / ____|                
    /  \   _ __   __ _  ___| |__   ___  | |     ___  _ __ | |_ _  __ _  | (___   ___ __ _ _ __  
   / /\ \ | '_ \ / _` |/ __| '_ \ / _ \ | |    / _ \| '_ \|  _| |/ _` |  \___ \ / __/ _` | '_ \ 
  / ____ \| |_) | (_| | (__| | | |  __/ | |___| (_) | | | | | | | (_| |  ____) | (_| (_| | | | |
 /_/    \_| .__/ \__,_|\___|_| |_|\___|  \_____\___/|_| |_|_| |_|\__, | |_____/ \___\__,_|_| |_|
          | |                                                     __/ |                         
          |_|                                                    |___/    {Color.RED}By TheMalwareGuardian{Color.BLUE}
 
 Security best practices in Apache server configuration files
    {Color.OFF}""")
    print('\n')


# Read the JSON data
def read_json_best_practices():
    with open("best_practices.json", "r", encoding='utf-8') as json_file:
        best_practices_data = json.load(json_file)
    return best_practices_data


# Best practices to secure Apache HTTP server
def best_practices_apache():

    # Read the JSON data
    best_practices_data = read_json_best_practices()

    # Table
    table = PrettyTable()
    table.field_names = ["Best Practice", "Configuration"]
    table.align["Configuration"] = "l"

    # Best practice and configuration
    for apache_best_practice_key, apache_best_practice_key_values in best_practices_data.items():
        table.add_row([f"{Color.BLUE}" + apache_best_practice_key_values['name'] + f"{Color.OFF}", ""])
        for apache_best_practice_configuration in apache_best_practice_key_values['configuration']:
            table.add_row(["", apache_best_practice_configuration])
        table.add_row(["", "---------------------------------------"])
    
    # Print
    print(table)


# Get config files
def get_config_files(directory, recursive):
    config_files = []
    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if '.conf' in file or '.include' in file:
                    config_files.append(os.path.join(root, file))
    else:
        config_files = [
            os.path.join(directory, file)
            for file in os.listdir(directory)
            if '.conf' in file or '.inclue' in file
        ]
    return config_files


# Check configuration files
def check_configuration_directory_recursive(recursive_value):

    # Ask the user
    user_directory = input('Enter the directory path where Apache configuration files are located (e.g., C:\\Users\\user1\\Downloads): ')

    if not os.path.isdir(user_directory):
        print('Invalid directory path. Please make sure the directory exists and try again.')
        return

    # Get configuration files
    config_files_list = get_config_files(user_directory, recursive_value)

    # Configuration
    for config_file in config_files_list:
        check_configuration(config_file)


# Check configuration file
def check_configuration_file():

    # Ask the user
    config_file = input('Enter the Apache configuration file (e.g., C:\\Users\\user1\\Downloads\\apache2.conf): ')

    # Is file
    if not os.path.isfile(config_file):
        print('Invalid file path. Please make sure the file exists and try again.')
        return
    else:
        # Configuration
        check_configuration(config_file)


# Check Configuration
def check_configuration(config_file):

    # File name
    print('File:', os.path.basename(config_file))
    print('Path:', os.path.dirname(config_file))

    # Read the JSON data
    best_practices_data = read_json_best_practices()

    # Read the content of the file
    with open(config_file, "r") as file:
        file_check_content = file.read().lower()

    # Table
    table = PrettyTable()
    table.field_names = ["Best Practice", "Implemented"]

    # Best Practices
    for apache_best_practice_key, apache_best_practice_key_values in best_practices_data.items():
        # Status True
        if apache_best_practice_key_values['status']:
            # Regex
            regex_all_match = False
            for regex_pattern in apache_best_practice_key_values['regex']:
                regex_pattern = regex_pattern.strip()
                pattern = re.compile(regex_pattern)
                if pattern.search(file_check_content):
                    regex_all_match = True
                    break

            # Match
            if regex_all_match:
                table.add_row([apache_best_practice_key_values['name'], f"{Color.GREEN}YES{Color.OFF}"])
                # Implemented
                if apache_best_practice_key not in best_practices_verified:
                    best_practices_verified.append(apache_best_practice_key)
            else:
                table.add_row([apache_best_practice_key_values['name'], f"{Color.RED}NO{Color.OFF}"])

    # Print
    print(table)
    print('\n')


# Not Implemented
def not_implemented():

    # Read the JSON data
    best_practices_data = read_json_best_practices()

    # Table
    table = PrettyTable()
    table.field_names = ["Best Practice", "Impact"]

    # Best Practices
    print(f"{Color.GREEN}IMPLEMENTED{Color.OFF}")
    print(f"{Color.YELLOW}NOT IMPLEMENTED{Color.OFF}")
    for apache_best_practice_key, apache_best_practice_key_values in best_practices_data.items():
        # Status True and Not Implemented
        if apache_best_practice_key_values['status']:
            if apache_best_practice_key not in best_practices_verified:
                table.add_row([f"{Color.YELLOW}{apache_best_practice_key_values['name']}{Color.OFF}", apache_best_practice_key_values['impact']])
            else:
                table.add_row([f"{Color.GREEN}{apache_best_practice_key_values['name']}{Color.OFF}", apache_best_practice_key_values['impact']])

    # Print
    print(table)
    print('Run the first option of the script to see how to implement each best practice')
    print('\n')


# Main
def main():

    try:

        # Banner
        banner()

        # Options
        option_best_practices = 'Best practices to secure Apache HTTP server'
        option_check_file = 'Check for best practices in Apache configuration file (File)'
        option_check_directory = 'Check for best practices in Apache configuration files (Directory)'
        option_check_recursive = 'Check for best practices in Apache configuration files (Recursive)'
        option_exit = 'Exit'

        # Question
        question = {
            "type": "list",
            "message": "Select an action:",
            "choices": [option_best_practices, option_check_file, option_check_directory, option_check_recursive, option_exit]
        }

        # Loop
        while True:

            # Clear
            best_practices_verified.clear()

            # Prompt
            result = prompt(questions=question)

            # Menu
            if result[0] == option_best_practices:
                best_practices_apache()
            elif result[0] == option_check_file:
                check_configuration_file()
                not_implemented()
            elif result[0] == option_check_directory:
                check_configuration_directory_recursive(False)
                not_implemented()
            elif result[0] == option_check_recursive:
                check_configuration_directory_recursive(True)
                not_implemented()
            elif result[0] == option_exit:
                exit(0)
            else:
                print('Invalid option. Please choose a valid action.')

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
