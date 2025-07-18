```
Plugin Name: "Fast Lookahead limiter"
Plugin Label: "fastLookaheadLimiter"
Plugin Unique ID: 1913
Maker: "Steve Harris <steve@plugin.org.uk>"
Copyright: "GPL"
Must Run Real-Time: No
Has activate() Function: Yes
Has deactivate() Function: No
Has run_adding() Function: Yes
Environment: Normal or Hard Real-Time
Ports:	"Input gain (dB)" input, control, -20 to 20, default 0
	"Limit (dB)" input, control, -20 to 0, default 0
	"Release time (s)" input, control, 0.01 to 2, default 0.5075
	"Attenuation (dB)" output, control, 0 to 70
	"Input 1" input, audio
	"Input 2" input, audio
	"Output 1" output, audio
	"Output 2" output, audio
	"latency" output, control


Plugin Name: "Glame Highpass Filter"
Plugin Label: "highpass_iir"
Plugin Unique ID: 1890
Maker: "Alexander Ehlert <mag@glame.de>"
Copyright: "GPL"
Must Run Real-Time: No
Has activate() Function: Yes
Has deactivate() Function: No
Has run_adding() Function: Yes
Environment: Normal or Hard Real-Time
Ports:	"Cutoff Frequency" input, control, 0.0001*srate to 0.45*srate, default 0.000819036*srate, logarithmic
	"Stages(2 poles per stage)" input, control, 1 to 10, default 1, integer
	"Input" input, audio
	"Output" output, audio


Plugin Name: "Glame Lowpass Filter"
Plugin Label: "lowpass_iir"
Plugin Unique ID: 1891
Maker: "Alexander Ehlert <mag@glame.de>"
Copyright: "GPL"
Must Run Real-Time: No
Has activate() Function: Yes
Has deactivate() Function: No
Has run_adding() Function: Yes
Environment: Normal or Hard Real-Time
Ports:	"Cutoff Frequency" input, control, 0.0001*srate to 0.45*srate, default 0.0549426*srate, logarithmic
	"Stages(2 poles per stage)" input, control, 1 to 10, default 1, integer
	"Input" input, audio
	"Output" output, audio


Plugin Name: "Matrix: Stereo to MS"
Plugin Label: "matrixStMS"
Plugin Unique ID: 1420
Maker: "Steve Harris <steve@plugin.org.uk>"
Copyright: "GPL"
Must Run Real-Time: No
Has activate() Function: No
Has deactivate() Function: No
Has run_adding() Function: Yes
Environment: Normal or Hard Real-Time
Ports:	"Left" input, audio
	"Right" input, audio
	"Mid" output, audio
	"Side" output, audio


Plugin Name: "Triple band parametric with shelves"
Plugin Label: "triplePara"
Plugin Unique ID: 1204
Maker: "Steve Harris <steve@plugin.org.uk>"
Copyright: "GPL"
Must Run Real-Time: No
Has activate() Function: Yes
Has deactivate() Function: No
Has run_adding() Function: Yes
Environment: Normal or Hard Real-Time
Ports:	"Low-shelving gain (dB)" input, control, -70 to 30, default 0
	"Low-shelving frequency (Hz)" input, control, 0.0001*srate to 0.49*srate, default 0.0001*srate, logarithmic
	"Low-shelving slope" input, control, 0 to 1, default 0.5
	"Band 1 gain (dB)" input, control, -70 to 30, default 0
	"Band 1 frequency (Hz)" input, control, 0.0001*srate to 0.49*srate, default 0.00083666*srate, logarithmic
	"Band 1 bandwidth (octaves)" input, control, 0 to 4, default 1
	"Band 2 gain (dB)" input, control, -70 to 30, default 0
	"Band 2 frequency (Hz)" input, control, 0.0001*srate to 0.49*srate, default 0.007*srate, logarithmic
	"Band 2 bandwidth (octaves)" input, control, 0 to 4, default 1
	"Band 3 gain (dB)" input, control, -70 to 30, default 0
	"Band 3 frequency (Hz)" input, control, 0.0001*srate to 0.49*srate, default 0.0585662*srate, logarithmic
	"Band 3 bandwidth (octaves)" input, control, 0 to 4, default 1
	"High-shelving gain (dB)" input, control, -70 to 30, default 0
	"High-shelving frequency (Hz)" input, control, 0.0001*srate to 0.49*srate, default 0.49*srate, logarithmic
	"High-shelving slope" input, control, 0 to 1, default 0.5
	"Input" input, audio, -1 to 1
	"Output" output, audio, -1 to 1

Plugin Name: "Multiband EQ"
Plugin Label: "mbeq"
Plugin Unique ID: 1197
Maker: "Steve Harris <steve@plugin.org.uk>"
Copyright: "GPL"
Must Run Real-Time: No
Has activate() Function: Yes
Has deactivate() Function: No
Has run_adding() Function: Yes
Environment: Normal or Hard Real-Time
Ports:	"50Hz gain (low shelving)" input, control, -70 to 30, default 0
	"100Hz gain" input, control, -70 to 30, default 0
	"156Hz gain" input, control, -70 to 30, default 0
	"220Hz gain" input, control, -70 to 30, default 0
	"311Hz gain" input, control, -70 to 30, default 0
	"440Hz gain" input, control, -70 to 30, default 0
	"622Hz gain" input, control, -70 to 30, default 0
	"880Hz gain" input, control, -70 to 30, default 0
	"1250Hz gain" input, control, -70 to 30, default 0
	"1750Hz gain" input, control, -70 to 30, default 0
	"2500Hz gain" input, control, -70 to 30, default 0
	"3500Hz gain" input, control, -70 to 30, default 0
	"5000Hz gain" input, control, -70 to 30, default 0
	"10000Hz gain" input, control, -70 to 30, default 0
	"20000Hz gain" input, control, -70 to 30, default 0
	"Input" input, audio
	"Output" output, audio
	"latency" output, control

Plugin Name: "Valve saturation"
Plugin Label: "valve"
Plugin Unique ID: 1209
Maker: "Steve Harris <steve@plugin.org.uk>"
Copyright: "GPL"
Must Run Real-Time: No
Has activate() Function: Yes
Has deactivate() Function: No
Has run_adding() Function: Yes
Environment: Normal or Hard Real-Time
Ports:	"Distortion level" input, control, 0 to 1, default 0
	"Distortion character" input, control, 0 to 1, default 0
	"Input" input, audio
	"Output" output, audio
```
