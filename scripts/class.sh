#!/usr/bin/env bash
# Snapshots of the files a class is allowed to change.
set -euo pipefail
cd "$(dirname "$0")/.."
root="$(pwd)"
snap_root="${root}/.class-snapshots"
mkdir -p "$snap_root" class-work

track_list() {
  find episodes/files learners class-work -type f \
    ! -name '.gitkeep' \
    ! -path '*/.git/*' \
    | sort
}

cmd="${1:-}"
case "$cmd" in
  before)
    n=1
    if [[ -f "${snap_root}/latest" ]]; then
      n=$(($(cat "${snap_root}/latest") + 1))
    fi
    dir="${snap_root}/${n}"
    mkdir -p "$dir/files"
    while IFS= read -r path; do
      [[ -n "$path" ]] || continue
      mkdir -p "${dir}/files/$(dirname "$path")"
      cp -a "$path" "${dir}/files/${path}"
      echo "$path" >> "${dir}/manifest"
    done < <(track_list)
    echo "$n" > "${snap_root}/latest"
    echo "$n"
    ;;
  changed|undo)
    n="${2:-}"
    if [[ -z "$n" ]]; then
      echo "usage: class.sh ${cmd} N" >&2
      exit 2
    fi
    dir="${snap_root}/${n}"
    if [[ ! -d "$dir" ]]; then
      echo "no snapshot ${n}" >&2
      exit 1
    fi
    if [[ "$cmd" == "changed" ]]; then
      while IFS= read -r path; do
        [[ -n "$path" ]] || continue
        if [[ ! -f "${dir}/files/${path}" ]]; then
          echo "added ${path}"
        elif ! cmp -s "$path" "${dir}/files/${path}"; then
          echo "changed ${path}"
        fi
      done < <(track_list)
      if [[ -f "${dir}/manifest" ]]; then
        while IFS= read -r path; do
          [[ -n "$path" ]] || continue
          if [[ ! -f "$path" ]]; then
            echo "removed ${path}"
          fi
        done < "${dir}/manifest"
      fi
    else
      if [[ -f "${dir}/manifest" ]]; then
        while IFS= read -r path; do
          [[ -n "$path" ]] || continue
          mkdir -p "$(dirname "$path")"
          cp -a "${dir}/files/${path}" "$path"
        done < "${dir}/manifest"
      fi
      while IFS= read -r path; do
        [[ -n "$path" ]] || continue
        if [[ ! -f "${dir}/files/${path}" ]]; then
          rm -f "$path"
          echo "removed ${path}"
        fi
      done < <(track_list)
    fi
    ;;
  *)
    echo "usage: class.sh before|changed N|undo N" >&2
    exit 2
    ;;
esac
