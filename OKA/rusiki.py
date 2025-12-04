import threading
import random
import time
from typing import List, Tuple

PRICE_PER_UNIT = 50          
ATTEMPTS_PER_RUNNER = 10      
RUNNER_COUNTS = [1, 3, 5, 8]  
N_WAREHOUSES = 4              
class Warehouse:
    def __init__(self, name: str, meds: int):
        self.name = name
        self.meds = meds
        self.lock = threading.Lock()

    def steal(self, amount: int) -> Tuple[int, str]:
        p = random.random()

        if p < 0.05:
            return 0, "caught"

        if p < 0.30:
            if self.meds <= 0:
                return 0, "empty"
            stolen = min(self.meds, random.randint(1, max(1, amount - 1)))
            self.meds -= stolen
            return stolen, "partial"

        if self.meds <= 0:
            return 0, "empty"
        stolen = min(self.meds, amount)
        self.meds -= stolen
        return stolen, "success"

class Runner(threading.Thread):
    def __init__(self, runner_name: str, warehouses: List[Warehouse]):
        super().__init__()
        self.runner_name = runner_name
        self.warehouses = warehouses
        self.earnings = 0
        self.attempts_done = 0
        self.attempts_total = ATTEMPTS_PER_RUNNER

    def run(self):
        for _ in range(self.attempts_total):
            wh = random.choice(self.warehouses)
            amount = random.randint(10, 30)

            with wh.lock:
                stolen, _ = wh.steal(amount)

            self.earnings += stolen * PRICE_PER_UNIT
            self.attempts_done += 1

            time.sleep(random.uniform(0.08, 0.25))

    def progress(self):
        return self.attempts_done / self.attempts_total

def make_warehouses(n: int):
    return [Warehouse(f"WH-{i+1}", random.randint(100, 300)) for i in range(n)]


def show_progress(runners):
    lines = []
    for r in runners:
        bar_len = 20
        filled = int(r.progress() * bar_len)
        bar = "[" + "#" * filled + "-" * (bar_len - filled) + "]"
        lines.append(f"{r.runner_name:10} {bar} {r.attempts_done}/{r.attempts_total}")
    print("\033c", end="")
    print("Simulation progress:\n" + "\n".join(lines))


def run_simulation(num_runners: int):
    warehouses = make_warehouses(N_WAREHOUSES)
    runners = [Runner(f"Runner-{i+1}", warehouses) for i in range(num_runners)]

    for r in runners:
        r.start()

    while any(r.is_alive() for r in runners):
        show_progress(runners)
        time.sleep(0.15)

    show_progress(runners)

    total = sum(r.earnings for r in runners)
    print("\nRESULTS:")
    print(f"Total earned: {total} UAH")

    print("\nWarehouse stocks after robbery:")
    for w in warehouses:
        print(f"{w.name}: {w.meds} meds left")

    print("\nRunner earnings:")
    for r in runners:
        print(f"{r.runner_name}: {r.earnings} UAH")

    print("\n" + "=" * 45)
    return total

if name == "__main__":
    print("Starting simulations...\n")
    for count in RUNNER_COUNTS:
        print(f"\n=== Simulation with {count} runners ===")
        run_simulation(count)
        time.sleep(1)