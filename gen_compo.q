#!/root/q/l64/q
pwds: "/" vs {value[.z.s]}[][6];
script_path: "/" sv _[pwds; count[pwds] - 1];
system("l ", script_path, "/../scripts/utils.q");
args: .Q.def[(1#`dt)!1#.z.d].Q.opt .z.x;
d: args`dt;
{ show system(script_path, "/dump_compo.py ", date_to_str[x], " csi300") } each get_bday_range[d - 10; d];
{ show system(script_path, "/dump_compo.py ", date_to_str[x], " csi500") } each get_bday_range[d - 10; d];
exit 0;
