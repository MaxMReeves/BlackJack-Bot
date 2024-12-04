Blackjack Bot with Martingale Strategy

A Python-powered Blackjack bot designed to automate gameplay and utilize the Martingale Strategy to maximize profits. This project simulates betting patterns and decision-making processes in Blackjack, aiming to assist users in profiting over time.
Features

    Simulates Blackjack games using programmed rules.
    Implements the Martingale Strategy:
        Increases the bet size after every loss to recover previous losses and make a profit equal to the initial bet.
        Resets the bet to the base amount after a win.
    Tracks gameplay statistics, such as:
        Total wins, losses, and draws.
        Total profit/loss.
        Number of games played.
    Configurable settings for:
        Starting balance.
        Base bet amount.
        Maximum allowable bet (to prevent excessive loss).

How It Works

    The bot starts with an initial balance and a base bet.
    It plays Blackjack rounds:
        If the bot wins, the bet resets to the base amount.
        If the bot loses, the bet doubles (per the Martingale Strategy).
    The bot stops if the balance falls below the base bet or exceeds a predefined profit target.
    Game results are logged for analysis.
