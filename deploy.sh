#!/bin/sh
# Deploy to https://lemmingsvc.vercel.app
# Deploys a git-free copy of the site: Vercel blocks deploys whose git commit
# author isn't a member of the Vercel account.
set -e
cd "$(dirname "$0")"
D=$(mktemp -d)
mkdir -p "$D/play"
cp index.html og.png favicon.png "$D"/
cp -R img "$D"/
cp play/index.html play/sounds.js "$D/play/"
cp -R .vercel "$D"/
(cd "$D" && npx --yes vercel@latest deploy --prod --yes)  # uses the project linked in .vercel/ (run `vercel link` once)
rm -rf "$D"
