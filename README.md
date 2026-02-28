Downloads Folder Organizer
A simple, efficient Python script to declutter your Downloads directory. It automatically sorts files into specific subfolders based on their file extensions to keep your workspace organized.

Features
Automatic Categorization: Sorts files into specific folders:

all pdf/ for .pdf

all mkv/ for .mkv

png/ for .png

mp4/ for .mp4

docs/ for .docx, .doc, and .txt

Non-Destructive: Only moves files; does not delete data.

Lightweight: Written in pure Python with minimal dependencies.

How it Works
The script scans the current user's Downloads folder, identifies the extension of every file, and moves it to the corresponding destination folder. If the destination folder doesn't exist, the script creates it automatically.

Getting Started
Prerequisites
Python 3.x installed on your system.

Installation
Clone the repository:

Bash
git clone https://github.com/yourusername/downloads-organizer.git
Navigate to the directory:

Bash
cd downloads-organizer
Usage
Run the script manually to clean your folder:

Bash
python fileorganizer.py
Future Improvements
Duplicate Handling: Adding logic to rename files if a file with the same name already exists in the destination.

Background Monitoring: Implementing watchdog to move files instantly as they are downloaded.

Custom Mapping: Allowing users to define their own folder names via a JSON config file.
