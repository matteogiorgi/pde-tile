#!/usr/bin/env bash

# This 'pde-tile' setup script will install qtile window manager with a bare-bone
# configuration ready to be used as a base for further customization.
# ---
# There are no worries of losing a potential old configuration: il will be
# stored in a separate folder in order to be restored manually if needed.




### Check & Funcs
#################

RED='\033[1;36m'
NC='\033[0m'
# ---
if [[ -d "${HOME}/.tilerestore" ]]; then
    printf "\n${RED}%s${NC}"   "════════ Warning: pde-conf already set ════════"
    printf "\n${RED}%s${NC}\n" "Remove ~/.tilerestore and run this script again"
    exit 1
fi
# ---
function warning-message () {
    if [[ "$(id -u)" = 0 ]]; then
        printf "\n${RED}%s${NC}"     "This script MUST NOT be run as root user since it makes changes"
        printf "\n${RED}%s${NC}"     "to the \$HOME directory of the \$USER executing this script."
        printf "\n${RED}%s${NC}"     "The \$HOME directory of the root user is, of course, '/root'."
        printf "\n${RED}%s${NC}"     "We don't want to mess around in there. So run this script as a"
        printf "\n${RED}%s${NC}\n\n" "normal user. You will be asked for a sudo password when necessary."
        exit 1
    fi
}
# ---
function error-echo () {
    printf "${RED}ERROR: %s${NC}\n" "$1" >&2
    exit 1
}
# ---
function store-conf () {
    function backup-conf () {
        if [[ -f "$1" ]]; then
            if [[ -L "$1" ]]; then
                command unlink "$1"
            else
                mv "$1" "${RESTORE}"
            fi
        fi
    }
    RESTORE="${HOME}/.tilerestore" && command mkdir -p "${RESTORE}"
    backup-conf "${HOME}/.config/qtile/config.py"
    backup-conf "${HOME}/.config/qtile/autostart.sh"
    backup-conf "${HOME}/.config/qtile/wallpaper.png"
}




### Start
#########

warning-message
SCRIPTPATH="$( cd "$(command dirname "$0")" ; pwd -P )" || exit 1
command sudo apt-get update && sudo apt-get upgrade -qq -y || error-echo "syncing repos"
command sudo apt-get install -qq -y python3 python3-pip fonts-liberation diodon || error-echo "installing from apt"
command pip3 install qtile || error-echo "installing from pip"
# ---
store-conf
QTILE="${HOME}/.config/qtile" && command mkdir -p "${QTILE}"
cp "${SCRIPTPATH}/qtile/config.py" "${QTILE}/"
cp "${SCRIPTPATH}/qtile/autostart.sh" "${QTILE}/"
cp "${SCRIPTPATH}/qtile/wallpaper.png" "${QTILE}/"




### Finish
##########

printf "${RED}%s${NC}\n" "setup complete"
