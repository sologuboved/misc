def generate_tab(project, script):
    script = script.rsplit('.')[0]
    print("""
sudo vim {project}.conf

[program:{project}]
user=sologuboved
command=/home/sologuboved/venv_py3/bin/python -u /home/sologuboved/scripts/{project}/{script}.py
stderr_logfile = /home/sologuboved/scripts/{project}/{script}.log
    """.format(project=project, script=script))


if __name__ == '__main__':
    for proj in ('instaurl', 'odol', 'pagecount', 'pequod', 'stubb', 'time_calc'):
        generate_tab(proj, 'bot.py')

    # sudo supervisorctl update
