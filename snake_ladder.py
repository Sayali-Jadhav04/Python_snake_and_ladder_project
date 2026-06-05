"""
🎲 Snake and Ladder Game
========================
A 2-player terminal Snake & Ladder game built in Python.
Concepts used: functions, dictionaries, loops, random, input/output
"""

import random
import time

# ─────────────────────────────────────────────
#  COLORS (ANSI escape codes)
# ─────────────────────────────────────────────
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    CYAN    = "\033[96m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"
    GREY    = "\033[90m"
    WHITE   = "\033[97m"

def c(text, color):
    return f"{color}{text}{Color.RESET}"

# ─────────────────────────────────────────────
#  SNAKES & LADDERS  (key=head/top, value=tail/bottom destination)
# ─────────────────────────────────────────────
SNAKES = {
    99: 7,
    91: 28,
    74: 53,
    64: 45,
    54: 17,
    43: 18,
    27: 5,
}

LADDERS = {
    4:  25,
    13: 46,
    33: 49,
    42: 63,
    50: 69,
    62: 81,
    70: 91,
}

PLAYER_ICONS = {
    "Player 1": c("🔴", Color.RED),
    "Player 2": c("🔵", Color.BLUE),
}

# ─────────────────────────────────────────────
#  BOARD DRAWING
# ─────────────────────────────────────────────
def draw_board(positions: dict):
    """Draw a 10x10 board with player positions, snakes & ladders marked."""
    print()
    # Build a lookup: cell number -> what to show
    cell_display = {}
    for cell in SNAKES:
        cell_display[cell] = c("🐍", Color.RED)
    for cell in LADDERS:
        cell_display[cell] = c("🪜", Color.GREEN)

    # Player positions override
    for player, pos in positions.items():
        icon = "🔴" if player == "Player 1" else "🔵"
        if pos in cell_display:
            cell_display[pos] = icon + cell_display[pos][-2:]  # stack
        else:
            cell_display[pos] = "🔴" if player == "Player 1" else "🔵"

    # Check if both players on same cell
    vals = list(positions.values())
    if len(vals) == 2 and vals[0] == vals[1] and vals[0] != 0:
        cell_display[vals[0]] = "🟣"  # both on same cell

    print(c("  ┌" + "────┬" * 9 + "────┐", Color.GREY))

    for row in range(9, -1, -1):  # row 9 (top) to row 0 (bottom)
        # Number the cells: even rows go left→right, odd rows go right→left
        start = row * 10 + 1
        cells = list(range(start, start + 10))
        if row % 2 == 1:        # odd rows are right-to-left on the board
            cells = cells[::-1]

        line = c("  │", Color.GREY)
        for cell in cells:
            icon = cell_display.get(cell, "  ")
            num  = str(cell).rjust(2)
            if icon in ("  ",):
                line += f" {c(num, Color.GREY)} {c('│', Color.GREY)}"
            else:
                line += f"{icon}{c('│', Color.GREY)}"
        print(line)

        if row > 0:
            print(c("  ├" + "────┼" * 9 + "────┤", Color.GREY))

    print(c("  └" + "────┴" * 9 + "────┘", Color.GREY))
    print()

    # Legend
    print(f"  {c('🐍 Snake', Color.RED)}  {c('🪜 Ladder', Color.GREEN)}  "
          f"{c('🔴 Player 1', Color.RED)}  {c('🔵 Player 2', Color.BLUE)}")
    print()

# ─────────────────────────────────────────────
#  DICE
# ─────────────────────────────────────────────
def roll_dice() -> int:
    """Simulate rolling a 6-sided dice."""
    return random.randint(1, 6)

def show_dice(value: int):
    faces = {
        1: ["┌─────┐", "│     │", "│  ●  │", "│     │", "└─────┘"],
        2: ["┌─────┐", "│ ●   │", "│     │", "│   ● │", "└─────┘"],
        3: ["┌─────┐", "│ ●   │", "│  ●  │", "│   ● │", "└─────┘"],
        4: ["┌─────┐", "│ ● ● │", "│     │", "│ ● ● │", "└─────┘"],
        5: ["┌─────┐", "│ ● ● │", "│  ●  │", "│ ● ● │", "└─────┘"],
        6: ["┌─────┐", "│ ● ● │", "│ ● ● │", "│ ● ● │", "└─────┘"],
    }
    for line in faces[value]:
        print(f"    {c(line, Color.YELLOW)}")

# ─────────────────────────────────────────────
#  MOVE LOGIC
# ─────────────────────────────────────────────
def move_player(current_pos: int, dice: int) -> tuple[int, str]:
    """
    Calculate new position after rolling dice.
    Returns (new_position, event_message)
    """
    new_pos = current_pos + dice

    # Can't go beyond 100
    if new_pos > 100:
        return current_pos, c(f"  ⚠️  Needs exact roll to reach 100. Stay at {current_pos}.", Color.GREY)

    # Exact 100 = win
    if new_pos == 100:
        return 100, c("  🎉 REACHED 100!", Color.GREEN)

    # Check snake
    if new_pos in SNAKES:
        tail = SNAKES[new_pos]
        msg = (f"  🐍 {c('SNAKE!', Color.RED)} Slid down from "
               f"{c(new_pos, Color.BOLD)} → {c(tail, Color.RED)}")
        return tail, msg

    # Check ladder
    if new_pos in LADDERS:
        top = LADDERS[new_pos]
        msg = (f"  🪜 {c('LADDER!', Color.GREEN)} Climbed up from "
               f"{c(new_pos, Color.BOLD)} → {c(top, Color.GREEN)}")
        return top, msg

    return new_pos, f"  ➡️  Moved to {c(new_pos, Color.CYAN)}"

# ─────────────────────────────────────────────
#  SCORE TRACKER
# ─────────────────────────────────────────────
def show_scoreboard(stats: dict):
    print(f"\n  {c('SCOREBOARD', Color.BOLD)}")
    print(f"  {'─'*30}")
    for player, data in stats.items():
        icon = "🔴" if player == "Player 1" else "🔵"
        print(f"  {icon} {c(player, Color.BOLD):<20} "
              f"Rolls: {c(data['rolls'], Color.YELLOW)}  "
              f"Snakes: {c(data['snakes'], Color.RED)}  "
              f"Ladders: {c(data['ladders'], Color.GREEN)}")
    print()

# ─────────────────────────────────────────────
#  MAIN GAME LOOP
# ─────────────────────────────────────────────
def get_player_names() -> tuple[str, str]:
    print(c("\n  Enter player names (or press Enter for defaults):\n", Color.CYAN))
    p1 = input(f"  🔴 Player 1 name [Player 1]: ").strip() or "Player 1"
    p2 = input(f"  🔵 Player 2 name [Player 2]: ").strip() or "Player 2"
    return p1, p2

def main():
    # ── Welcome Screen ──
    print("\n" + c("=" * 55, Color.YELLOW))
    print(c("       🎲  SNAKE AND LADDER GAME  🎲", Color.BOLD))
    print(c("=" * 55, Color.YELLOW))
    print(c("  2-Player  |  First to reach 100 wins!", Color.GREY))
    print(c("=" * 55 + "\n", Color.YELLOW))

    # ── Snakes & Ladders info ──
    print(c("  🐍 SNAKES (slide down):", Color.RED))
    for head, tail in SNAKES.items():
        print(f"     {head} → {tail}", end="   ")
    print()
    print(c("\n  🪜 LADDERS (climb up):", Color.GREEN))
    for bottom, top in LADDERS.items():
        print(f"     {bottom} → {top}", end="   ")
    print("\n")

    p1_name, p2_name = get_player_names()
    players = [p1_name, p2_name]

    # positions start at 0 (off the board)
    positions = {p1_name: 0, p2_name: 0}

    # Stats tracking
    stats = {
        p1_name: {"rolls": 0, "snakes": 0, "ladders": 0},
        p2_name: {"rolls": 0, "snakes": 0, "ladders": 0},
    }

    turn = 0  # alternates between 0 and 1

    while True:
        current_player = players[turn]
        icon = "🔴" if turn == 0 else "🔵"
        color = Color.RED if turn == 0 else Color.BLUE

        # ── Show Board ──
        draw_board(positions)
        show_scoreboard(stats)

        print(c(f"  {icon}  {current_player}'s turn", color) +
              f"  (currently at {c(positions[current_player], Color.BOLD)})")
        input(c("  Press ENTER to roll the dice... 🎲 ", Color.YELLOW))

        # ── Roll ──
        dice = roll_dice()
        stats[current_player]["rolls"] += 1

        print(f"\n  {current_player} rolled a {c(dice, Color.BOLD)}!")
        show_dice(dice)
        time.sleep(0.5)

        # ── Move ──
        old_pos = positions[current_player]
        new_pos, message = move_player(old_pos, dice)
        positions[current_player] = new_pos

        # Track snakes and ladders
        if "SNAKE" in message:
            stats[current_player]["snakes"] += 1
        if "LADDER" in message:
            stats[current_player]["ladders"] += 1

        print(message)
        time.sleep(0.8)

        # ── Check Win ──
        if new_pos == 100:
            draw_board(positions)
            print(c("=" * 55, Color.GREEN))
            print(c(f"  🏆  {current_player} WINS THE GAME!  🏆", Color.BOLD))
            print(c("=" * 55, Color.GREEN))
            show_scoreboard(stats)
            break

        # ── Next turn ──
        turn = 1 - turn  # toggles between 0 and 1
        print()

    # ── Play Again ──
    again = input(c("\n  Play again? [y/N]: ", Color.CYAN)).strip().lower()
    if again == "y":
        main()
    else:
        print(c("\n  Thanks for playing! Goodbye 👋\n", Color.CYAN))

# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
