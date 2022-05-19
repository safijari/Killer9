import subprocess
import json


class Plugin:
    # A normal method. It can be called from JavaScript using call_plugin_function("method_1", argument1, argument2)
    async def kill(self, pid):
        return subprocess.Popen(
            "kill " + str(pid), stdout=subprocess.PIPE, shell=True
        ).wait()

    async def get_procs(self):
        proc = subprocess.Popen(
            """ps a -o pid,comm=,tty""",
            stdout=subprocess.PIPE,
            stderr=None,
            shell=True,
        )
        proc.wait()
        resstr = proc.communicate()[0].decode("ascii")

        with open("/tmp/out", "w") as f:
            f.write(resstr)

        pids_and_names = []
        ignore_phrases = [
            "gamescope",
            "Xwayland",
            "power-button",
            "mangoapp",
            "bash",
            "steam",
            "reaper",
        ]
        for line in resstr.split("\n")[1:]:
            include = True
            for phrase in ignore_phrases:
                if phrase in line:
                    include = False
            if not include:
                continue
            line = line.strip()
            if not line:
                continue
            elements = line.split(" ")
            pids_and_names.append(elements[:2])

        return json.dumps(pids_and_names)

    async def _main(self):
        pass
