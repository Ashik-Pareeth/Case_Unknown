"""
Treasure & Evidence Management System for Case Unknown.

Tracks puzzle unlock states, recovered case evidence items, and case completion progress.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from src.puzzles import NumberLockPuzzle, TileAlignPuzzle, BasePuzzle


@dataclass
class TreasureItem:
    item_id: str
    room_id: str
    name: str
    puzzle_type: str  # "number_lock" or "tile_align"
    puzzle_title: str
    target_solution: list
    hint: str
    reward_name: str
    reward_description: str
    is_unlocked: bool = False


class TreasureManager:
    """Central singleton managing all treasure points and case evidence across rooms."""

    def __init__(self):
        self.treasures: Dict[str, TreasureItem] = {}
        self._init_precinct_treasures()

    def _init_precinct_treasures(self):
        """Initializes the 5 thematic treasures located in each precinct room."""
        # 1. Precinct Detective Office - Brass Wall Safe
        self.treasures["office_safe"] = TreasureItem(
            item_id="office_safe",
            room_id="office",
            name="Precinct Commander's Wall Safe",
            puzzle_type="number_lock",
            puzzle_title="Brass Wall Safe — 3-Digit Tumbler",
            target_solution=[1, 9, 2],
            hint="Precinct founding calendar date: 1928. Try the first 3 digits.",
            reward_name="Gold Master Precinct Keycard",
            reward_description="A tarnished brass keycard that grants unrestricted access to confidential archives.",
        )

        # 2. Forensic Evidence Archive - High-Security Vault Box
        self.treasures["archive_vault"] = TreasureItem(
            item_id="archive_vault",
            room_id="archive",
            name="Archival Evidence Vault Strongbox",
            puzzle_type="tile_align",
            puzzle_title="Forensic Compass Seal — 4-Dial Alignment",
            target_solution=[0, 90, 180, 270],  # North, East, South, West
            hint="Forensic index card: 'Align all 4 dials clockwise to cardinal points (N - E - S - W)'.",
            reward_name="Classified Dossier #77",
            reward_description="Unredacted surveillance logs linking city hall kickbacks to the dockside syndicate.",
        )

        # 3. Cold Storage & Morgue - Cryo Specimen Locker
        self.treasures["morgue_locker"] = TreasureItem(
            item_id="morgue_locker",
            room_id="morgue",
            name="Cryo Specimen Storage Locker",
            puzzle_type="number_lock",
            puzzle_title="Specimen Cold Locker — 4-Digit Combination",
            target_solution=[8, 4, 1, 6],
            hint="Coroner's autopsy ledger notes: 'Chemical batch formula 8-4-1-6 synthesized for specimen freezing.'",
            reward_name="Rare Toxicology Vial",
            reward_description="A chilled glass ampoule containing the lethal untraceable sedative used in the crime.",
        )

        # 4. Detention Lockup - Contraband Stash Box
        self.treasures["lockup_stash"] = TreasureItem(
            item_id="lockup_stash",
            room_id="lockup",
            name="Smuggled Contraband Strongbox",
            puzzle_type="tile_align",
            puzzle_title="Contraband Lock Pins — Tumbler Alignment",
            target_solution=[180, 0, 180, 0],  # Alternating South, North, South, North
            hint="Scratched into the cell wall plaster: 'Poles alternate like a heartbeat: Down, Up, Down, Up'.",
            reward_name="Syndicate Diamond Locket",
            reward_description="An engraved antique platinum locket containing microdots of secret bank accounts.",
        )

        # 5. Interrogation Chamber - Tape Recorder Case Box
        self.treasures["interrogation_box"] = TreasureItem(
            item_id="interrogation_box",
            room_id="interrogation",
            name="One-Way Mirror Lockbox",
            puzzle_type="number_lock",
            puzzle_title="Acoustic Wiretap Case — 3-Digit Tumbler",
            target_solution=[3, 5, 9],
            hint="Stamped on the tape reel box: 'Confession statement recorded at 03:59 AM'.",
            reward_name="Original Witness Confession Tape",
            reward_description="The master reel recording capturing the suspect naming the precinct mole.",
        )

    def get_treasure(self, item_id: str) -> Optional[TreasureItem]:
        return self.treasures.get(item_id)

    def is_unlocked(self, item_id: str) -> bool:
        treasure = self.get_treasure(item_id)
        return treasure.is_unlocked if treasure else False

    def unlock_treasure(self, item_id: str) -> bool:
        treasure = self.get_treasure(item_id)
        if treasure:
            treasure.is_unlocked = True
            return True
        return False

    def create_puzzle(self, item_id: str) -> Optional[BasePuzzle]:
        """Creates an instance of the puzzle mini-game for this treasure."""
        item = self.get_treasure(item_id)
        if not item:
            return None

        if item.puzzle_type == "number_lock":
            return NumberLockPuzzle(
                title=item.puzzle_title,
                target_code=item.target_solution,
                hint=item.hint,
                reward_name=item.reward_name,
            )
        elif item.puzzle_type == "tile_align":
            return TileAlignPuzzle(
                title=item.puzzle_title,
                target_angles=item.target_solution,
                hint=item.hint,
                reward_name=item.reward_name,
            )
        return None

    def get_all_unlocked(self) -> List[TreasureItem]:
        return [t for t in self.treasures.values() if t.is_unlocked]

    def get_progress_percentage(self) -> int:
        if not self.treasures:
            return 0
        unlocked = sum(1 for t in self.treasures.values() if t.is_unlocked)
        return int((unlocked / len(self.treasures)) * 100)
