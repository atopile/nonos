def calculate_min_inductance(Vin_max, Vout, Io, K_IND, fsw):
    """
    Calculate the minimum inductance required for an output inductor in a buck converter,
    correcting the previous misunderstanding in the formula application.
    
    Parameters:
    - Vin_max: Maximum input voltage (V)
    - Vout: Output voltage (V)
    - Io: DC output current (A)
    - K_IND: Ripple factor (expressed as a fraction of Io, e.g., 0.3 for 30%)
    - fsw: Switching frequency (Hz)

    Returns:
    - Lmin: Minimum inductance (H)
    """
    # Correcting the formula based on the typical approach for calculating minimum inductance
    Lmin = (Vin_max - Vout) * Vout / (Vin_max * Io * K_IND * fsw)
    return Lmin

# Correcting the example values and recalculating
Vin_max = 12  # Assuming a more typical maximum input voltage of 12V
Vout = 5  # Output voltage in volts
Io = 0.6  # Assuming a DC output current of 2A
K_IND = 0.3  # Ripple factor, 30% of Io
fsw = 2.1e6  # Correcting the switching frequency to a more typical value, e.g., 500 kHz

Lmin = calculate_min_inductance(Vin_max, Vout, Io, K_IND, fsw)
# print(Lmin)
# convert to uH
Lmin = Lmin * 1e6
print(Lmin)
