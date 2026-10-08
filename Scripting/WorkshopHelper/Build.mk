# docker-compose web challenge; `pwnmake check` starts it, runs the solver, and
# tears it down.
$(call ctf_check_web,$(DIR),18202,workshophelper.ctf.hackucf.org,python3 solution.py)
