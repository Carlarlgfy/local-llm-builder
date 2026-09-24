#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p 'AI Builder.app/Contents/MacOS' 'AI Builder.app/Contents/Resources/local_builder'
cp packaging/Info.plist 'AI Builder.app/Contents/Info.plist'
cp local_builder/*.py local_builder/*.html 'AI Builder.app/Contents/Resources/local_builder/'
swiftc Launcher.swift -o 'AI Builder.app/Contents/MacOS/AIBuilder' -framework Cocoa -framework WebKit -framework PDFKit
icon_dir=$(mktemp -d "${TMPDIR:-/tmp}/ai-builder-icon.XXXXXX")
mkdir "$icon_dir/AppIcon.iconset"
swift MakeIcon.swift "$icon_dir/icon.png"
for size in 16 32 128 256 512; do
    sips -z "$size" "$size" "$icon_dir/icon.png" --out "$icon_dir/AppIcon.iconset/icon_${size}x${size}.png" >/dev/null
    double_size=$((size * 2))
    sips -z "$double_size" "$double_size" "$icon_dir/icon.png" --out "$icon_dir/AppIcon.iconset/icon_${size}x${size}@2x.png" >/dev/null
done
iconutil -c icns "$icon_dir/AppIcon.iconset" -o 'AI Builder.app/Contents/Resources/AppIcon.icns'
codesign --force --deep --sign - 'AI Builder.app'
codesign --verify --deep --strict 'AI Builder.app'
