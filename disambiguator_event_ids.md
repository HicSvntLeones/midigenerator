This is just a note for how things are handled in the midi disambiguator, might delete later.
All events stored as tuples.

0 - Note Begin - 0,  delta_time, channel, pitch, velocity, matched, length, <Desc>
1 - Midi Header - 1, midi_format_type, track_count, time_type, midi_PPQN, midi_FPS, midi_TPS, <Desc>
2 - Track Header - 2, track_length, <Desc>
3 - Tempo Change - 3, delta_time, tempo, bpm, <Desc>
4 - Key Signature Change - 4, delta_time, numerator, denominator, clocks_per_metronome_tick, thirtyseconds_per_tick, <Desc>
5 - End of track - 5, delta_time, <Desc>
6 - Instrument - 6, delta_time, instrument, <Desc>
7 - Control Change - 7, delta_time, channel, controller_number, value, match_index, <Desc>
8 - Program Change - 8, delta_time, channel, program, <Desc>
9 - Note End - 9, delta_time, channel, pitch, velocity, matched, <Desc>




999 - End of File - 999, delta_time, <desc>