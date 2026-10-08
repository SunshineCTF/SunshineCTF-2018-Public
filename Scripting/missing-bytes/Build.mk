# docker-compose TCP challenge; `pwnmake check` starts it, runs the solver, and
# tears it down.
$(call ctf_check_tcp,$(DIR),18201,python3 solution.py)
