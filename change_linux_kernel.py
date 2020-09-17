#!/usr/bin/python3
import subprocess


def set_grub_default(kernel_version: str):
    grub_file_path = "/etc/grub/default"
    with open(grub_file_path, "r") as grub_config:
        grub_lines = grub_config.readlines()
        for i in range(len(grub_lines)):
            if line.startswith("GRUB_DEFAULT="):
                grub_lines[
                    i
                ] = f"GRUB_DEFAULT=Advanced options for Ubuntu>Ubuntu, with Linux {kernel_version}"
                break
    if grub_lines:
        with open(grub_file_path, "w") as grub_config:
            grub_config.writelines(grub_lines)


if __name__ == "__main__":
    """"In order to change the kernel this script has to be run with raised privileges (superuser)."""

    cmd = "grub-mkconfig | grep -E 'submenu |menuentry '"
    process = subprocess.run(
        cmd, shell=True, universal_newlines=True, capture_output=True
    )
    lines = process.stdout.split("\n")
    kernels = set()
    for line in lines:
        if ", with Linux" in line:
            first_linux_part = line[
                line.find(", with Linux") : line.find(", with Linux") + 50
            ]
            second_part = first_linux_part[
                len(", with Linux ") : first_linux_part.find("'")
            ]
            kernels.add(second_part)
    print("Available Kernels:")
    sorted_kernels = sorted(list(kernels))
    for i, kernel in enumerate(sorted_kernels):
        print(f"[{i}] {kernel}")
    chosen_kernel = input("Enter kernel version or number: ")
    print(f"Selected kernel: {chosen_kernel}")
    chosen_number = -1
    is_number = True
    try:
        chosen_number = int(chosen_kernel)
    except ValueError:
        # chosen_number is not an int
        is_number = False

    if is_number:
        if chosen_number not in range(len(kernels)):
            print("No valid kernel was provided.")
            exit(1)
        else:
            chosen_kernel = sorted_kernels[chosen_number]

    if chosen_kernel not in kernels:
        print("No valid kernel was provided.")
        print(f"Please check if '{chosen_kernel}' was listed in the available kernel.")
        exit(1)

    approval = input(f"Are you sure to change to this version (y/n):")
    if approval.strip().lower() == "y":
        print(f"Changing to version {chosen_kernel}.")
        set_grub_default(kernel_version=chosen_kernel)
        subprocess.run("update-grub")
        print("Updated grub.")
        print("Finished.")
        print("Please reboot to apply changes.")
