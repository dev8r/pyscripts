import threading
from pywinauto import Desktop, Application
import time

def handle_modal_dialog(app, dialog_title, button_title, max_attempts=20, interval=1):
    def worker():
        """
        Continuously checks for the modal dialog and clicks the specified button when it appears.

        :param app: The application instance.
        :param dialog_title: The title of the modal dialog.
        :param button_title: The title of the button to click.
        :param max_attempts: Maximum number of attempts to check for the dialog.
        :param interval: Time (in seconds) to wait between attempts.
        """
        attempts = 0
        while attempts < max_attempts:
            try:
 #               if attempts == 0:
                #print(f"Attempt {attempts + 1}: launching modal dialog '{dialog_title}'...")
                # user_search.child_window(title="Search", control_type="Button").click()
#
                print(f"Attempt {attempts + 1}: Checking for modal dialog '{dialog_title}'...")
                model = Application(backend="uia").connect(title=dialog_title, timeout=10)

                #model = Desktop(backend="uia").window(title=dialog_title)
                print(model.window_text())
                #modal_dialog = app.window(title=dialog_title)
                #print(f"Modal dialog '{dialog_title}' found.")
                #modal_dialog.child_window(title=button_title, control_type="Button").click()
                #if modal_dialog.exists(timeout=1):
                #    print(f"Modal dialog '{dialog_title}' found.")
                #     modal_dialog.child_window(title=button_title, control_type="Button").click()
                #     print(f"Clicked '{button_title}' on the '{dialog_title}' dialo\g.")
                #     return
            except Exception as e:
                print(f"Attempt {attempts + 1}: Error handling modal dialog: {e}")
            attempts += 1
            time.sleep(interval)
        print(f"Modal dialog '{dialog_title}' did not appear after {max_attempts} attempts.")
    threading.Thread(target=worker).start()

def close_modal():
    def worker():
        time.sleep(15)
        try:
            modal = Desktop(backend="uia").window(title="No Results")
            print("Modal dialog found.")
            modal.wait('visible', timeout=5)
            print("Modal dialog visible.")
            modal.child_window(title="OK", control_type="Button").click_input()
            print("Clicked 'OK' on the modal dialog.")
        except Exception as e:
            print(f"Error closing modal dialog: {e}")
    threading.Thread(target=worker).start()
   

#C:\GitHub\optifreight-app-webusermanagement\WebUserManagementApplication\WebUserManagementApplication\bin\Debug
# Connect to the app by its window title
#app = Application(backend="uia").connect(title="Web User Management Application", timeout=10)

app = Application(backend="uia").start(r"path_to_app")

# Access the main window
main_window = app.window(title="Web User Management Application")

# Interact with a button
main_window.child_window(title="Search User", control_type="Button").click()

# Wait for the new window to appear
user_search = app.window(title="User Search ")
user_search.wait('visible', timeout=2)
email_edit_box=user_search.child_window(auto_id="tb_Email", control_type="Edit")
email_edit_box.set_text("example@example.com")

#handle_modal_dialog(user_search, "No Results", "OK")
#close_modal()
user_search.child_window(title="Search", control_type="Button").click()

#user_search.print_control_identifiers()
