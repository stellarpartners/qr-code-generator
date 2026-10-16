#!/usr/bin/env bash
# Recompute the Subresource Integrity hashes for the two CDN libraries used by
# index.html. Run this after bumping a version, then paste the new hash into the
# matching integrity="..." attribute.
#
#   ./tools/check-integrity.sh
#
set -euo pipefail

QR_VERSION="1.9.2"
JSPDF_VERSION="2.5.1"

QR_URL="https://unpkg.com/qr-code-styling@${QR_VERSION}/lib/qr-code-styling.js"
JSPDF_URL="https://unpkg.com/jspdf@${JSPDF_VERSION}/dist/jspdf.umd.min.js"

sri() {
  curl -fsSL "$1" | openssl dgst -sha384 -binary | openssl base64 -A
}

echo "qr-code-styling ${QR_VERSION}"
echo "  url:  ${QR_URL}"
echo "  hash: sha384-$(sri "$QR_URL")"
echo
echo "jsPDF ${JSPDF_VERSION}"
echo "  url:  ${JSPDF_URL}"
echo "  hash: sha384-$(sri "$JSPDF_URL")"
echo
echo "Compare these with the integrity attributes in index.html."
