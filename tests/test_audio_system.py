"""
Unit tests for the Case Unknown audio and sound synthesis system.
"""

import os
import unittest
import pygame

os.environ["SDL_VIDEODRIVER"] = "dummy"

from src.audio_manager import (
    AudioManager,
    Synthesizer,
    get_audio_manager,
    play_sound,
    play_menu_music,
    stop_menu_music,
)


class TestAudioSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            except Exception:
                pass

    def test_synthesizer_waveforms(self):
        """Verify all 16 procedural waveform generators produce valid Sound objects when mixer is active."""
        if not pygame.mixer.get_init():
            self.skipTest("Pygame mixer not supported in this test environment.")

        sound_generators = [
            ("puzzle_click", Synthesizer.synth_puzzle_click),
            ("puzzle_digit", Synthesizer.synth_puzzle_digit),
            ("puzzle_solved", Synthesizer.synth_puzzle_solved),
            ("puzzle_failed", Synthesizer.synth_puzzle_failed),
            ("inspect_open", Synthesizer.synth_inspect_open),
            ("inspect_close", Synthesizer.synth_inspect_close),
            ("evidence_reveal", Synthesizer.synth_evidence_reveal),
            ("guard_alert", Synthesizer.synth_guard_alert),
            ("game_over", Synthesizer.synth_game_over),
            ("door_open", Synthesizer.synth_door_open),
            ("door_locked", Synthesizer.synth_door_locked),
            ("door_unlocked", Synthesizer.synth_door_unlocked),
            ("journal_flip", Synthesizer.synth_journal_flip),
            ("ui_toast", Synthesizer.synth_ui_toast),
            ("ui_select", Synthesizer.synth_ui_select),
            ("footstep", Synthesizer.synth_footstep),
        ]

        for name, generator in sound_generators:
            sound = generator()
            self.assertIsNotNone(sound, f"Failed to synthesize {name}")
            self.assertGreater(sound.get_length(), 0.0, f"Sound {name} has zero duration")

    def test_audio_manager_singleton(self):
        """Ensure get_audio_manager returns a consistent singleton instance."""
        mgr1 = get_audio_manager()
        mgr2 = get_audio_manager()
        self.assertIs(mgr1, mgr2)

    def test_volume_and_mute_controls(self):
        """Test master volume, sfx volume, and mute state toggling."""
        mgr = AudioManager(master_volume=0.8, sfx_volume=0.9)
        self.assertAlmostEqual(mgr.master_volume, 0.8)
        self.assertAlmostEqual(mgr.sfx_volume, 0.9)
        self.assertFalse(mgr.is_muted())

        mgr.set_master_volume(0.5)
        self.assertAlmostEqual(mgr.master_volume, 0.5)

        mgr.set_sfx_volume(0.3)
        self.assertAlmostEqual(mgr.sfx_volume, 0.3)

        # Clamping
        mgr.set_master_volume(1.5)
        self.assertAlmostEqual(mgr.master_volume, 1.0)
        mgr.set_master_volume(-0.5)
        self.assertAlmostEqual(mgr.master_volume, 0.0)

        # Mute toggle
        self.assertTrue(mgr.toggle_mute())
        self.assertTrue(mgr.is_muted())
        self.assertFalse(mgr.toggle_mute())
        self.assertFalse(mgr.is_muted())

    def test_play_footstep_interval(self):
        """Test that footstep sounds are throttled to proper walking cadence intervals."""
        mgr = AudioManager()
        # First call at t=1.0 should play
        played1 = mgr.play_footstep(current_time=1.0, interval=0.32)
        self.assertTrue(played1)

        # Immediate follow-up call at t=1.1 (delta 0.1 < 0.32) should not play
        played2 = mgr.play_footstep(current_time=1.1, interval=0.32)
        self.assertFalse(played2)

        # Call at t=1.35 (delta 0.35 >= 0.32) should play
        played3 = mgr.play_footstep(current_time=1.35, interval=0.32)
        self.assertTrue(played3)

    def test_playback_helpers_do_not_raise(self):
        """Verify play_sound and audio manager play never raise uncaught exceptions."""
        play_sound("puzzle_click")
        play_sound("evidence_reveal")
        play_sound("non_existent_sound_key")  # Should be cleanly ignored

    def test_menu_music_controls(self):
        """Verify menu music playback start, stop, volume adjustments, and mute behavior."""
        mgr = get_audio_manager()

        mgr.set_music_volume(0.5)
        self.assertAlmostEqual(mgr.music_volume, 0.5)
        mgr.set_music_volume(1.8)
        self.assertAlmostEqual(mgr.music_volume, 1.0)
        mgr.set_music_volume(-0.3)
        self.assertAlmostEqual(mgr.music_volume, 0.0)

        # Restore reasonable volume
        mgr.set_music_volume(0.65)

        # Helper functions should execute cleanly
        play_menu_music()
        if mgr.enabled:
            self.assertTrue(mgr.is_music_playing)

        # Calling play_menu_music again resets/restarts smoothly without error
        play_menu_music()
        if mgr.enabled:
            self.assertTrue(mgr.is_music_playing)

        stop_menu_music()
        if mgr.enabled:
            self.assertFalse(mgr.is_music_playing)


if __name__ == "__main__":
    unittest.main()

