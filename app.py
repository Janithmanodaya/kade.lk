import tkinter as tk
import customtkinter
import subprocess
import threading
import os
import git
import argparse
import sys

class RepoProcessor:
    def __init__(self, update_callback=None):
        self.update_callback = update_callback

    def log(self, message):
        if self.update_callback:
            self.update_callback(message)
        else:
            print(message, end='')

    def process_repo(self, repo_url):
        try:
            repo_name = repo_url.split("/")[-1].replace(".git", "")
            clone_dir = os.path.join(os.getcwd(), "cloned_repos", repo_name)

            self.clone_repo(repo_url, clone_dir)
            self.install_requirements(clone_dir)
            self.find_and_run(clone_dir)
        except Exception as e:
            self.log(f"An error occurred: {e}\n")

    def clone_repo(self, repo_url, clone_dir):
        self.log(f"Cloning repository from {repo_url} into {clone_dir}...\n")
        if os.path.exists(clone_dir):
            self.log("Repository already exists. Skipping cloning.\n")
            return

        try:
            git.Repo.clone_from(repo_url, clone_dir)
            self.log("Repository cloned successfully.\n")
        except git.exc.GitCommandError as e:
            self.log(f"Error cloning repository: {e}\n")
            raise

    def install_requirements(self, repo_dir):
        requirements_file = os.path.join(repo_dir, "requirements.txt")
        if not os.path.exists(requirements_file):
            self.log("No requirements.txt file found. Skipping dependency installation.\n")
            return

        self.log("Installing dependencies from requirements.txt...\n")
        try:
            if sys.platform == "win32":
                python_executable = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")
            else:
                python_executable = os.path.join(os.getcwd(), "venv", "bin", "python")


            process = subprocess.Popen(
                [python_executable, "-m", "pip", "install", "-r", requirements_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=repo_dir
            )

            for line in iter(process.stdout.readline, ''):
                self.log(line)
            process.stdout.close()
            return_code = process.wait()
            if return_code:
                self.log(f"pip install exited with code {return_code}\n")
                raise subprocess.CalledProcessError(return_code, process.args)
            self.log("Dependencies installed successfully.\n")
        except subprocess.CalledProcessError as e:
            self.log(f"Error installing dependencies: {e}\n")
            raise

    def find_and_run(self, repo_dir):
        possible_files = ["main.py", "app.py", "st.py", "run.py"]
        file_to_run = None
        for file in possible_files:
            if os.path.exists(os.path.join(repo_dir, file)):
                file_to_run = file
                break

        if not file_to_run:
            self.log("Could not find a main file to run (main.py, app.py, st.py, run.py).\n")
            py_files = [f for f in os.listdir(repo_dir) if f.endswith('.py')]
            if len(py_files) == 1:
                self.log(f"Found one python file: {py_files[0]}. Running it.\n")
                file_to_run = py_files[0]
            else:
                self.log(f"Found {len(py_files)} python files in the root directory: {py_files}. Please specify which one to run.\n")
                return

        self.log(f"Running {file_to_run}...\n")
        try:
            if sys..platform == "win32":
                python_executable = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")
            else:
                python_executable = os.path.join(os.getcwd(), "venv", "bin", "python")

            process = subprocess.Popen(
                [python_executable, file_to_run],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=repo_dir
            )
            for line in iter(process.stdout.readline, ''):
                self.log(line)
            process.stdout.close()
            return_code = process.wait()
            if return_code:
                self.log(f"{file_to_run} exited with code {return_code}\n")
            self.log(f"{file_to_run} finished.\n")
        except Exception as e:
            self.log(f"Error running script: {e}\n")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Git Repo Runner")
        self.geometry("700x500")

        self.processor = RepoProcessor(update_callback=self.update_gui)

        # create a text entry box for the git repo url
        self.url_entry = customtkinter.CTkEntry(self, placeholder_text="Enter Git Repository URL")
        self.url_entry.pack(pady=10, padx=10, fill="x")

        # create a scrollable list or dropdown menu for pre-loaded repos
        self.repo_list = customtkinter.CTkOptionMenu(self, values=["https://github.com/pallets/flask", "https://github.com/django/django"], command=self.update_url_entry)
        self.repo_list.pack(pady=10, padx=10, fill="x")
        self.repo_list.set("Select a repository")

        # create a run button
        self.run_button = customtkinter.CTkButton(self, text="Run", command=self.run_repo)
        self.run_button.pack(pady=10, padx=10)

        # create a scrollable text area for command-line output
        self.output_text = customtkinter.CTkTextbox(self, width=680, height=350)
        self.output_text.pack(pady=10, padx=10)

    def update_url_entry(self, choice):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, choice)

    def update_gui(self, message):
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)
        self.update_idletasks()

    def run_repo(self):
        repo_url = self.url_entry.get()
        if not repo_url or repo_url == "Enter Git Repository URL" or repo_url == "Select a repository":
            self.update_gui("Please enter a repository URL or select one from the list.\n")
            return

        self.output_text.delete("1.0", tk.END)
        self.update_gui(f"Starting process for {repo_url}\n")

        thread = threading.Thread(target=self.processor.process_repo, args=(repo_url,))
        thread.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Run in test mode with a specific repo URL")
    args = parser.parse_args()

    if args.test:
        # Run in test mode
        def print_to_console(message):
            print(message, end='')

        processor = RepoProcessor(update_callback=print_to_console)
        processor.process_repo(args.test)
    else:
        # Run in GUI mode
        app = App()
        app.mainloop()
