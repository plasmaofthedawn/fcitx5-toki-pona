# hiiii

fcitx5 table based inputs for toki pona

adds a few dozen sitelen Kansi inputs (one for each column in https://sona.pona.la/wiki/sitelen_Kansi, as well as one that combines all of them)

as well as one for the UCSUR codepage, one for the emoji one (nasin pi sitelen jelo) and one for the dingbats one (called toki pona script)

emoji and UCSUR data was adapted from [ajemi](https://github.com/dec32/ajemi/tree/master)

there's also one for [sitelen seli kiwen](https://www.kreativekorp.com/software/fonts/sitelenselikiwen/). it has all the glyphs and varieties of the glyphs but not the names (yet (?))

# building

all the information for the tables are in that data text filee

running the combine.py script will sort it out into the dictionary and configuration files

# installation

run the `combine.py` script, then copy all the files under the `confs` directory into `~/.local/share/fcitx5/inputmethod/` and all the files in the `table` dir into `~/.local/share/fcitx5/table/` dir

additionally you can download this on the aur [here](https://aur.archlinux.org/packages/fcitx5-toki-pona-git)
