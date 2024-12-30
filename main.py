#!/usr/bin/env python3

import argparse
import numpy as np
import os
import subprocess
import sys
import shutil
path_to_add = "/Users/binxiaokang/Desktop/feedbackdownload/Argyll_V3.2.0/bin"
os.environ["PATH"] += os.pathsep + path_to_add
executable_name = "your_executable_here"  # Replace with the actual executable name
executable_path = shutil.which(executable_name)

if executable_path:
    print(f"Executable found at: {executable_path}")
else:
    print(f"Executable {executable_name} not found in PATH")


def parse_input_file(input_file):
    """Parse the input configuration file."""
    config = {}
    with open(input_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith('file description:'):
            config['description'] = line.split(':', 1)[1].strip()
        elif line.startswith('color primaries:'):
            primaries_str = line.split(':', 1)[1].strip()
            primaries_values = [float(v) for v in primaries_str.split()]
            if len(primaries_values) != 6:
                raise ValueError('Invalid number of color primary values. Expected 6 values.')
            config['color_primaries'] = primaries_values
        elif line.startswith('gamma curve params:'):
            params_str = line.split(':', 1)[1].strip()
            params = {}
            for param in params_str.split(','):
                key_value = param.strip().split(':')
                if len(key_value) != 2:
                    raise ValueError('Invalid gamma curve parameter format.')
                key = key_value[0].strip()
                value = float(key_value[1].strip())
                params[key] = value
            required_params = {'alpha', 'beta', 'gamma', 'delta'}
            if not required_params.issubset(params.keys()):
                missing = required_params - params.keys()
                raise ValueError(f'Missing gamma curve parameters: {missing}')
            config['gamma_params'] = params
        else:
            # Ignore unrecognized lines or add custom handling if needed
            pass
    return config


def generate_trc_file(gamma_params, steps=4096, trc_filename='temp_trc.txt'):
    """Generate the transfer curve (TRC) file based on gamma parameters."""
    alpha = gamma_params['alpha']
    beta = gamma_params['beta']
    gamma = gamma_params['gamma']
    delta = gamma_params['delta']

    # Generate normalized linear light values (L) from 0 to 1
    L_values = np.linspace(0, 1, steps)

    # Compute encoded values (E) based on the gamma curve
    E_values = []
    for L in L_values:
        if L < beta:
            E = delta * L
        else:
            E = alpha * (L ** gamma) - (alpha - 1)
        E_values.append(E)

    # Ensure E_values are within [0, 1]
    E_values = np.clip(E_values, 0, 1)

    # Write E_values to the TRC file
    with open(trc_filename, 'w') as f:
        for E in E_values:
            f.write(f"{E}\n")

    return trc_filename


def create_icc_profile(description, color_primaries, trc_filename, output_icc_path):
    """Create the ICC profile using ArgyllCMS's curve2icc utility."""
    # Ensure ArgyllCMS's curve2icc is accessible
    if not shutil.which('curve2icc'):
        print('Error: curve2icc not found. Please ensure ArgyllCMS is installed and curve2icc is in your PATH.')
        sys.exit(1)

    # Prepare the curve2icc command
    command = [
        'curve2icc',
        '-v',
        '-c', description,
        '-u', description,
        '-s',
        '-t', trc_filename,
        '-x',
        f"{color_primaries[0]:.4f}", f"{color_primaries[1]:.4f}",
        f"{color_primaries[2]:.4f}", f"{color_primaries[3]:.4f}",
        f"{color_primaries[4]:.4f}", f"{color_primaries[5]:.4f}",
        '-w', '0.3127', '0.3290',  # Using D65 white point
        output_icc_path
    ]

    # Run the command
    try:
        subprocess.run(command, check=True)
        print(f"ICC profile created at {output_icc_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating ICC profile: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Generate an ICC profile based on input configuration.')
    parser.add_argument('input_file', help='Path to the input configuration file.')
    parser.add_argument('output_icc', help='Path to save the generated ICC profile.')
    parser.add_argument('--trc_steps', type=int, default=4096, help='Number of steps in the TRC (default: 4096).')
    args = parser.parse_args()

    # Parse the input configuration file
    try:
        config = parse_input_file(args.input_file)
    except Exception as e:
        print(f"Error parsing input file: {e}")
        sys.exit(1)

    # Generate the TRC file
    trc_filename = 'temp_trc.txt'  # Temporary file for the TRC
    try:
        generate_trc_file(config['gamma_params'], steps=args.trc_steps, trc_filename=trc_filename)
    except Exception as e:
        print(f"Error generating TRC file: {e}")
        sys.exit(1)

    # Create the ICC profile
    try:
        create_icc_profile(config['description'], config['color_primaries'], trc_filename, args.output_icc)
    finally:
        # Clean up the temporary TRC file
        if os.path.exists(trc_filename):
            os.remove(trc_filename)


if __name__ == '__main__':
    main()
