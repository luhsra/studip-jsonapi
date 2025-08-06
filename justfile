default:
    @just --list

release *version:
    echo "Releasing version {{ version }}"
    git tag --sign -a "v{{ version }}" -m "Released version {{ version }}"
    git tag -l
    git push origin "v{{ version }}"
