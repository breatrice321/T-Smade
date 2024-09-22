import subprocess
import time
import os

def attack():
    state = True

    while state:
        try:
            # Set the same environment variables.
            env = os.environ.copy()

            time_init = time.time()

            print("attack begin ...")

            # result = subprocess.run(
            #     './spectrev1',
            #     timeout=601,
            #     capture_output=True,
            #     text=True,
            #     cwd='./attack_code/spectre',
            #     env=env
            # )

            # result = subprocess.run(
            #     './evasive-spectre',
            #     timeout=601,
            #     capture_output=True,
            #     text=True,
            #     cwd='./attack_code/evasive_spectre_nop',
            #     env=env
            # )

            result = subprocess.run(
                './expand-spectre',
                timeout=601,
                capture_output=True,
                text=True,
                cwd='./attack_code/evasive_spectre_memory',
                env=env
            )


        except subprocess.TimeoutExpired:
            print("attack execution timed out")

        if time.time() - time_init > 599:
            state = False
            print("Execution completed")

if __name__ == "__main__":
    attack()