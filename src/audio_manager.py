"""
Audio and sound effects management system for Case Unknown.

Provides procedural sound waveform synthesis in pure Python with support for
drop-in WAV/OGG asset overrides, graceful headless fallback, and global volume/mute controls.
"""

from __future__ import annotations

import io
import math
import os
import random
import struct
import wave
import pygame


# Directories for audio and sound assets
SOUND_ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "sounds"
)
AUDIO_ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "audio"
)

# Background menu music track path
MENU_MUSIC_PATH = os.path.join(
    AUDIO_ASSETS_DIR,
    "Rain_Against_the_Glass.mp3",
)


class Synthesizer:
    """Procedural waveform synthesizer generating standard 16-bit PCM WAV buffers."""

    SAMPLE_RATE = 44100

    @classmethod
    def _create_wav_sound(cls, duration: float, generator_fn) -> pygame.mixer.Sound | None:
        """Helper to compile a sample generator into a pygame.mixer.Sound."""
        buf = io.BytesIO()
        try:
            with wave.open(buf, "wb") as wf:
                wf.setnchannels(2)
                wf.setsampwidth(2)
                wf.setframerate(cls.SAMPLE_RATE)
                total_frames = int(cls.SAMPLE_RATE * duration)
                for i in range(total_frames):
                    t = float(i) / cls.SAMPLE_RATE
                    val = generator_fn(t, duration, i)
                    val = max(-1.0, min(1.0, val))
                    sample = int(val * 32767.0 * 0.75)
                    data = struct.pack("<hh", sample, sample)
                    wf.writeframesraw(data)
            buf.seek(0)
            return pygame.mixer.Sound(buf)
        except Exception:
            return None

    @classmethod
    def synth_puzzle_click(cls) -> pygame.mixer.Sound | None:
        """Crisp mechanical switch / dial click (0.025s)."""
        return cls._create_wav_sound(
            0.025,
            lambda t, d, i: (
                math.sin(2.0 * math.pi * 1600.0 * t) + ((i % 7) - 3) / 6.0
            ) * max(0.0, 1.0 - t / d),
        )

    @classmethod
    def synth_puzzle_digit(cls) -> pygame.mixer.Sound | None:
        """Keypad electronic button tone (0.04s)."""
        return cls._create_wav_sound(
            0.04,
            lambda t, d, i: (
                math.sin(2.0 * math.pi * 941.0 * t) * 0.6
                + math.sin(2.0 * math.pi * 1336.0 * t) * 0.4
            ) * max(0.0, math.exp(-t * 22.0)),
        )

    @classmethod
    def synth_puzzle_solved(cls) -> pygame.mixer.Sound | None:
        """Ascending chime triad indicating puzzle solved / safe unlocked (0.45s)."""
        return cls._create_wav_sound(
            0.45,
            lambda t, d, i: (
                (0.4 * math.sin(2.0 * math.pi * 523.25 * t) if t < 0.4 else 0.0)
                + (0.4 * math.sin(2.0 * math.pi * 659.25 * max(0.0, t - 0.08)) if t >= 0.08 else 0.0)
                + (0.5 * math.sin(2.0 * math.pi * 783.99 * max(0.0, t - 0.16)) if t >= 0.16 else 0.0)
            ) * max(0.0, 1.0 - t / d),
        )

    @classmethod
    def synth_puzzle_failed(cls) -> pygame.mixer.Sound | None:
        """Low double-rejection buzzer for invalid codes (0.18s)."""
        return cls._create_wav_sound(
            0.18,
            lambda t, d, i: (
                (1.0 if (int(t * 140.0) % 2 == 0) else -1.0) * 0.4
                + math.sin(2.0 * math.pi * 110.0 * t) * 0.5
            ) * max(0.0, 1.0 - t / d),
        )

    @classmethod
    def synth_inspect_open(cls) -> pygame.mixer.Sound | None:
        """Gentle document / dossier paper rustle on opening (0.08s)."""
        return cls._create_wav_sound(
            0.08,
            lambda t, d, i: (
                ((i % 11) - 5) / 5.0 * 0.4
                + math.sin(2.0 * math.pi * 600.0 * t) * 0.2
            ) * max(0.0, math.sin(math.pi * t / d)),
        )

    @classmethod
    def synth_inspect_close(cls) -> pygame.mixer.Sound | None:
        """Soft folder closure sound (0.06s)."""
        return cls._create_wav_sound(
            0.06,
            lambda t, d, i: (
                ((i % 13) - 6) / 6.0 * 0.35
                + math.sin(2.0 * math.pi * 320.0 * t) * 0.35
            ) * max(0.0, 1.0 - t / d),
        )

    @classmethod
    def synth_evidence_reveal(cls) -> pygame.mixer.Sound | None:
        """Dramatic noir minor chord discovery sting (0.70s)."""
        return cls._create_wav_sound(
            0.70,
            lambda t, d, i: (
                math.sin(2.0 * math.pi * 293.66 * t) * 0.45  # D4
                + math.sin(2.0 * math.pi * 349.23 * t) * 0.35  # F4
                + math.sin(2.0 * math.pi * 440.0 * t) * 0.35   # A4
                + math.sin(2.0 * math.pi * 587.33 * t) * 0.15  # D5 overtone
            ) * max(0.0, math.exp(-t * 3.8)),
        )

    @classmethod
    def synth_guard_alert(cls) -> pygame.mixer.Sound | None:
        """Sharp dissonant tritone sting when guard is alerted (0.28s)."""
        return cls._create_wav_sound(
            0.28,
            lambda t, d, i: (
                math.sin(2.0 * math.pi * 880.0 * t) * 0.5
                + math.sin(2.0 * math.pi * 932.33 * t) * 0.5
                + math.sin(2.0 * math.pi * 1244.5 * t) * 0.25
            ) * max(0.0, math.exp(-t * 8.5)),
        )

    @classmethod
    def synth_game_over(cls) -> pygame.mixer.Sound | None:
        """Deep ominous impact chord upon apprehension (1.20s)."""
        return cls._create_wav_sound(
            1.20,
            lambda t, d, i: (
                math.sin(2.0 * math.pi * 65.41 * t) * 0.5   # C2
                + math.sin(2.0 * math.pi * 77.78 * t) * 0.4  # Eb2
                + math.sin(2.0 * math.pi * 98.00 * t) * 0.3  # G2
                + math.sin(2.0 * math.pi * 130.81 * t) * 0.2 # C3
            ) * max(0.0, math.exp(-t * 2.2)),
        )

    @classmethod
    def synth_door_open(cls) -> pygame.mixer.Sound | None:
        """Heavy timber door unlatch and swing (0.20s)."""
        return cls._create_wav_sound(
            0.20,
            lambda t, d, i: (
                math.sin(2.0 * math.pi * 180.0 * t) * 0.4
                + math.sin(2.0 * math.pi * (140.0 - 50.0 * (t / d)) * t) * 0.4
                + ((i % 9) - 4) / 4.0 * 0.15
            ) * max(0.0, 1.0 - t / d),
        )

    @classmethod
    def synth_door_locked(cls) -> pygame.mixer.Sound | None:
        """Iron door handle rattle indicating locked passage (0.12s)."""
        return cls._create_wav_sound(
            0.12,
            lambda t, d, i: (
                math.sin(2.0 * math.pi * 95.0 * t) * 0.5
                + math.sin(2.0 * math.pi * 220.0 * t) * 0.4
                + ((i % 7) - 3) / 3.0 * 0.2
            ) * max(0.0, 1.0 - t / d),
        )

    @classmethod
    def synth_door_unlocked(cls) -> pygame.mixer.Sound | None:
        """Relay click and lock slide release (0.18s)."""
        return cls._create_wav_sound(
            0.18,
            lambda t, d, i: (
                (math.sin(2.0 * math.pi * 1400.0 * t) * 0.5 if t < 0.04 else 0.0)
                + (math.sin(2.0 * math.pi * 380.0 * (t - 0.04)) * 0.5 if t >= 0.04 else 0.0)
            ) * max(0.0, 1.0 - t / d),
        )

    @classmethod
    def synth_journal_flip(cls) -> pygame.mixer.Sound | None:
        """Paper dossier page turn / blueprint unfold (0.08s)."""
        return cls._create_wav_sound(
            0.08,
            lambda t, d, i: (
                ((i % 15) - 7) / 7.0 * 0.45
                + math.sin(2.0 * math.pi * 480.0 * t) * 0.25
            ) * max(0.0, math.sin(math.pi * t / d)),
        )

    @classmethod
    def synth_ui_toast(cls) -> pygame.mixer.Sound | None:
        """Typewriter bell notification ding (0.35s)."""
        return cls._create_wav_sound(
            0.35,
            lambda t, d, i: (
                math.sin(2.0 * math.pi * 1760.0 * t) * 0.7
                + math.sin(2.0 * math.pi * 3520.0 * t) * 0.3
            ) * max(0.0, math.exp(-t * 7.5)),
        )

    @classmethod
    def synth_ui_select(cls) -> pygame.mixer.Sound | None:
        """Subtle menu navigation tick (0.02s)."""
        return cls._create_wav_sound(
            0.02,
            lambda t, d, i: (
                math.sin(2.0 * math.pi * 820.0 * t) * 0.6
                + ((i % 5) - 2) / 2.0 * 0.2
            ) * max(0.0, 1.0 - t / d),
        )

    @classmethod
    def synth_wood_bootstep(cls, variation: int = 0) -> pygame.mixer.Sound | None:
        """Organic wood bootstep with heel strike, plank cavity body, and leather friction."""
        durations = [0.110, 0.095, 0.125, 0.090, 0.130, 0.105]
        fund_freqs = [142.0, 168.0, 150.0, 182.0, 132.0, 158.0]
        wood_modes = [310.0, 360.0, 290.0, 410.0, 275.0, 340.0]
        heel_clicks = [1750.0, 1520.0, 1920.0, 2200.0, 1400.0, 1650.0]
        decay_rates = [32.0, 38.0, 28.0, 42.0, 25.0, 35.0]

        idx = variation % len(durations)
        dur = durations[idx]
        f0 = fund_freqs[idx]
        f_wood = wood_modes[idx]
        f_click = heel_clicks[idx]
        decay = decay_rates[idx]

        def _gen(t: float, d: float, i: int) -> float:
            click = math.sin(2.0 * math.pi * f_click * t) * math.exp(-t * 220.0) * 0.45
            pitch_drop = f0 * (1.0 + 0.35 * math.exp(-t * 60.0))
            thud = math.sin(2.0 * math.pi * pitch_drop * t) * math.exp(-t * decay) * 0.65
            wood = (
                math.sin(2.0 * math.pi * f_wood * t + 0.3)
                * math.exp(-t * (decay * 1.35))
                * 0.38
            )
            sub = math.sin(2.0 * math.pi * 75.0 * t) * math.exp(-t * (decay * 1.6)) * 0.30
            scuff = (
                (((i % 11) - 5) / 5.0) * 0.22 * math.exp(-t * 45.0)
                if t < 0.04
                else 0.0
            )

            combined = click + thud + wood + sub + scuff
            attack = min(1.0, t / 0.0025)
            release = max(0.0, 1.0 - (t / d) ** 2.0)
            return math.tanh(combined * attack * release * 1.25)

        return cls._create_wav_sound(dur, _gen)

    @classmethod
    def synth_footstep(cls) -> pygame.mixer.Sound | None:
        """Default procedural leather bootstep on hardwood floor."""
        return cls.synth_wood_bootstep(0)


class AudioManager:
    """Centralized sound effect controller with procedural fallback and asset loading."""

    def __init__(
        self,
        master_volume: float = 0.8,
        sfx_volume: float = 0.85,
        music_volume: float = 0.65,
    ):
        self.enabled = False
        self.master_volume = max(0.0, min(1.0, master_volume))
        self.sfx_volume = max(0.0, min(1.0, sfx_volume))
        self.music_volume = max(0.0, min(1.0, music_volume))
        self.muted = False
        self.is_music_playing = False
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.footstep_sounds: list[pygame.mixer.Sound] = []
        self.last_footstep_time = 0.0

        self._init_mixer()
        self._load_sounds()

    def _init_mixer(self) -> None:
        """Initialize pygame.mixer safely with dummy driver tolerance."""
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                self.enabled = True
            except (pygame.error, Exception) as exc:
                self.enabled = False
        else:
            self.enabled = True

    def _load_sounds(self) -> None:
        """Load external sound assets from disk or synthesize procedural defaults."""
        if not self.enabled:
            return

        sound_generators = {
            "puzzle_click": Synthesizer.synth_puzzle_click,
            "puzzle_digit": Synthesizer.synth_puzzle_digit,
            "puzzle_solved": Synthesizer.synth_puzzle_solved,
            "puzzle_failed": Synthesizer.synth_puzzle_failed,
            "inspect_open": Synthesizer.synth_inspect_open,
            "inspect_close": Synthesizer.synth_inspect_close,
            "evidence_reveal": Synthesizer.synth_evidence_reveal,
            "guard_alert": Synthesizer.synth_guard_alert,
            "game_over": Synthesizer.synth_game_over,
            "door_open": Synthesizer.synth_door_open,
            "door_locked": Synthesizer.synth_door_locked,
            "door_unlocked": Synthesizer.synth_door_unlocked,
            "journal_flip": Synthesizer.synth_journal_flip,
            "ui_toast": Synthesizer.synth_ui_toast,
            "ui_select": Synthesizer.synth_ui_select,
            "footstep": Synthesizer.synth_footstep,
        }

        for name, generator in sound_generators.items():
            sound = None
            # Check for disk override in assets/sounds/
            if os.path.isdir(SOUND_ASSETS_DIR):
                for ext in (".wav", ".ogg"):
                    path = os.path.join(SOUND_ASSETS_DIR, f"{name}{ext}")
                    if os.path.isfile(path):
                        try:
                            sound = pygame.mixer.Sound(path)
                            break
                        except Exception:
                            sound = None

            # Fall back to procedural synthesis
            if sound is None:
                sound = generator()

            if sound is not None:
                self.sounds[name] = sound

        # Load wood bootstep variation pool (assets/audio/ or procedural fallback)
        self.footstep_sounds.clear()
        for i in range(1, 7):
            step_sound = None
            for folder in (AUDIO_ASSETS_DIR, SOUND_ASSETS_DIR):
                if os.path.isdir(folder):
                    for ext in (".wav", ".ogg"):
                        path = os.path.join(folder, f"bootstep_{i}{ext}")
                        if os.path.isfile(path):
                            try:
                                step_sound = pygame.mixer.Sound(path)
                                break
                            except Exception:
                                step_sound = None
                    if step_sound is not None:
                        break

            if step_sound is None:
                step_sound = Synthesizer.synth_wood_bootstep(i - 1)

            if step_sound is not None:
                self.footstep_sounds.append(step_sound)

        if self.footstep_sounds and "footstep" not in self.sounds:
            self.sounds["footstep"] = self.footstep_sounds[0]

    def play(self, sound_name: str, volume_mult: float = 1.0) -> None:
        """Play a designated sound effect if mixer is active and unmuted."""
        if not self.enabled or self.muted:
            return

        sound = self.sounds.get(sound_name)
        if sound is not None:
            effective_vol = max(
                0.0, min(1.0, self.master_volume * self.sfx_volume * volume_mult)
            )
            sound.set_volume(effective_vol)
            sound.play()

    def play_menu_music(self) -> None:
        """Play the main menu music track in a continuous loop from the beginning."""
        if not self.enabled or not os.path.isfile(MENU_MUSIC_PATH):
            return

        try:
            pygame.mixer.music.load(MENU_MUSIC_PATH)
            effective_vol = (
                0.0 if self.muted else max(0.0, min(1.0, self.master_volume * self.music_volume))
            )
            pygame.mixer.music.set_volume(effective_vol)
            pygame.mixer.music.play(loops=-1, start=0.0)
            self.is_music_playing = True
        except Exception:
            self.is_music_playing = False

    def stop_menu_music(self) -> None:
        """Stop menu background music playback."""
        if not self.enabled:
            return

        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        self.is_music_playing = False

    def play_footstep(
        self,
        current_time: float | None = None,
        interval: float = 0.32,
        volume_mult: float = 1.0,
    ) -> bool:
        """Play a wood bootstep sound from the variation pool on an available channel."""
        if not self.enabled or self.muted:
            return False

        if current_time is not None:
            if current_time - self.last_footstep_time < interval:
                return False
            self.last_footstep_time = current_time

        pool = (
            self.footstep_sounds
            if self.footstep_sounds
            else ([self.sounds["footstep"]] if "footstep" in self.sounds else [])
        )
        if not pool:
            return False

        sound = random.choice(pool)
        vol_variation = random.uniform(0.70, 0.90)
        effective_vol = max(
            0.0,
            min(1.0, self.master_volume * self.sfx_volume * vol_variation * volume_mult),
        )
        sound.set_volume(effective_vol)

        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(sound)
        else:
            sound.play()
        return True

    def set_master_volume(self, volume: float) -> None:
        """Adjust master volume level between 0.0 and 1.0."""
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_music_volume()

    def set_sfx_volume(self, volume: float) -> None:
        """Adjust sound effects volume level between 0.0 and 1.0."""
        self.sfx_volume = max(0.0, min(1.0, volume))

    def set_music_volume(self, volume: float) -> None:
        """Adjust background music volume level between 0.0 and 1.0."""
        self.music_volume = max(0.0, min(1.0, volume))
        self._update_music_volume()

    def _update_music_volume(self) -> None:
        """Synchronize active music playback volume with current settings."""
        if not self.enabled:
            return
        try:
            effective_vol = (
                0.0 if self.muted else max(0.0, min(1.0, self.master_volume * self.music_volume))
            )
            pygame.mixer.music.set_volume(effective_vol)
        except Exception:
            pass

    def toggle_mute(self) -> bool:
        """Toggle mute state and return new mute status."""
        self.muted = not self.muted
        self._update_music_volume()
        return self.muted

    def is_muted(self) -> bool:
        """Return True if audio playback is currently muted."""
        return self.muted


# Singleton instance
_audio_manager_instance: AudioManager | None = None


def get_audio_manager() -> AudioManager:
    """Return the global AudioManager singleton instance."""
    global _audio_manager_instance
    if _audio_manager_instance is None:
        _audio_manager_instance = AudioManager()
    return _audio_manager_instance


def play_sound(sound_name: str, volume_mult: float = 1.0) -> None:
    """Convenience helper to play a sound via the global audio manager."""
    get_audio_manager().play(sound_name, volume_mult=volume_mult)


def play_menu_music() -> None:
    """Convenience helper to start playing the menu music track from the start."""
    get_audio_manager().play_menu_music()


def stop_menu_music() -> None:
    """Convenience helper to stop the menu music track."""
    get_audio_manager().stop_menu_music()


def play_footstep(
    current_time: float | None = None,
    interval: float = 0.32,
    volume_mult: float = 1.0,
) -> bool:
    """Convenience helper to play a wood bootstep sound via the global audio manager."""
    return get_audio_manager().play_footstep(
        current_time=current_time, interval=interval, volume_mult=volume_mult
    )

