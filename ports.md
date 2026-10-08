Port Assignments
-----

Port assignment convention (`port = yycnn`):
- `yy` = last two digits of the competition year (18 for SunshineCTF 2018)
- `c`  = category: 0 pwn, 1 reversing, 2 scripting, 3 web, 4 crypto, 5 misc
        (also forensics/other), 6 speedrun, 7 pegasus
- `nn` = challenge index within the category (ordered by point value then name)

Raw TCP challenges: `nc ctf.hackucf.org <port>`.
HTTP(S) web challenges are served at `<slug>.ctf.hackucf.org` and bound to
`127.0.0.1:<port>` behind nginx (see the `nginx/` fragments).

| Challenge Name | Category | Author | Directory | Host | Port | Connection |
|----------------|----------|--------|-----------|------|-----:|------------|
| Hacker Name | Pwn | lil_marv | Pwn/hacker-name | ctf.hackucf.org | 18001 | `nc ctf.hackucf.org 18001` |
| Log Search | Pwn | kcolley | Pwn/Log-Search | ctf.hackucf.org | 18002 | `nc ctf.hackucf.org 18002` |
| Rot13 | Pwn | kcolley | Pwn/Rot13 | ctf.hackucf.org | 18003 | `nc ctf.hackucf.org 18003` |
| Hexalicious | Pwn | kcolley | Pwn/Hexalicious | ctf.hackucf.org | 18004 | `nc ctf.hackucf.org 18004` |
| UAF | Pwn | kcolley | Pwn/UAF | ctf.hackucf.org | 18005 | `nc ctf.hackucf.org 18005` |
| BookWriter | Pwn | kcolley | Pwn/BookWriter | ctf.hackucf.org | 18006 | `nc ctf.hackucf.org 18006` |
| Missing Bytes | Scripting | vraelvrangr | Scripting/missing-bytes | ctf.hackucf.org | 18201 | `nc ctf.hackucf.org 18201` |
| Workshop Helper | Scripting | vraelvrangr | Scripting/WorkshopHelper | workshophelper.ctf.hackucf.org | 18202 | https://workshophelper.ctf.hackucf.org |
| Evaluation | Web | leviathan | Web/Evaluation | evaluation.ctf.hackucf.org | 18301 | https://evaluation.ctf.hackucf.org |
| Marceau | Web | charlton | Web/Marceau | marceau.ctf.hackucf.org | 18302 | https://marceau.ctf.hackucf.org |
| SearchBox | Web | leviathan | Web/SearchBox | searchbox.ctf.hackucf.org | 18303 | https://searchbox.ctf.hackucf.org |
| Home Sweet Home | Web | leviathan | Web/HomeSweetHome | homesweethome.ctf.hackucf.org | 18304 | https://homesweethome.ctf.hackucf.org |
