#!/usr/bin/env python3

import glob, sys, os, subprocess, re, pickle;

version="""

Version 0.3.1

Each upload to Github constitutes a new version. I only change the version right before the upload, regardless of whatever else I change in the meantime.

This version only applies to this file (not the other files in the project).

Previous uploads that didn't say the version:
1. 0.1.0 (first upload)
2. 0.1.1 (fixed a typo)
3. 0.2.0 (added persistent data)
4. 0.3.0 (lots of changes)

""".strip();

contact="""
My website: www.growspice.com
Github page: https://github.com/kumoshk/key
""".strip();

path=os.getcwd();
settings={}; #One dictionary for all the settings.
settings["extension"]=".key";
settings["app"]="nano";
settings["lastKeyDir"]=None; #Directory of the last key opened.
settings["defaultDir"]=None; #This is a saved directory for frequent use, which can be changed. You can use it even when you're not in it.
settings["useDefault"]=False; #If this is true then when you're not in a base directory, it will act as if you are in the default directory structure no matter where you are.
settings["baseDirs"]=set(); #This is a set of directories. If you're within these when you use key, it will always search from it even when in its subdirectories. You can't set both a directory and one of its subdirectories to be in baseDirs.
settings["baseDir"]=None; #This is the current base directory (of if there is no current one, it is the last base directory used).
settings["searchBaseDir"]=True; #Whether or not to search for keys from the base dir when in its subdirectories (and so on recursively).
settings["openAll"]=False; #Whether or not to open all files found or just one.
backup=settings.copy();
save_it=False; #If set to True, settings will be saved (pickled). Calling saveSettings() sets it back to False.

#Make sure the user settings folder exists.
settingsPath=os.path.join(os.path.expanduser("~"), ".key");
if not os.path.isdir(settingsPath):
    os.makedirs(settingsPath);

#Load the settings, if they've been saved.
settingsDictPath=os.path.join(settingsPath, "settings_dict.pkl");
if os.path.exists(settingsDictPath):
    with open(settingsDictPath, "rb") as FILE:
        settings=pickle.load(FILE);

def saveSettings():
    #Use this wherever you want to save the settings.
    global save_it, settings;
    save_it=False; #To make sure we don't do redundant saves.
    with open(settingsDictPath, "wb") as FILE:
            pickle.dump(settings, FILE, -1);

baseDir=None;
for x in settings["baseDirs"]:
    if path.startswith(x+os.sep) or x==path:
        baseDir=x;
        if settings["baseDir"]!=baseDir:
            settings["baseDir"]=baseDir;
            save_it=True;
        break;

def addCurrentBaseDir(): #Make the current working directory a base directory.
    global settings, path, save_it;
    for x in settings["baseDirs"]:
        if path==x:
            print("• The current working directory is already a base directory. It cannot be added.");
            return False;
        elif path.startswith(x+os.sep):
            print("• The current working directory is already within the directory structure of a base directory. It cannot be added. Here is the base directory:\n"+x);
            return False;
        elif x==path:
            print("• The current working directory is already a base directory. It cannot be added.");
            return False;
        elif x.startswith(path+os.sep):
            print("• The current working directory has a base directory within its recursive subdirectories. It cannot be added. Here is the base directory:\n"+x);
            return False;
    settings["baseDirs"].add(path); #path is a global variable.
    print("• Adding the current working directory to your list of base directories. Here is the new list of all your base directories:\n"+"\n".join(settings["baseDirs"])+"\n");
    save_it=True;
    return True;


helpString="""
Welcome to key, which is designed to make your command-line life easier. It allows you to open a file (default) or all the files (searching recursively) within a directory structure, with a program of your choice (nano being the default). For instance, if you are in `~/book/` and you type `key Sam Jones` it will search `/book/` and all its subdirectories recursively for a file named `Sam Jones.key`; when it finds one, it will open it with the nano text editor (without changing the current directory).

Note that you must only provide one file name per use of key (and you do not need to surround it with quotes, nor escape spaces); you do not need to type `.key`. You may do these things, however. `.key` is the default file extension, but you can change it, or make it so no extension is used. In order to change the default file extension, simply specify the file extension: e.g. `key test.txt` will change the default file extension to `.txt`; then, when you type `key test2` it will search for `test2.txt`.

If a file does not exist, key will prompt you to create it (and ask where to do so, giving you some convenient options).

Key saves your decisions for future uses of the program. Key is not designed to be used from a script. It is designed for use by humans.

The name key is inspired by dictionary key value pairs (or entries in an index, such as a glossary, or an actual lexicon). Because entries in such tend to have unique names, opening only one file by that name is the default.

Key begins each feedback entry (except for such as this help page) with a bullet, in order to make them more readable.

Combinable options:
• -q: reset the app settings.
• -o: Toggle whether key opens multiple files with the same name (default is false).
• -a: If used, the first word you enter after the flags will be the new default app key uses to open files (if you follow it with a file, it will open it).
• -e: This sets the default file extension to no file extension. (FYI, to set it to another file extension just type out the file extension when you open it the first time; e.g. `key index.html` will set the default file extension to `.html`, and you can type `key index` to access it next time.)
• -d: Set the default directory: If no base directory is set, make the current working directory the default directory. If there is at least one base directory, make the current or last-accessed base directory the default directory (in that priority order). You may only have one default directory at a time.
• -D: Toggle whether to use the default directory (default is False). This overrides everything else (and uses it as your current base directory no matter where you are).
• -b: Make the current working directory a base directory (you can have multiple base directories).
• -r: Remove the current directory (or the current base directory) from being a base directory.
• -s: Toggle whether to search for the key (file) to open from the base directory (if you are inside a base directory structure).
• -c: Clear the list of base directories, or remove the current base directory from being a base directory (you will be prompted which to do).
• -n: List the base directories, and the default directory.
• -h: Print the help.

Non-combinable options:
• --help: Print the help (without the option of doing other stuff at the same time).
Warnings:
• Should the program crash, note that it's possible that some data was not saved during that execution of key (since the print statements occur before the saving in many instances, in order to make the code more efficient).
• Improper configuation may result in undesirable effects. 
• You use this software at your own risk. It comes with no guarantees. You assume all responsibility for what happens by using it, etc.
• Flags are evaluated before the key (the file).

Example usage:
• key -bae rm tester -> This makes the current working directory a base directory and deletes a file called `tester` (no extension); you better remember that it will remove files for future uses until you change that! (e.g. `key my important file` will then delete a file called `my important file`.) Normally, key uses nano (not rm), so if you don't use the -a flag, you should be fine.

To do:
• Make an update option (which downloads and installs the update, if one exists).
• Make it so users can use glob wildcards properly.
• Make more flags, which instead of toggling something will ensure a specific setting is set (in case you forget what was set or something).
• Make a file extension whose name supercedes others and runs code (e.g. Python, Lua, etc.) when accessed (instead of being opened by nano). Make it so you can toggle this on and off.
• Make a file extension whose name supercedes others and opens a random key, or set of keys (with the rules of how to select which ones defined in the file). Also, you could make it so it does opens a/some key(s) according to variables saved somewhere. The idea is to make the command-line itself a text adventure or some such (instead of having to stay in the program the entire time). So, `key the pearl room` might open different files depending on which variables have been set, or which random choice is chosen. Random choices need to be able to define the likelihood of being chosen.
• Debug default directories.
• Add -v and --version flags.
• Add the --about flag.
• Add a manpage entry.
• Make it so you can install it with pip.
• Make --help be an actual file opened with nano.
• Make an install file (which ensures you have nano and touch, too.)
• Make an option to specify a directory structure to search within, followed by the key to search for.
• Make a directory that is used wherever you are when you're not under a base directory structure.
• Make an option to go to a key (or make the key's directory the current working directory). Perhaps make it so it does that every time you open a key.
""".strip();

if __name__=="__main__":
    if len(sys.argv)>=2:
        args=sys.argv[1:];
        pre=" ".join(args).strip(); #string args to test for flags and such before doing any manipulations.
        if pre.startswith("-")==True and pre.startswith("--")==False:
            flags=pre.replace(" -", "");
            flagSplit=flags.split(" ");
            args=flagSplit[1:];
            flags=flagSplit[0];
            if "q" in flags: #Reset app data
                yn=input("• Are you sure you want to reset key's application data? (y/n) ");
                if yn in {"y", "yes"}:
                    settings=backup.copy();
                    baseDir=None;
                    save_it=True;
                    print("• Key's application data has been reset.");
                else:
                    print("• Key's application data has not been reset.");
            if "o" in flags: #Toggle whetehr to open all files with the name at once (instead of just one). Default is False.
                settings["openAll"]=not settings["openAll"];
                print("• Open all files at once set to "+str(settings["openAll"])+".");
                save_it=True
            if "a" in flags: #-p This means the next non-flag group of characters is the new default app to use instead of nano, or whatever.
                settings["app"]=args[0];
                print("• Files will now opened with "+settings["app"]+" by default.\n");
                args=args[1:];
                save_it=True;
            if "e" in flags: #Make the default extension no extension.
                settings["extension"]="";
                print("• The default extension is now no extension.\n");
                save_it=True;
            if "d" in flags: #Make the current or last-accessed base directory the default directory, or if there is none, make the current working directory the default directory (and a base directory).
                if settings["baseDir"]==None:
                    yn=input("• No base directories exist. Would you like to make the current working directory a base directory (and the default directory)? (y/n) ");
                    if yn in {"y", "yes"}:
                        addCurrentBaseDir();
                        #settings["baseDirs"].add(path);
                        settings["defaultDir"]=path;
                        baseDir=path;
                        settings["baseDir"]=path;
                        print("• The current working directory is now a base directory and the default directory.");
                        save_it=True;
                    else:
                        print("• New default directory not set.");
                else:
                    if baseDir==None:
                        settings["defaultDir"]=path;
                        #&&&Make sure you're adding the baseDirs right.
                        itWorked=addCurrentBaseDir();
                        #settings["baseDirs"].add(path);
                        if itWorked==True:
                            print("• The current working directory is now set to be the default directory.");
                        else:
                            print("• The current working directory has not been set to be the default directory.");
                    else:
                        settings["defaultDir"]=settings["baseDir"];
                        if settings["defaultDir"]==baseDir:
                            print("• The current base directory is now set to be the default directory:\n"+settings["defaultDir"]);
                        else:
                            print("• The last-accessed base directory is now set to be the default directory:\n"+settings["defaultDir"]);
                    save_it=True;
            if "D" in flags: #Toggle whether to use the default directory when you aren't in a base directory.
                settings["useDefault"]=not settings["useDefault"];
                print("• Use default directory (when not in a base directory structure) set to "+str(settings["useDefault"])+".");
                save_it=True;
            if "b" in flags: #Add the current working directory (not that of the key opened_ to baseDirs.
                addCurrentBaseDir();
            if "r" in flags: #Remove the current directory or current base directory from being a base directory.
                if baseDir==None:
                    print("• You are not in a base directory structure and so cannot remove it from being a base directory (because it isn't one). No base directory removed from being a base directory.");
                else:
                    yn=input("• Are you sure you want to remove the current base directory from being a base directory? FYI, if so, if it's the default directory, it will no longer be the default. (y/n) ");
                    if yn in {"y", "yes"}:
                        settings["baseDirs"].remove(baseDir);
                        if settings["baseDir"]==baseDir:
                            settings["baseDir"]=None;
                        if settings["defaultDir"]==baseDir:
                            settings["defaultDir"]=None;
                            print("• The default directory is no longer set.");
                        save_it=True;
                        print("• The current base directory has been removed from being a base directory:\n"+baseDir);
                        baseDir=None;
                    else:
                        print("• The current base directory is unchanged (still a base directory).");
            if "s" in flags: #Toggle whether to search for the key to open from the base directory (default is True).
                settings["searchBaseDir"]=not settings["searchBaseDir"];
                print("• Searching for keys from the base directory set to "+str(settings["searchBaseDir"])+".");
                save_it=True;
            if "c" in flags: #Clear the list of base directories, or remove the current base directory from being a base directory.
                if len(settings["baseDirs"])>0:
                    yn=input("• Are you sure you want to clear the following base directories?\n"+"\n".join(settings["baseDirs"])+"\n(y/n; press c to remove only the current base directory.) ");
                    if yn in {"y", "yes"}:
                        settings["baseDirs"].clear();
                        save_it=True;
                        print("• Base directories cleared.");
                        baseDir=None;
                        if settings["defaultDir"]!=None:
                            settings["defaultDir"]=None;
                            print("• The default directory has been removed.");
                    elif yn=="c":
                        if baseDir==None:
                            print("• You are not in a base directory. It cannot be removed.");
                        else:
                            settings["baseDirs"].remove(baseDir);
                            save_it=True;
                            print("• The following directory is no longer a base directory:\n"+baseDir);
                            baseDir=None;
                    else:
                        print("• Base directories not cleared.");
                else:
                    print("• You don't have any base directories set to clear.");
            if "n" in flags: #List the base directories and the default directory.
                print("• Default directory:\n"+str(settings["defaultDir"]));
                if len(settings["baseDirs"])>0:
                    print("• Base directories:\n"+"\n".join(settings["baseDirs"]));
                else:
                    print("• Base directories:\nNone");
            if "h" in flags: #Print the help string.
                print("\n\n"+helpString+"\n\n");
        elif pre.startswith("--")==True:
            args=[]; #Clear the args so it won't do anything else.
            if pre=="--help":
                print(helpString);
            elif pre=="--version":
                pass;
            elif pre=="--about":
                pass;
        if len(args)!=0:
            if "." in args[-1]: #If an extension is specified, make it the new default extension (it goes from the final period to the end of the filename).
                newExt="."+args[-1].split(".")[-1];
                if newExt!=settings["extension"]:
                    settings["extension"]=newExt;
                    print("• Default extension changed to `"+settings["extension"]+"`.");
                    #saveSettings();
                    save_it=True;
            if len(args)>1:
                args=" ".join(args);
                args=args.strip();
                if not args.endswith(settings["extension"]):
                    args=args+settings["extension"];
                if "\\" in args:
                    args=args.replace("\\", "");
            else:
                args=args[0];
                args=os.path.basename(args);
                if not args.endswith(settings["extension"]):
                    args=args+settings["extension"];

            g=None;
            if settings["searchBaseDir"]==True and baseDir!=None:
                if settings["useDefault"]==True and settings["defaultDir"]!=None:
                    g=glob.glob(settings["defaultDir"]+"/**/"+args, recursive=True);
                else:
                    g=glob.glob(baseDir+"/**/"+args, recursive=True);
            else:
                if settings["searchBaseDir"]==True and settings["useDefault"]==False:
                    print("• There is no base directory here; using the current working directory.");
                    g=glob.glob(path+"/**/"+args, recursive=True);
                elif settings["searchBaseDir"]==True and settings["useDefault"]==True and settings["defaultDir"]!=None:
                    print("• Using the default directory:\n"+settings["defaultDir"]);
                    g=glob.glob(settings["defaultDir"]+"/**/"+args, recursive=True);
                elif settings["useDefault"]==True:
                    if settings["defaultDir"]!=None:
                        g=glob.glob(settings["defaultDir"]+"/**/"+args, recursive=True);
                    else:
                        print("• The default directory is not set. (Acting as if it is disabled.)");
                        if baseDir==None:
                            print("• There is no base directory here; using the current working directory.");
                        g=glob.glob(path+"/**/"+args, recursive=True);
                else:
                    g=glob.glob(path+"/**/"+args, recursive=True);
            try:
                allFound=[];
                firstFile=True;
                for f in g:
                    dn=os.path.dirname(f);
                    bn=os.path.basename(f);
                    f=dn+os.sep+bn;
                    f=re.sub(r"\\* ", r"\\ ", f);
                    allFound.append(f);
                    if firstFile==True:
                        if settings["lastKeyDir"]!=dn:
                            settings["lastKeyDir"]=dn;
                            print("• Last key directory set to `"+settings["lastKeyDir"]+"`.");
                            #saveSettings();
                            save_it=True;
                        firstFile=False;
                if settings["openAll"]==False:
                    subprocess.Popen(settings["app"]+" "+allFound[0], shell=True).communicate();
                else:
                    subprocess.Popen(settings["app"]+" "+" ".join(allFound), shell=True).communicate();
            except IndexError:
                yn=None;
                def chunk():
                    global settings, path;
                    if settings["defaultDir"]==None:
                        return False;
                    else:
                        return settings["defaultDir"].startswith(path+os.sep);
                if settings["useDefault"]==True and (chunk() or settings["defaultDir"]==path):
                    yn=input("• "+args+" does not exist.\n• Do you wish to create and open it (n = no; y = current working directory; b = base directory; k = directory of the last key opened?) ");
                elif settings["useDefault"]==True and settings["defaultDir"]!=None:
                    yn=input("• "+args+" does not exist.\n• Do you wish to create and open it (n = no; b = base directory; k = directory of the last key opened?) ");
                    if yn in {"y", "yes"}:
                        yn="n";
                else:
                    yn=input("• "+args+" does not exist.\n• Do you wish to create and open it (n = no; y = current working directory; b = base directory; k = directory of the last key opened?) ");
                if yn in {"y", "yes"}:
                    rfile=re.sub(r"\\* ", r"\\ ", args);
                    if settings["lastKeyDir"]!=path:
                        settings["lastKeyDir"]=path;
                        print("• Last key directory set to `"+settings["lastKeyDir"]+"`.");
                        #saveSettings();
                        save_it=True;
                    subprocess.Popen("touch "+rfile, shell=True).communicate();
                    print("• "+args+" created.");
                    subprocess.Popen(settings["app"]+" "+rfile, shell=True).communicate();
                elif yn=="b":
                    if settings["useDefault"]==True and settings["defaultDir"]!=None:

                        file=os.path.join(settings["defaultDir"], os.path.basename(args));
                        rfile=re.sub(r"\\* ", r"\\ ", file);
                        if settings["lastKeyDir"]!=settings["defaultDir"]:
                            settings["lastKeyDir"]=settings["defaultDir"];
                            print("• Last key directory set to `"+settings["lastKeyDir"]+"`.");
                            #saveSettings();
                            save_it=True;
                        subprocess.Popen("touch "+rfile, shell=True).communicate();
                        print("• "+args+" created in the default directory:\n"+file);
                        subprocess.Popen(settings["app"]+" "+rfile, shell=True).communicate();
                    else:
                        if settings["useDefault"]==True and settings["defaultDir"]==None:
                            print("• No default directory has been set. Acting as if the default directory is disabled.");
                        if baseDir==None:
                            print("• You are not within a base directory structure.");
                            if settings["baseDir"]==None:
                                print("• "+args+" not created.");
                            else:
                                yn2=input("• Would you like to create it within the last-accessed base directory? (y/n) ");
                                if yn2 in {"y", "yes"}:
                                    file=os.path.join(settings["baseDir"], os.path.basename(args));
                                    rfile=re.sub(r"\\* ", r"\\ ", file);
                                    if settings["lastKeyDir"]!=settings["baseDir"]:
                                        settings["lastKeyDir"]=settings["baseDir"];
                                        print("• Last key directory set to `"+settings["lastKeyDir"]+"`.");
                                        #saveSettings();
                                        save_it=True;
                                    subprocess.Popen("touch "+rfile, shell=True).communicate();
                                    print("• "+args+" created in the last-accessed base directory:\n"+file);
                                    subprocess.Popen(settings["app"]+" "+rfile, shell=True).communicate();
                                else:
                                    print("• "+args+" not created.");
                        else:
                            file=os.path.join(baseDir, os.path.basename(args));
                            rfile=re.sub(r"\\* ", r"\\ ", file);
                            if settings["lastKeyDir"]!=baseDir:
                                settings["lastKeyDir"]=baseDir;
                                print("• Last key directory set to `"+settings["lastKeyDir"]+"`.");
                                #saveSettings();
                                save_it=True;
                            subprocess.Popen("touch "+rfile, shell=True).communicate();
                            print("• "+args+" created in the base directory:\n"+file);
                            subprocess.Popen(settings["app"]+" "+rfile, shell=True).communicate();
                elif yn=="k":
                    if settings["useDefault"]==True and settings["defaultDir"]!=None and settings["lastKeyDir"].startswith(settings["defaultDir"])==False:
                        print("• The last key directory is not within the default directory structure. No file created.");
                    else:
                        if settings["useDefault"]==True and settings["defaultDir"]==None:
                            print("• The default directory is not set. Acting as if the default directory is disabled.");
                        file=os.path.join(settings["lastKeyDir"], os.path.basename(args));
                        rfile=re.sub(r"\\* ", r"\\ ", file);
                        subprocess.Popen("touch "+rfile, shell=True).communicate();
                        print("• "+args+" created in the last key directory:\n"+file);
                        subprocess.Popen(settings["app"]+" "+rfile, shell=True).communicate();
                else:
                    print("• "+args+" not created.");
    if save_it==True:
        saveSettings();
