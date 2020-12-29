import json
import os
import re
import time

from collections import OrderedDict
from datetime import datetime as dt
from operator import itemgetter
import vim

languages = {"py": ["#"], "js": ["//"], "md": ["[//]: #"]}

class Lackey:
    
    def __init__(self):
        self.task_map = {}
        self.ignores = ["__pycache__", "node_modules", "venv", "virtualenv"]
        self.tags = ["DOCS", "FEAT", "FIX", "NOTE",
                     "REFACTOR", "STYLE", "TEST", "TODO"]
        self.tag_pattern = "|".join(self.tags)
        self.win_id = 0
        self.border_id = 0
        
        self.lackey_path = self._get_lackey_json_path(os.getcwd())
        self.file_paths = []

    def _get_window_size(self):
        """Returns the width and height of the Vim editor window.

        Returns
        -------
        tuple
            Tuple containing the width of the editor as the first element
            and the height as the second element.
        """
        dims = vim.api.list_uis()[0]
        w = dims["width"]
        h = dims["height"]
        return (w, h)

    def _create_win(self, messages):
        """Opens a floating window in Vim and displays message in the buffer.

        Parameters
        ----------
        messages : list           Messages to be put into the buffer.
        """
        w, h = self._get_window_size()
        buffer_handler = vim.api.create_buf(False, True)
        self.win_id = vim.api.open_win(
                buffer_handler,
                True,
                {
                    "relative":"editor",
                    "width":w-12,
                    "height":h-12,
                    "col":8,
                    "row":4,
                    "style":"minimal"
                }
            )
        vim.api.buf_set_keymap(buffer_handler,
                               "n", ":q<CR>", ":call LackeyClose()<CR>", {})
        vim.api.buf_set_keymap(buffer_handler,
                               "n", "q", ":call LackeyClose()<CR>", {})
        vim.api.buf_set_keymap(buffer_handler,
                               "n", "<Esc>", ":call LackeyClose()<CR>", {})
        for key in self.task_map.keys():
            vim.api.buf_set_keymap(buffer_handler,
                                   "n", key+"<CR>",
                                   ":call LackeyGo("+key+")<CR>", {})
        vim.api.win_set_option(self.win_id, "winhl", "Normal:MyNormal")
        vim.api.put(messages, "l", False, False)
        self._add_border()

    def _add_border(self):
        """Draw separate windo that is slightly bigger that the task window.

        This window is created to be able to simulate a border,
        because the current `nvim_open_win` API does not support borders.
        """
        opts = vim.api.win_get_config(self.win_id)
        border_buf = vim.api.create_buf(False, True)
        vim.api.buf_set_option(border_buf, "bufhidden", "wipe")
        opts["width"] += 2
        opts["height"] += 2
        opts["row"] -= 1
        opts["col"] -= 1
        opts["style"] = "minimal"
        opts["focusable"] = False
        self.border_id = vim.api.open_win(border_buf, False, opts)
        vim.api.win_set_option(self.border_id, 'winhl', 'Normal:StatusLine')

    def _get_lackey_json_path(self, path):
        """Returns path of `lackey.json` in any one of the upper level
        directories. 

        Walks up from arg `path`, until it finds `lackey.json`. If it is not
        found, return `False`.

        Parameters
        ----------
        path : str
            Base directory to walk up from.

        Returns
        -------
        str or bool
            Returns path containing `lackey.json` if found,
            otherwise return `False`
        """
        files = os.listdir(path)
        if "lackey.json" in files:
            return path
        else:
            next_dir = self._move_up_dir(path)
            if next_dir == 0:
                return False
            else:
                return self._get_lackey_json_path(next_dir)

    def _get_project_files(self):
        """Returns a list of all non-ignored files to be scanned.
        
        Walks down from the lackey root folder.

        Returns
        -------
        list
            A list of files that are not set to be ignored.

            Refer to the Lackey doc to see which files and folders
            are ignored by default.
        """
        for root, dirs, files in os.walk(self.lackey_path, topdown=True):
            dirs[:] = [d for d in dirs if re.match("^[^.].*$", d) and d not in self.ignores]

            for f in files:
                self.file_paths.append(os.path.join(root, f))

    def _move_up_dir(self, path):
        """Return the path of upper directory for a given path.

        Parameters
        ----------
        path : str
            Path of the directory to split.

        Returns
        -------
        str
            Path of the directory, one level up.
        """
        split_paths = os.path.split(path)
        if split_paths[1] == "":
            return 0
        return split_paths[0]

    def _load_tasks(self):
        """Returns collections.OrderedDict with Lackey tasks."""
        # change to dynamic loading:
        self.lackey_path = self._get_lackey_json_path(os.getcwd())
        if not self.lackey_path:
           return False
        json_file = open("H:/python/vim-lackey/lackey.json", "r")
        tasks = json.load(json_file)
        json_file.close()
        return OrderedDict(sorted(tasks.items()))

    def _sort_by_date(self, obj, ascending=False):
        """Returns collections.OrderedDict sorted by date.

        Parameters
        ----------
        obj : collections.OrderedDict
            List of task items.
        ascending : bool, optional
            If True, will sort by date in ascending order (old to new).

        Returns
        -------
        collections.OrderedDict
            OrderedDict object with the same items but sorted by date.
        """
        return sorted(obj, key=itemgetter("timestamp"), reverse=ascending)

    def lackey_show(self):
        """Open a popup window in Neovim and display all tasks."""
        tasks = self._load_tasks()
        if not tasks:
            print("Could not find 'lackey.json'")
            print("Make sure that you are in a directory branch that contains this file")
            print("Or run :LackeyInit to create it in the current directory")
            return
        # check how much spacing we need for the task count to make it pretty:
        spacing = len(str(sum(len(v) for v in tasks.values())))
        messages = ["", ""]
        count = 1
        for (k, v) in tasks.items():
            messages += ["  "+k.upper(), "  -----------"]
            v_sorted = self._sort_by_date(v)
            for t in v_sorted:
                # add task to task_map:
                t["tag"] = k
                self.task_map[str(count)] = t
                time = t["timestamp"]
                strtime = dt.fromtimestamp(int(time)).strftime("%Y-%m-%d+%H:%M")
                file_loc = t["location"]["file"]
                line_loc  = t["location"]["line"]
                desc = t["description"]
                i = (" "*(spacing-len(str(count)))) + str(count)
                messages.append(f"  [{i}] {strtime} | line {line_loc} | {file_loc}")
                messages += [" "*(5+spacing)+desc, ""]
                count += 1
            messages.append("")
        print(self.task_map)
        self._create_win(messages)

    def lackey_close(self):
        """Closes the task popup and the border window."""
        try:
            vim.api.win_close(self.win_id, True)
            vim.api.win_close(self.border_id, True)
        except:
            print("Could not close Lackey.")

    def lackey_go(self, task_key):
        """Close the task popup, look up the task in a task dict and open file.

        Parameters
        ----------
        task_key : str
            Task number as listed in the popup. This number is used to
            look up the file and line number where the task was written.
        """
        # close Lackey
        self.lackey_close()
        loc = self.task_map[task_key]["location"]["file"]
        loc = os.path.abspath(os.path.join(self.lackey_path+loc))
        line = self.task_map[task_key]["location"]["line"]
        try:
            vim.command(f":e +{line} {loc}")
        except Exception as e:
            print(loc, "could not be opened:")
            print(e)

    def lackey_test(self):
        """Tests if Lackey instance is working.

        If it does, it prints out 'Lackey is ready!'
        """
        print("Lackey is ready!")

    def _extract_todo(self, string):
        """Extracts the task description from a line that Lackey recognizes.

        Parameters
        ----------
        string : str
            Single line comment containing a Lackey tag
            
        Returns
        -------
        str
            String without the comment tag and Lackey tag
        """
        pattern = "#*\s*("+tag_pattern+")\s*:*\s*"
        chunks = re.split(pattern, string)
        return chunks[-1]

    def write_todo(self, string):
        """Write task or note to `lackey` file.
        
        Parameters
        ----------
        string : str
            A parsed string. Use `extract_todo` to parse.
        """

    def lackey_init(self):
        """Initialize the current working directory as a Lackey root folder."""
        try:
            f = open("lackey.json")
            f.close()
            print("A lackey file already exists in this folder")
        except IOError:
            open("lackey", "a").close()
            print("Created lackey file")

    def lackey_collect(self):
        """Scans all of your files and collect tasks.
        
        Directories and files can be ignored by adding a `lackey_ignore` 
        variable to Vim's runtime configuration file (`.vimrc` or `init.vim`).

        For example:

        `let g:lackey_ignore='node_modules,__pycache__'`
        """
        try:
            ignore = vim.eval("g:lackey_ignore").strip()
            for i in ignore:
                if i in ignores:
                    continue
                ignores.append(i)
        except:
            pass
        cwd = os.getcwd()
        self.lackey_path = self._get_lackey_json_path(cwd)
        if not self.lackey_path:
            print("Could not find 'lackey.json'")
            print("Make sure that you are in a directory branch that contains this file")
            print("Or run :LackeyInit to create it in the current directory")
        else:
            print("Found lackey in", self.lackey_path)
            self._get_project_files()
            # for f in files:
                # # if file ext is not a recognized lang, skip
                # if not f.split(".")[-1] in list(languages.keys()):
                    # continue

                # # if file or folder name is configured to ignore, skip
                # if not f in ignores:
                    # content = open(f, "r")
                    # lines = content.readlines()
                    # for l in lines:
                        # # print(l)
                        # match = re.match(r"#\s*("+tag_pattern+")\s*", l)
                        # if match:
                            # pass
                            # # print(l)
                    # content.close()

