import sys

sys.dont_write_bytecode = True

from package import base
from package.core.info import users, miner, balance
from package.core.earn import process_claim_daily_task, process_claim_social_tasks
from package.core.tapper import process_tap
from package.core.cards import process_buy_card

import time
import brotli


class HashCats:
    def __init__(self):
        # Get file directory
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")

        # Initialize line
        self.line = base.create_line(length=50)

        # Initialize banner
        self.banner = base.create_banner(game_name="HashCats")

        # Get config
        self.auto_claim_daily_reward = base.get_config(
            config_file=self.config_file, config_name="auto-claim-daily-reward"
        )

        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_tap = base.get_config(
            config_file=self.config_file, config_name="auto-tap"
        )

        self.auto_buy_card = base.get_config(
            config_file=self.config_file, config_name="auto-buy-card"
        )

    def main(self):
        while True:
            base.clear_terminal()
            print(self.banner)
            data = open(self.data_file, "r").read().splitlines()
            num_acc = len(data)
            base.log(self.line)
            base.log(f"{base.green}Numer of accounts: {base.white}{num_acc}")

            for no, token in enumerate(data):
                base.log(self.line)
                base.log(f"{base.green}Account number: {base.white}{no+1}/{num_acc}")

                try:
                    # Get user info
                    mined_coins = users(token=token)
                    name, level, tap, energy_per_tap, energy = miner(token=token)
                    current_balance = balance(token=token)

                    base.log(
                        f"{base.green}Miner: {base.white}{name} - {base.green}Level: {base.white}{level} - {base.green}Tap: {base.white}{tap} - {base.green}Energy per Tap: {base.white}{energy_per_tap} - {base.green}Energy: {base.white}{energy}"
                    )
                    base.log(f"{base.green}Mined Coins: {base.white}{mined_coins}")
                    base.log(f"{base.green}Balance: {base.white}{current_balance}")

                    # Claim daily reward
                    if self.auto_claim_daily_reward:
                        base.log(
                            f"{base.yellow}Auto Claim Daily Reward: {base.green}ON"
                        )
                        process_claim_daily_task(token=token)
                    else:
                        base.log(f"{base.yellow}Auto Claim Daily Reward: {base.red}OFF")

                    # Do task
                    if self.auto_do_task:
                        base.log(f"{base.yellow}Auto Do Task: {base.green}ON")
                        process_claim_social_tasks(token=token)
                    else:
                        base.log(f"{base.yellow}Auto Do Task: {base.red}OFF")

                    # Tapping
                    if self.auto_tap:
                        base.log(f"{base.yellow}Auto Tap: {base.green}ON")
                        process_tap(token=token)
                    else:
                        base.log(f"{base.yellow}Auto Tap: {base.red}OFF")

                    # Buy cards
                    if self.auto_buy_card:
                        base.log(f"{base.yellow}Auto Buy Card: {base.green}ON")
                        process_buy_card(token=token)
                    else:
                        base.log(f"{base.yellow}Auto Buy Card: {base.red}OFF")

                except Exception as e:
                    base.log(f"{base.red}Error: {base.white}{e}")

            break


if __name__ == "__main__":
    try:
        hashcats = HashCats()
        hashcats.main()
    except KeyboardInterrupt:
        sys.exit()
