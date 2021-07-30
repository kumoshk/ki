#!/usr/bin/env python3

import glob, sys, os, subprocess;

path=os.getcwd();


if __name__=="__main__":
    if len(sys.argv)>=2:
        args=sys.argv[1:];
        if len(args)>1:
            args=" ".join(args);
            args=args.strip();
            if not args.endswith(".key"):
                args=args+'.key';
            if "\\" in args:
                args=args.replace("\\", "");
        else:
            args=args[0];
            args=os.path.basename(args);
            if not args.endswith(".key"):
                args=args+".key";
        #print(args);

        g=glob.glob(path+"/**/"+args, recursive=True);
        #print("g: ", g, args);
        try:
            file=g[0];
            dn=os.path.dirname(file);
            bn=os.path.basename(file);
            bn=bn.replace(" ", "\\ ");
            file=dn+os.sep+bn;
            #print(file);
            subprocess.Popen("nano "+file, shell=True).communicate();
        except IndexError:
            yn=input(args+" does not exist. Do you wish to create an open it? (y/n) ");
            if yn in ["yes", "y"]:
                file=args.replace(" ", "\\ ");
                subprocess.Popen("touch "+file, shell=True).communicate();
                print(args+" created.");
                subprocess.Popen("nano "+file, shell=True).communicate();
            else:
                print(args+" not created.");
