#!/usr/bin/env python3

import glob, sys, os, subprocess, re, pickle;

path=os.getcwd();
settings={"extension": ".key"}; #One dictionary for all the settings.
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
    global settings;
    with open(settingsDictPath, "wb") as FILE:
            pickle.dump(settings, FILE, -1);

if __name__=="__main__":
    if len(sys.argv)>=2:
        args=sys.argv[1:];
        if "." in args[-1]: #If an extension is specified, make it the new default extension (it goes from the final period to the end of the filename).
            newExt="."+args[-1].split(".")[-1];
            if newExt!=settings["extension"]:
                settings["extension"]=newExt;
                print("Default extension changed to `"+settings["extension"]+"`.");
                saveSettings();
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
        #print(args);

        g=glob.glob(path+"/**/"+args, recursive=True);
        #print("g: ", g, args);
        try:
            file=g[0];
            dn=os.path.dirname(file);
            bn=os.path.basename(file);
            #bn=bn.replace(" ", "\\ ");
            file=dn+os.sep+bn;
            file=re.sub(r"\\* ", r"\\ ", file);
            #print(file);
            subprocess.Popen("nano "+file, shell=True).communicate();
        except IndexError:
            yn=input(args+" does not exist. Do you wish to create and open it? (y/n) ");
            if yn in ["yes", "y"]:
                file=re.sub(r"\\* ", r"\\ ", args);
                #file=args.replace(" ", "\\ ");
                subprocess.Popen("touch "+file, shell=True).communicate();
                print(args+" created.");
                subprocess.Popen("nano "+file, shell=True).communicate();
            else:
                print(args+" not created.");

