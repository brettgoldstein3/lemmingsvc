#!/bin/sh
# Deploy to https://lemmingsvc.vercel.app
# Deploys a git-free copy of the playable files: Vercel blocks deploys whose
# git commit author isn't a member of the Vercel account.
set -e
cd "$(dirname "$0")"
D=$(mktemp -d)
cp index.html sounds.js og.png favicon.png "$D"/
cp -R .vercel "$D"/
(cd "$D" && npx --yes vercel@latest deploy --prod --yes --scope brettlaunchhouses-projects)
rm -rf "$D"
