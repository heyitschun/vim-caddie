let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import lackey
l = lackey.Lackey()
EOF

function! LackeyTest()
  python3 l.lackey_test()
endfunction
command! -nargs=0 LackeyTest call LackeyTest()

function! LackeyInit()
  python3 l.lackey_init()
endfunction
command! -nargs=0 LackeyInit call LackeyInit()

function! LackeyCollect()
  python3 l.lackey_collect()
endfunction
command! -nargs=0 LackeyCollect call LackeyCollect()

function! LackeyShow()
  python3 l.lackey_show()
endfunction
command! -nargs=0 LackeyShow call LackeyShow()

function! LackeyClose()
  python3 l.lackey_close()
endfunction

function! LackeyGo(task_key)
  python3 l.lackey_go(vim.eval("a:task_key"))
endfunction
command! -nargs=1 LackeyGo call LackeyGo(<f-args>)

