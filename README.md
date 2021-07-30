# key
This is a command-line script designed to make reading, writing and editing such as indexes and glossaries from the command-line much easier. Example usage: If you're in a folder called `book/` and type `key author`, it will recursively look through book and its subdirectories for a file named `author.key`; if it finds it, it will open it with nano (nano is a dependency, but you could replace it in the code for something else); if it doesn't find it, it will ask you if you want to create it and open it with nano (a command-line text editor for Linux); the created file will be in the directory that you are currently in (so make sure you're in the desired location or that you move the file later). If you're wondering why I made this it's so I could work on things for creative writing projects more easily via Termux on Android (Termux is basically a command-line Linux for Android). It is not yet optimized for Windows' command-line. I will probably expand this with more features.
