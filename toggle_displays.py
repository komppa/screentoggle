import subprocess


def get_connected_displays():
    
    result = subprocess.run(['xrandr', '--query'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    connected_displays = {}
    current_display = None
    resolutions = []

    for line in lines:
        if ' connected' in line and 'eDP-1' not in line:
            if current_display and resolutions:
                max_resolution = max(resolutions, key=lambda res: [int(num) for num in res.split('x')])
                connected_displays[current_display] = max_resolution
            current_display = line.split()[0]
            resolutions = []
        elif current_display and ' connected' not in line and line.strip():
            resolutions.append(line.strip().split()[0])

    if current_display and resolutions:
        max_resolution = max(resolutions, key=lambda res: [int(num) for num in res.split('x')])
        connected_displays[current_display] = max_resolution

    return connected_displays


def get_active_display():

    result = subprocess.run(['xrandr', '--query'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    for line in lines:
        if ' connected' in line and '+0+0' in line and 'eDP-1' not in line:
            return line.split()[0]
    return None


def main():

    external_displays = get_connected_displays()
    num_displays = len(external_displays)
    
    if num_displays == 0:
        return
    
    active_display = get_active_display()
    two_k_displays = [display for display, res in external_displays.items() if '2560x1440' in res]
    fullhd_display = [display for display, res in external_displays.items() if '1920x1080' in res]
    
    if active_display:
        active_resolution = external_displays[active_display]
        if '2560x1440' in active_resolution:
            # If a 2K display is active, turn off both 2K displays and switch to the Full HD display
            for display in two_k_displays:
                subprocess.run(['xrandr', '--output', display, '--off'])
            if fullhd_display:
                subprocess.run(['xrandr', '--output', fullhd_display[0], '--auto'])
        elif '1920x1080' in active_resolution:
            subprocess.run(['xrandr', '--output', active_display, '--off'])
            if len(two_k_displays) >= 2:
                subprocess.run(['xrandr', '--output', two_k_displays[0], '--auto', '--primary'])
                subprocess.run(['xrandr', '--output', two_k_displays[1], '--auto', '--right-of', two_k_displays[0]])
            elif len(two_k_displays) == 1:
                subprocess.run(['xrandr', '--output', two_k_displays[0], '--auto'])
    else:
        # Default to Full HD if no active display is found
        if fullhd_display:
            subprocess.run(['xrandr', '--output', fullhd_display[0], '--auto'])
        for display in two_k_displays:
            subprocess.run(['xrandr', '--output', display, '--off'])


if __name__ == "__main__":
    main()
